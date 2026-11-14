---
type: docs
title: '3.1 Pre-Installation Preparation'
weight: 10
toc: true
---

Preparation establishes not only where to copy the software, but also where data will remain,
which account will run the server, and how clients will connect. Check package and operating
system compatibility, then prepare storage, networking, and licensing. Use the supplied release
information and support policy to determine supported configurations.

## Deployment Information to Decide First

| Item | Decision | Why it matters |
|---|---|---|
| Edition and version | Standard or Cluster, server and SDK versions | Select supported SQL features and deployment methods |
| OS account | Server account and file owner | Align access to configuration, data, and log directories |
| Installation home | Absolute path containing executables and configuration | Identify the instance controlled by administration commands |
| Data path | Actual `DBS_PATH`, file system, and free space | Identify data to preserve across restarts and upgrades |
| Connection details | Server address, SQL and management ports, allowed clients | Prevent port conflicts and connections to the wrong instance |
| Recovery and licensing | Backup storage, restoration procedure, and license | Establish recovery and operating limits |

The OS account `machbase` and database user `SYS` are different identities. The former controls
processes and file access; the latter controls SQL connections and database permissions.
A server can start successfully while loading or backup still fails because of file or SQL permissions.

| Topic | Contents |
|---|---|
| [Requirements](#pre-install-requirements) | OS compatibility, resources, and network ports |
| [Package Layout](#package) | Package naming, directories, and executables |
| [License Installation](#license) | Installing license.dat and checking its state |

<a id="pre-install-requirements"></a>

## Pre-Installation Requirements

### Operating System and Package

Match the operating system and CPU architecture to the package. Supported OS releases and
minimum versions can change between releases; check the release information supplied with the
package instead of relying on a fixed version list.

### System Resources

CPU, memory, disk, and network requirements depend on ingestion rate, retention, indexes, and
ROLLUP. Include raw data, backups, and operational headroom as well as installation space, and
validate capacity and throughput with representative workloads.

Estimate raw row counts from the ingestion rate and retention period, then load representative
data to measure row size, compression, and index costs. Include replica storage for Cluster.
Separate directories on the same disk are neither independent failure domains nor independent
I/O devices.

### Default Port

| Port | Purpose |
|---|---|
| **5656** | SQL client connections over native TCP |

Set `PORT_NO` in `$MACHBASE_HOME/conf/machbase.conf` to change the SQL port.
The `MACHBASE_PORT_NO` environment variable is also used, so inspect the environment of the
shell or service that starts the server. Specify the new port in clients too. A changed
environment variable does not retroactively modify a running server.

Allow the required incoming connections through the firewall. Cluster also requires ports for
Coordinator links and administration, Brokers, Warehouses, and Deployers.

### Linux Kernel and Process Settings

Check the following before installation.

#### File Descriptor Limit

A low file descriptor limit can constrain workloads that open many files. Defaults depend on
the OS and account configuration; check the account that will run the server.

```bash
# Check the current limit
ulimit -Sn
```

This example uses 65535. If the current limit is lower, update `/etc/security/limits.conf`
and verify the result in a new login session.

```
*  hard  nofile  65535
*  soft  nofile  65535
```

Log in again as the server account. If a service manager starts the server, also check the
limit configured for that service.

```bash
ulimit -Sn
# Expected output: 65535
```

#### Port Reservation

Reserve Machbase service ports so the OS does not select them automatically as ephemeral ports.
This does not prevent another process from explicitly binding the same port.

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5656
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

Merge existing reserved ports rather than overwriting them. For persistence, merge the required
values into `net.ipv4.ip_local_reserved_ports` in `/etc/sysctl.conf`.

```
net.ipv4.ip_local_reserved_ports = 5656
```

### Time Synchronization

Use NTP or `chrony` to synchronize system clocks. Accurate time matters for time-series data,
and clocks across Cluster nodes must be synchronized.

```bash
# Check the time zone
ls -l /etc/localtime
date
```

<a id="package"></a>

## Package Layout

### Package Naming

Package names follow this pattern, with Edition-specific values.

```
machbase-EDITION-VERSION-OS-CPU-BIT-MODE.EXT
```

| Field | Meaning | Example |
|---|---|---|
| EDITION | Edition identifier | `SDK`, `cluster` |
| VERSION | Major.Minor.Fix.AUX | `8.7.0.official` |
| OS | Operating system | `LINUX`, `WINDOWS` |
| CPU | CPU architecture | `X86` |
| BIT | Architecture bit width | `64` |
| MODE | Build mode | `release` |
| EXT | File extension | `tgz` for Linux; `zip` or an installer for Windows |

The Standard Edition Linux archive uses the name `machbase-SDK-...tgz`.

- Standard: `machbase-SDK-8.7.0.official-LINUX-X86-64-release.tgz`
- Cluster: `machbase-cluster-8.7.0.official-LINUX-X86-64-release.tgz`

Different minor versions may differ in DB file or protocol compatibility. Check the destination
release's compatibility guidance and the [Upgrade Procedure](../upgrade/) for supported paths,
including fix-version changes.

### Installation Directories

Extracting the archive creates the following layout under `$MACHBASE_HOME`.

```text
$MACHBASE_HOME/
├── bin/        Executables
├── conf/       Configuration, including machbase.conf
├── dbs/        Data storage
├── doc/        License documents
├── include/    C/C++ headers
├── install/    Makefile include files
├── lib/        Shared libraries
├── package/    Additional Cluster packages
├── sample/     Examples
├── trc/        Server trace logs
├── tutorials/  Tutorials
├── utility/    Utilities
└── 3rd-party/  Grafana plugins and other integrations
```

### Main Executables

| Executable | Purpose |
|---|---|
| `machbased` | Server daemon |
| `machadmin` | Server start, stop, and database creation |
| `machsql` | SQL command-line client |
| `machloader` | Bulk file loading and export |
| `csvimport` | CSV import |
| `csvexport` | CSV export |
| `tagmetaimport` | Bulk TAG metadata registration |

Cluster packages also contain administration tools such as `machcoordinatoradmin` and
`machdeployeradmin`. `machclusterctl` is available in packages built to include it.

### Configuration Files

Edition-specific sample files are under `$MACHBASE_HOME/conf/`.

```bash
ls $MACHBASE_HOME/conf/
# machbase.conf
# machbase.conf.sample.standard
# machbase.conf.sample.edge
# machloader.conf.sample
```

The active configuration file is `machbase.conf`. The full Standard package includes a copy of
`machbase.conf.sample.standard` as `machbase.conf`. If your package does not include the active
file, copy the sample for the appropriate Edition and configure it.

Standard/Edge samples include `TRANSACTION_BUSY_TIMEOUT_MS`, `TRANSACTION_SYNCHRONOUS`, and
`TRANSACTION_JOURNAL_MODE` for TRANSACTION write contention and durability. Start with the
defaults, then evaluate concurrent writes and durability requirements before changing them.

<a id="license"></a>

## License Installation

Without a license file, the server uses the default `COMMUNITY` license information. Before
installation, confirm that its limits fit the planned features and capacity. If you need a
separate license, prepare it before the first startup. Successful startup alone does not
establish that the license meets production requirements.

### Check License State

Use `VIOLATE_STATUS` and `VIOLATE_MSG` in `V$LICENSE_INFO` to inspect the installed license
and any limit violations. Do not edit the license file's contents.

### Installation Methods

#### Method 1: Copy the File Before Startup

Copy `license.dat` to `$MACHBASE_HOME/conf/`. The server reads it when starting.

```bash
cp license.dat $MACHBASE_HOME/conf/license.dat
```

#### Method 2: Use machadmin

`machadmin` validates and installs the file. If the server is running, it also requests a
license reload.

```bash
machadmin -t /path/to/license.dat
```

#### Method 3: Use SQL on a Running Server

Run the following in `machsql`. The server process must be able to read the specified file.

```sql
ALTER SYSTEM INSTALL LICENSE = '/path/to/license.dat';
```

### Verify Installation

#### machadmin

```bash
machadmin -f
```

#### V$LICENSE_INFO

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```

Check that `VIOLATE_STATUS` is zero. You can also inspect license information in `machsql`:

```sql
SHOW LICENSE;
```
