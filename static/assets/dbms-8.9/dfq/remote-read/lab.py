"""Serve the DFQ sample data on this machine's loopback interfaces."""
import argparse
from contextlib import ExitStack, contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
import functools
import hashlib
import json
import logging
import os
import shlex
import signal
import ssl
import subprocess
import threading

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
REGION = "us-east-1"
BUCKET = "dfq-lab-data"
EXAMPLE_PORTS = {
    "http": 18080, "destination": 18081, "https": 18443,
    "plain": 18210, "explicit": 18211, "implicit": 18990,
    "tftp": 18069, "s3": 19000,
}


def certificate(root):
    def openssl(*args):
        subprocess.run(["openssl", *args], cwd=root, check=True, capture_output=True)
    openssl("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "3",
            "-subj", "/CN=DFQ lab CA", "-keyout", "ca.key", "-out", "ca.pem")
    openssl("req", "-new", "-newkey", "rsa:2048", "-nodes", "-subj", "/CN=localhost",
            "-keyout", "server.key", "-out", "server.csr")
    (root / "server.ext").write_text("subjectAltName=DNS:localhost,DNS:dfq-lab-data.localhost,IP:127.0.0.1\nextendedKeyUsage=serverAuth\n")
    openssl("x509", "-req", "-days", "3", "-CA", "ca.pem", "-CAkey", "ca.key", "-set_serial",
            "1", "-in", "server.csr", "-extfile", "server.ext", "-out", "server.pem")


@contextmanager
def web(files, root, label, tls=False, redirect=None, port=0):
    log = root / "http-requests.jsonl"

    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def copyfile(self, source, output):
            while chunk := source.read(64 * 1024):
                self.transferred += output.write(chunk)

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            self.transferred = 0
            try:
                if path == "/redirect.csv" and redirect:
                    self.send_response(302)
                    self.send_header("Location", redirect + "/measurements.csv")
                    self.end_headers()
                else:
                    super().do_GET()
            finally:
                with log.open("a") as out:
                    out.write(json.dumps({"service": label, "path": path,
                                          "range": self.headers.get("Range"),
                                          "bytes_sent": self.transferred}) + "\n")

    with ThreadingHTTPServer((HOST, port), functools.partial(Handler, directory=files)) as server:
        if tls:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(root / "server.pem", root / "server.key")
            server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"{'https' if tls else 'http'}://{HOST}:{server.server_port}"
        finally:
            server.shutdown()
            thread.join()


@contextmanager
def ftp(files, root, mode, port=0):
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
    from pyftpdlib.ioloop import IOLoop
    from pyftpdlib.servers import FTPServer

    class ImplicitTLS(TLS_FTPHandler):
        def handle(self):
            self.secure_connection(self.ssl_context)
            super().handle()

    accounts = DummyAuthorizer()
    accounts.add_anonymous(str(files), perm="elr")
    accounts.add_user("dfq-lab", "loopback-fixture-only", str(files), perm="elr")
    base = {"plain": FTPHandler, "explicit": TLS_FTPHandler, "implicit": ImplicitTLS}[mode]
    handler = type("DFQFTPHandler", (base,), {
        "authorizer": accounts, "certfile": str(root / "server.pem"),
        "keyfile": str(root / "server.key"), "tls_control_required": mode != "plain",
        "tls_data_required": mode != "plain",
    })
    server = FTPServer((HOST, port), handler, ioloop=IOLoop())
    port = server.socket.getsockname()[1]
    stop = threading.Event()

    def serve():
        while not stop.is_set():
            server.ioloop.loop(timeout=0.05, blocking=False)

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        scheme = "ftps" if mode == "implicit" else "ftp"
        yield f"{scheme}://{HOST}:{port}"
    finally:
        stop.set()
        thread.join()
        server.close_all()


@contextmanager
def tftp(files, port=0):
    import tftpy

    server = tftpy.TftpServer(tftproot=str(files))
    thread = threading.Thread(target=server.listen, args=(HOST, port, 0.2, 4), daemon=True)
    thread.start()
    try:
        if not server.is_running.wait(5):
            raise RuntimeError("TFTP lab server did not start")
        yield f"tftp://{HOST}:{server.listenport}"
    finally:
        server.stop(now=True)
        thread.join(timeout=5)


