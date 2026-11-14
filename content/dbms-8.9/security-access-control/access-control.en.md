---
type: docs
title: '14.5 Access Control'
weight: 50
toc: true
---

Restrict network access with `GRANT_REMOTE_ACCESS`, `BIND_IP_ADDRESS`, and OS or cloud
firewalls together. Check current values as follows.

```sql
SELECT NAME, VALUE
  FROM V$PROPERTY
 WHERE NAME IN ('GRANT_REMOTE_ACCESS', 'BIND_IP_ADDRESS');
```

Listener settings take effect at server startup. Do not assume a running listener automatically
rebinds. Change `machbase.conf`, then follow the approved restart procedure.

<a id="remote-access-configuration"></a>

## Configure remote access

`GRANT_REMOTE_ACCESS` controls whether remote clients can connect.

```ini
# Allow remote access
GRANT_REMOTE_ACCESS = 1

# Block remote access
GRANT_REMOTE_ACCESS = 0
```

Before changing the value, check:

1. Connection origins for application, monitoring, and backup clients.
2. How to retain local administrative access.
3. The procedure for testing remote and emergency access after restart.

Configure a firewall allowlist alongside `GRANT_REMOTE_ACCESS=1` so enabling remote access
does not admit every remote address.

<a id="network-exposure-bind-ip-address"></a>

## BIND_IP_ADDRESS and network exposure

`BIND_IP_ADDRESS` specifies the address for the IPv4 listener.

```ini
# All IPv4 interfaces
BIND_IP_ADDRESS = 0.0.0.0

# Local IPv4 interface
BIND_IP_ADDRESS = 127.0.0.1

# Specified internal IPv4 interface
BIND_IP_ADDRESS = 10.0.0.5
```

An address that does not exist on the server can prevent startup. Check current interface
addresses before changing the setting. After restart, use OS tools to verify the actual
listening address and port.

If `0.0.0.0` is required, restrict allowed source addresses and ports in the firewall or
security group. Firewall commands depend on the deployed OS and network policy; do not
blindly apply fixed commands from this manual.
