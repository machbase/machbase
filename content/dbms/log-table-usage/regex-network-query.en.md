---
type: docs
title: '7.12 Network Type Queries'
weight: 120
toc: true
---

Storing IP addresses as strings is readable, but can lead to the mistaken assumption that lexical
order matches address-range order. Use IPV4/IPV6 types for address comparison, and retain a separate
string only when the original notation is also required.

<a id="design-type-network-data-types"></a>

<a id="범위의-양-끝과-null을-함께-준비합니다"></a>

## Prepare Network Data

```sql
CREATE LOG TABLE ch7_network (
    event_id INTEGER,
    src_ip   IPV4,
    dst_ip   IPV6,
    dst_port INTEGER
);
INSERT INTO ch7_network VALUES (1, '192.0.2.1',   '2001:db8::1', 80);
INSERT INTO ch7_network VALUES (2, '192.0.2.255', '2001:db8::2', 65535);
INSERT INTO ch7_network VALUES (3, '198.51.100.1', '2001:db8::3', 443);
INSERT INTO ch7_network VALUES (4, NULL, NULL, NULL);

SELECT event_id, src_ip, dst_ip, dst_port FROM ch7_network ORDER BY event_id;
```

The query returns four rows. Ports use INTEGER because USHORT reserves its maximum value, 65535, for
NULL and cannot represent the full port range.

<a id="동등-비교와-범위-조회를-구분합니다"></a>

## Equality and Range Queries

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip BETWEEN '192.0.2.1' AND '192.0.2.255'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IN ('192.0.2.1', '198.51.100.1')
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip = '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip BETWEEN '2001:db8::1' AND '2001:db8::2'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip IS NULL
 ORDER BY event_id;
```

| Predicate | Selected event_id values |
|---|---|
| IPv4 BETWEEN | 1, 2 |
| IPv4 IN | 1, 3 |
| IPv6 equality | 2 |
| IPv6 BETWEEN | 1, 2 |
| IPv4 IS NULL | 4 |

BETWEEN includes both endpoint addresses. The IPv4 range here is explicitly bounded by two
addresses; it does not automatically apply CIDR semantics. Use `CONTAINED` below to test network
membership. Test NULL with `IS NULL`, not `= NULL`.

<a id="cidr-대역으로-판정합니다"></a>

## Testing CIDR Network Membership

Use `CONTAINED` to test whether an address belongs to a network. Specify the network as
`address/prefix`. Both IPv4 and IPv6 are supported.

```sql
SELECT event_id FROM ch7_network
 WHERE src_ip CONTAINED '192.0.2.0/24'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE dst_ip CONTAINED '2001:db8::/32'
 ORDER BY event_id;

SELECT event_id FROM ch7_network
 WHERE src_ip NOT CONTAINED '192.0.2.0/24'
 ORDER BY event_id;
```

| Predicate | Selected event_id values |
|---|---|
| IPv4 `CONTAINED '192.0.2.0/24'` | 1, 2 |
| IPv6 `CONTAINED '2001:db8::/32'` | 1, 2, 3 |
| IPv4 `NOT CONTAINED '192.0.2.0/24'` | 3 |

The reversed form `'192.0.2.0/24' CONTAINS src_ip` has the same meaning. `CONTAINS` places the
network on the left and the address on the right; `CONTAINED` does the reverse.

Omitting the prefix, as in `CONTAINED '192.0.2.0'`, causes an error because the value cannot be
interpreted as a network. Row 4 has a NULL address and matches none of these predicates. Add a
separate `IS NULL` predicate when counting uncollected addresses.

<a id="혼합-주소와-원본-표기-정책을-먼저-정하세요"></a>

## Address Formats and Preserving Source Notation

Use IPV4 when input contains only IPv4 addresses and IPV6 for IPv6 addresses. If both are handled,
define input-conversion and column-separation policies first and validate them with real samples. Do
not assume implicit conversion always normalizes source addresses as intended.

Pay attention to output strings. The same IPv6 address may be displayed differently from its
compressed source notation. If the original notation must be retained as evidence, store the typed
address and raw string in separate columns.

For large datasets, limit the `_arrival_time` range together with address predicates and inspect the
execution plan. For message regular expressions, see
[Text Search](../text-search-keyword-index/#regex) and the
[SQL Function Dictionary](/dbms/reference/sql/functions/).

```sql
DROP TABLE ch7_network;
```

If an address query returns unexpected results, compare the source string, input type, and both
range endpoints. This helps distinguish notation differences from actual address-range differences.
