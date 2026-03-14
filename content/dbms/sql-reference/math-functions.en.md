---
title : 'Mathematical Functions'
type: docs
weight: 40
---

# Mathematical Functions

This page summarizes mathematical functions in Machbase.

## Function Matrix

|Function|Syntax|Return type|Arguments|Behavior|
|---|---|---|---|---|
|PI|`PI()`|`DOUBLE`|No arguments|Returns π constant (`3.141592653589793`).|
|SQRT|`SQRT(n)`|`DOUBLE`|1 numeric argument|Returns the square root of `n`.|
|POWER|`POWER(base, exponent)`|`DOUBLE`|2 numeric arguments|Returns `base` raised to `exponent`.|
|POW|`POW(base, exponent)`|`DOUBLE`|2 numeric arguments|Alias of `POWER`.|
|LOG|`LOG(n)`|`DOUBLE`|1 numeric argument|Returns natural logarithm `ln(n)`.|
|LOG|`LOG(base, n)`|`DOUBLE`|2 numeric arguments|Returns logarithm with base and argument, `log_base(n)`.|
|LN|`LN(n)`|`DOUBLE`|1 numeric argument|Returns natural logarithm `ln(n)`.|
|EXP|`EXP(n)`|`DOUBLE`|1 numeric argument|Returns `e^n`.|
|FLOOR|`FLOOR(n)`|`DOUBLE`|1 numeric argument|Rounds down toward negative infinity.|
|CEIL|`CEIL(n)`|`DOUBLE`|1 numeric argument|Rounds up toward positive infinity.|
|SIN|`SIN(radian)`|`DOUBLE`|1 numeric argument|Returns sine (argument is in radians).|
|COS|`COS(radian)`|`DOUBLE`|1 numeric argument|Returns cosine (argument is in radians).|
|TAN|`TAN(radian)`|`DOUBLE`|1 numeric argument|Returns tangent (argument is in radians).|
|MOD|`MOD(dividend, divisor)`|`DOUBLE`|2 numeric arguments|Returns remainder using truncation toward zero of quotient.|
|RAND|`RAND()`|`DOUBLE`|No arguments|Pseudo random in range `[0, 1)`, stateful per session.|
|RAND|`RAND(seed)`|`DOUBLE`|1 integer argument|Deterministic pseudo random in `[0, 1)` for a given seed.|

## Function List

- [PI()](#pi)
- [SQRT()](#sqrt)
- [POWER()](#power)
- [POW()](#pow)
- [LOG()](#log)
- [LN()](#ln)
- [EXP()](#exp)
- [FLOOR()](#floor)
- [CEIL()](#ceil)
- [SIN()](#sin)
- [COS()](#cos)
- [TAN()](#tan)
- [MOD()](#mod)
- [RAND()](#rand)

## PI()

```sql
SELECT PI() FROM m$sys_users WHERE name = 'SYS';
```

Returns a `DOUBLE` value. Passing arguments is not allowed.

## SQRT()

```sql
SELECT SQRT(9)
FROM m$sys_users WHERE name = 'SYS';
```

## FLOOR()

```sql
SELECT FLOOR(3.2), FLOOR(-1.2)
FROM m$sys_users WHERE name = 'SYS';
```

## CEIL()

```sql
SELECT CEIL(3.2), CEIL(-1.2)
FROM m$sys_users WHERE name = 'SYS';
```

## SIN()

```sql
SELECT SIN(PI()/2), SIN(0)
FROM m$sys_users WHERE name = 'SYS';
```

## COS()

```sql
SELECT COS(0), COS(PI())
FROM m$sys_users WHERE name = 'SYS';
```

## TAN()

```sql
SELECT TAN(0), TAN(PI()/4)
FROM m$sys_users WHERE name = 'SYS';
```

## LN()

```sql
SELECT LN(2), LN(10)
FROM m$sys_users WHERE name = 'SYS';
```

## EXP()

```sql
SELECT EXP(2), EXP(-1)
FROM m$sys_users WHERE name = 'SYS';
```

All trigonometric and logarithmic/exponential functions require numeric input and return `DOUBLE`.

```sql
SELECT SQRT(9), LN(2), EXP(2), SIN(PI()/2)
FROM m$sys_users WHERE name = 'SYS';
```

## POWER()

`POWER` and `POW` are identical.

```sql
SELECT POWER(3, 4), POW(2, -1) FROM m$sys_users WHERE name = 'SYS';
```

## POW()

Alias of `POWER()`.

```sql
SELECT POW(2, 3)
FROM m$sys_users WHERE name = 'SYS';
```

## LOG()

* `LOG(n)` is equivalent to `LN(n)`.
* `LOG(base, n)` uses change-of-base: `log_base(n)`.

```sql
SELECT LOG(2, 8), LOG(100) FROM m$sys_users WHERE name = 'SYS';
```

## MOD()

For negative values, quotient truncation uses zero-centered truncation.

```sql
SELECT MOD(-10, 3), MOD(10, -3), MOD(-10, -3)
FROM m$sys_users WHERE name = 'SYS';
```

## RAND()

* `RAND(seed)` requires an integer `seed`. Passing the same seed repeatedly returns the same value.
* `RAND()` uses internal state, so successive calls in one statement return different values.
* Output is `DOUBLE` in `[0, 1)`.

```sql
SELECT RAND(), RAND(), RAND(5), RAND(5), RAND() FROM m$sys_users WHERE name = 'SYS';
```

## Error handling

|Error kind|Error code|Triggered when|
|---|---|---|
|Argument type mismatch|`ERR-02036` / `ERR-02037`|`PI` with arguments, or any numeric-function input is non-numeric.|
|Execution failure|`ERR-02317`|Domain/range error while calculating value, for example negative input to `SQRT`, zero in `MOD` divisor, invalid `LOG` base, or overflow in `EXP`/`POWER`.|

When an argument is `NULL`, the result is `NULL`.