@contextmanager
def s3(files, root, port=0):
    import boto3
    from botocore.config import Config
    from moto.server import DomainDispatcherApplication, create_backend_app
    from werkzeug.serving import make_server

    server = make_server(HOST, port, DomainDispatcherApplication(create_backend_app),
                         threaded=True, ssl_context=(str(root / "server.pem"), str(root / "server.key")))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    endpoint = f"https://localhost:{server.server_port}"

    def client(service, key):
        return boto3.client(service, endpoint_url=endpoint, region_name=REGION,
                            aws_access_key_id=key, aws_secret_access_key="lab-only-secret",
                            verify=str(root / "ca.pem"),
                            config=Config(signature_version="s3v4" if service == "s3" else "v4",
                                          s3={"addressing_style": "path"}, proxies={}))

    try:
        lab = client("s3", "lab-profile-key")
        for bucket in (BUCKET, "dfq-lab-public"):
            lab.create_bucket(Bucket=bucket)
            for name in ("measurements.csv", "measurements.parquet", "a b.csv", "a%20b.csv"):
                access = {"ACL": "public-read"} if bucket == "dfq-lab-public" else {}
                lab.put_object(Bucket=bucket, Key=name, Body=(files / name).read_bytes(), **access)
        presigned = lab.generate_presigned_url("get_object",
                     Params={"Bucket": BUCKET, "Key": "measurements.csv"}, ExpiresIn=1800)
        yield endpoint, presigned
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def render(root):
    manifest = json.loads((root / "manifest.json").read_text())
    out = root / "sql"
    out.mkdir(exist_ok=True)
    for path in sorted((ROOT / "sql").glob("*.sql")):
        values = {key: str(value).replace("'", "''") for key, value in manifest.items()}
        (out / path.name).write_text(Template(path.read_text()).substitute(values))


def serve(root, ports):
    def stop(_signal, _frame):
        raise KeyboardInterrupt()

    signal.signal(signal.SIGTERM, stop)
    os.umask(0o077)
    os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
    for key in ("moto", "werkzeug", "pyftpdlib", "tftpy"):
        logging.getLogger(key).setLevel(logging.ERROR)
    root.mkdir(mode=0o700)
    files = root / "files"
    files.mkdir()
    for source in (ROOT / "data").iterdir():
        (files / source.name).write_bytes(source.read_bytes())
    csv = (files / "measurements.csv").read_bytes()
    for name in ("a b.csv", "a%20b.csv"):
        (files / name).write_bytes(csv)
    certificate(root)
    netrc = root / "ftp.netrc"
    netrc.write_text("machine 127.0.0.1 login dfq-lab password loopback-fixture-only\n")
    with ExitStack() as stack:
        enter = stack.enter_context
        other = enter(web(files, root, "destination", port=ports.get("destination", 0)))
        http = enter(web(files, root, "http", redirect=other, port=ports.get("http", 0)))
        https = enter(web(files, root, "https", tls=True, port=ports.get("https", 0)))
        plain, explicit, implicit = [
            enter(ftp(files, root, mode, port=ports.get(mode, 0)))
            for mode in ("plain", "explicit", "implicit")
        ]
        s3_endpoint, presigned = enter(s3(files, root, port=ports.get("s3", 0)))
        config = root / "aws-config"
        config.write_text(f"[profile dfq-lab]\nregion = {REGION}\nendpoint_url = {s3_endpoint}\n"
                          "s3 =\n    addressing_style = path\n")
        credentials = root / "aws-credentials"
        credentials.write_text("[dfq-lab]\naws_access_key_id = lab-profile-key\n"
                               "aws_secret_access_key = lab-only-secret\n")
        host_port = s3_endpoint.rsplit(":", 1)[1]
        mapping = dict(DFQ_FILES=str(files), DFQ_FILE_URI=files.as_uri(), DFQ_HTTP=http,
                       DFQ_HTTPS=https, DFQ_OTHER=other, DFQ_FTP=plain,
                       DFQ_FTP_ANON=plain.replace(HOST, "localhost"),
                       DFQ_EXPLICIT=explicit, DFQ_FTPS=implicit,
                       DFQ_TFTP=enter(tftp(files, port=ports.get("tftp", 0))),
                       DFQ_S3=s3_endpoint, DFQ_VIRTUAL=f"https://{BUCKET}.localhost:{host_port}",
                       DFQ_CA=str(root / "ca.pem"), DFQ_NETRC=str(netrc), DFQ_SIGNED=presigned,
                       DFQ_PARQUET_SHA=hashlib.sha256((files / "measurements.parquet").read_bytes()).hexdigest().upper())
        env = dict(AWS_CONFIG_FILE=str(config), AWS_SHARED_CREDENTIALS_FILE=str(credentials),
                   AWS_PROFILE="dfq-lab", AWS_ACCESS_KEY_ID="lab-environment-key",
                   AWS_SECRET_ACCESS_KEY="lab-only-secret", AWS_EC2_METADATA_DISABLED="true",
                   NO_PROXY="localhost,127.0.0.1,.localhost")
        (root / "server.env").write_text("unset AWS_SESSION_TOKEN\n" + "".join(
            f"export {key}={shlex.quote(value)}\n" for key, value in env.items()))
        (root / "manifest.json").write_text(json.dumps(mapping, indent=2) + "\n")
        render(root)
        print(f"DFQ lab ready: {root}\nSQL: {root / 'sql'}", flush=True)
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="new directory for the loopback lab")
    parser.add_argument("--example-ports", action="store_true",
                        help="use the loopback ports shown in the manual")
    args = parser.parse_args()
    serve(args.directory.resolve(), EXAMPLE_PORTS if args.example_ports else {})


if __name__ == "__main__":
    main()
