---
type: docs
title: '3.2 Standard Edition Installation'
weight: 20
toc: true
---

Standard Edition handles SQL and storage on one server. Install in this order: prepare the
package, configure the execution environment, create the database, check the license, start
the server, and verify SQL. A single server is not limited to small data sets; measure whether
its resources meet your throughput and retention requirements.

## Installation Paths

| OS | Method | Procedure |
|---|---|---|
| Linux | Tarball (.tgz) | [Tarball Installation](#linux-tarball) |
| Linux | Docker container | [Docker Installation](#linux-docker) |
| Windows | ZIP or installer | [Windows Package Installation](#windows-package) |

First complete [Linux Preparation](#linux-preparation-environment-linux) or
[Windows Preparation](#windows-preparation-environment-windows).

<a id="linux"></a>

## Linux Installation

| Method | Suitable situations |
|---|---|
| [Tarball](#linux-tarball) | Server deployments where you manage installation and data directories |
| [Docker](#linux-docker) | Development and test environments using containers |

Complete [Pre-Installation Preparation](../pre-install-preparation/) before tarball installation.
For Docker, prepare Docker Engine and the necessary volume and port permissions.

<a id="linux-preparation-environment-linux"></a>

### Linux Preparation

File descriptor limits, clock synchronization, port reservation, and firewall configuration
are shared preparation tasks. Configure them for the server account and operating environment
using [Pre-Installation Preparation](../pre-install-preparation/).

<a id="linux-tarball"></a>

### Tarball Installation

The following procedure extracts a Linux tarball to install Standard Edition.

#### 1. Create an OS User

Create the dedicated server account:

```bash
sudo useradd -m -d /home/machbase machbase
sudo passwd machbase
```

Log in as `machbase` for the remaining steps.

#### 2. Download and Extract the Package

The example assumes that the package is under `/home/machbase/packages/`.
Substitute the actual package name and extract it into a new installation directory without
an existing instance. For an existing installation, follow [Upgrade](../upgrade/).

```bash
machbase_package=/home/machbase/packages/machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz
test -r "$machbase_package" &&
mkdir /home/machbase/machbase_home &&
tar zxf "$machbase_package" -C /home/machbase/machbase_home &&
cd /home/machbase/machbase_home
```

Check the extracted layout:

```bash
ls -l
# bin/  conf/  dbs/  doc/  include/  lib/  trc/  ...
```

#### 3. Set Environment Variables

Add these variables to `~/.bashrc`:

```bash
export MACHBASE_HOME=/home/machbase/machbase_home
export PATH="$MACHBASE_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$MACHBASE_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

Apply them to the current shell:

```bash
source ~/.bashrc
```

#### 4. Create the Database

`machadmin -c` creates the physical instance's database files. It is different from SQL
`CREATE DATABASE`, which adds a logical database. First verify `MACHBASE_HOME`,
`conf/machbase.conf`, and the actual `DBS_PATH`. If a database already exists, inspect the
target path instead of deleting and recreating it.

```bash
machadmin -c
# Database created successfully.
```

#### Check Configuration and Licensing Before Startup

Check `PORT_NO` and `DBS_PATH` in `conf/machbase.conf`. If you use a separate license,
install it by copying the file or using `machadmin -t`, then check it with `machadmin -f`
before starting. See [License Installation](../pre-install-preparation/#license).

#### 5. Start the Server

```bash
machadmin -u
# Machbase server started successfully.
```

Check server state:

```bash
machadmin -e
```

#### 6. Test the Connection

Connect with `machsql`. The initial administrator credentials are `SYS` / `MANAGER`;
use the current password if it has been changed.

```bash
machsql
# Machbase server address (Default:127.0.0.1) :
# Machbase user ID  (Default:SYS)
# Machbase User Password :
# MACHBASE_CONNECT_MODE=INET, PORT=5656 EDITION=STANDARD
# Mach>
```

Run the basic SQL test:

```sql
CREATE LOG TABLE install_check (id INTEGER, val DOUBLE);
INSERT INTO install_check (id, val) VALUES (1, 3.14);
SELECT id, val FROM install_check;
DROP TABLE install_check;
```

Verify one row with `id=1` and `val=3.14`, followed by a successful DROP. If
`install_check` already exists, choose an unused practice name instead of deleting it.

#### Stop the Server

Run this only if you need to stop the server after verification.

```bash
machadmin -s
# Machbase server shut down successfully.
```

#### Change the Port

Change `PORT_NO` in `$MACHBASE_HOME/conf/machbase.conf` or set the environment variable:

```bash
export MACHBASE_PORT_NO=7878
```

Apply the setting while the server is stopped and start it again. This variable affects the
current shell; a service needs the same environment configured separately. Specify the changed
port when connecting, for example `machsql -s 127.0.0.1 -P 7878 -u SYS`.

<a id="linux-docker"></a>

### Docker Installation

Docker packages the server and its execution environment in a container. Even for development
and testing, prepare Docker Engine, storage volumes, ports, and file descriptor limits on the host.

The deployment example uses `machbase/machbase`. If you build your own image, replace it with
the local image name, such as `machbase:latest`.

#### Check the Image

```bash
docker pull machbase/machbase
docker image ls machbase/machbase
```

#### Create the Container

```bash
docker create \
  --name machbase \
  --ulimit nofile=65535 \
  -p 5656:5656 \
  -v /data/machbase:/home/machbase/machbase/dbs \
  machbase/machbase
```

| Option | Meaning |
|---|---|
| `-p 5656:5656` | Host SQL port mapped to container SQL port |
| `--ulimit nofile=65535` | File descriptor limit available to the server |
| `-v /data/machbase:...` | Preserve the data directory on the host |

Data stored only in a container's writable layer is removed with the container. Confirm that
the actual data path is mounted on the volume, and also keep backups against volume deletion
or disk failure.

`docker create` does not start the server yet. The container's server account must be able to
write `/data/machbase`. If it contains existing DB files, verify their version and instance.
Check the image's actual version and `MACHBASE_HOME`, then pin a validated tag or digest for
production. Do not assume the untagged public image always contains 8.7.0.

If you use a separate license, copy it before starting:

```bash
docker cp /path/to/license.dat machbase:/home/machbase/machbase/conf/license.dat
```

Start the prepared container:

```bash
docker start machbase
```

#### Check Container State

```bash
docker ps
docker logs machbase
```

#### Test the Connection

##### machsql Inside the Container

```bash
docker exec -it machbase machsql
# Mach>
```

##### From the Host

If `machsql` is installed on the host:

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

#### Stop and Restart the Container

```bash
docker stop machbase
docker start machbase
```

#### Update the License

Copy the replacement file into the running container and install it with the license command.
Configuration and licensing are separate from the data volume; retain their originals so
that they can be reapplied when recreating a container.

```bash
docker cp /path/to/license.dat machbase:/tmp/license.dat
docker exec machbase machadmin -t /tmp/license.dat
docker exec machbase machadmin -f
```

<a id="windows"></a>

## Windows Installation

### Before You Start

- Check supported Windows versions in the supplied package's release information.
- Match package bit width and CPU architecture to the operating system.

Complete [Windows Preparation](#windows-preparation-environment-windows) first.

### Installation Methods

| Method | Description |
|---|---|
| [Windows Package Installation](#windows-package) | Installation wizard; creates environment variables and shortcuts |

<a id="windows-preparation-environment-windows"></a>

### Windows Preparation

Check firewall configuration before installation.

#### Allow the SQL Port

| Port | Protocol | Purpose |
|---|---|---|
| 5656 | TCP | SQL client connections |

##### Configure Through the UI

1. Open **Control Panel → Windows Defender Firewall → Advanced settings**.
2. Select **Inbound Rules**, then **New Rule**.
3. Choose **Port**, then **Next**.
4. Choose **TCP**, enter `5656` in **Specific local ports**, then **Next**.
5. Choose **Allow the connection**, then **Next**.
6. Select only the network profiles where access is needed: **Domain**, **Private**, or **Public**.
7. Name the rule, for example `Machbase`, and select **Finish**.

Restrict the rule's remote-address scope to the actual clients. If remote access is unnecessary,
you do not need an inbound allow rule.

##### Configure with Administrator PowerShell

The following creates an inbound rule; apply the same profile and address restrictions.

```powershell
New-NetFirewallRule -DisplayName "Machbase SQL" -Direction Inbound -Protocol TCP -LocalPort 5656 -Action Allow
```

#### Visual C++ Redistributable

The runtime requires Visual C++ Redistributable. The installer may handle this dependency.
If it is missing, obtain the appropriate runtime from Microsoft's official site.

<a id="windows-package"></a>

### Windows Package Installation

A ZIP contains `bin\`, `conf\`, `dbs\`, and `trc\` at its root.
The installer creates `machbase_home\` below the installation directory and configures
environment variables and shortcuts.

#### Installation Procedure

1. Download the Windows package.
2. For a ZIP, extract it into the desired installation directory.

   ```cmd
   mkdir C:\machbase
   tar -xf machbase-SDK-8.7.0.official-WINDOWS-X86-64-release.zip -C C:\machbase
   ```

3. If using an installer instead, run it and select **Next**.
4. Select the installation directory. Its default follows the form
   `C:\machbase-<short_version>\`. Change it if needed, then select **Next**.
5. After installation, select **Next → Close**.

#### Initialize a ZIP Installation

In Command Prompt, set the extracted directory as the installation home. This example uses
a new installation at `C:\machbase`. Check the active configuration and license first.
Run `-c` only for a new instance without existing DB files.

```cmd
set "MACHBASE_HOME=C:\machbase"
set "PATH=%MACHBASE_HOME%\bin;%PATH%"
machadmin.exe -c
machadmin.exe -f
machadmin.exe -u
machadmin.exe -e
```

These `set` commands affect the current window. Use the same installation home and executable
path in later windows or services. If an installer already created the database, do not repeat
the ZIP creation command.

#### Start and Stop the Server

An installer provides these desktop or Start-menu shortcuts:

- **start Machbase** runs `machadmin.exe -u`.
- **stop Machbase** runs `machadmin.exe -s`.
- **machsql** opens the SQL console.

#### Connect from Command Prompt

For an installer, `<installation directory>\machbase_home\bin` is added to `PATH`.
For a ZIP, add its `bin\` directory yourself or run the executable by its full path.

```cmd
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

The initial credentials are `SYS` / `MANAGER`.

#### Installation Layout

A ZIP places `bin\`, `conf\`, `dbs\`, and `trc\` directly below the extraction directory.
An installer places the same layout under `machbase_home\`.
See [Package Layout](../pre-install-preparation/#package).
