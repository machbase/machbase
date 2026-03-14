---
title : '수학 함수'
type: docs
weight: 40
---

# 구현된 수학 함수 (Issue 3479)

현재 구현에서 제공되는 수학 함수를 한 번에 보기 쉽게 정리했습니다.

## 함수 목록

|함수|문법|반환 타입|인자|동작|
|---|---|---|---|---|
|PI|`PI()`|`DOUBLE`|인자 없음|원주율 π 상수(`3.141592653589793`)를 반환합니다.|
|SQRT|`SQRT(n)`|`DOUBLE`|숫자 1개|`n`의 제곱근을 반환합니다.|
|POWER|`POWER(base, exponent)`|`DOUBLE`|숫자 2개|`base`의 `exponent` 거듭제곱을 반환합니다.|
|POW|`POW(base, exponent)`|`DOUBLE`|숫자 2개|`POWER`와 동일한 동작입니다.|
|LOG|`LOG(n)`|`DOUBLE`|숫자 1개|자연로그 `ln(n)`을 반환합니다.|
|LOG|`LOG(base, n)`|`DOUBLE`|숫자 2개|로그의 밑과 진수를 받아 `log_base(n)` 값을 반환합니다.|
|LN|`LN(n)`|`DOUBLE`|숫자 1개|자연로그 `ln(n)`을 반환합니다.|
|EXP|`EXP(n)`|`DOUBLE`|숫자 1개|`e^n` 값을 반환합니다.|
|FLOOR|`FLOOR(n)`|`DOUBLE`|숫자 1개|음의 무한대로 내림합니다.|
|CEIL|`CEIL(n)`|`DOUBLE`|숫자 1개|양의 무한대로 올림합니다.|
|SIN|`SIN(radian)`|`DOUBLE`|숫자 1개|라디안 단위 입력의 사인 값을 반환합니다.|
|COS|`COS(radian)`|`DOUBLE`|숫자 1개|라디안 단위 입력의 코사인 값을 반환합니다.|
|TAN|`TAN(radian)`|`DOUBLE`|숫자 1개|라디안 단위 입력의 탄젠트 값을 반환합니다.|
|MOD|`MOD(dividend, divisor)`|`DOUBLE`|숫자 2개|몫을 0 방향으로 절사한 값으로 나머지를 계산합니다.|
|RAND|`RAND()`|`DOUBLE`|인자 없음|[0, 1) 범위의 난수를 반환합니다. 내부 상태를 공유합니다.|
|RAND|`RAND(seed)`|`DOUBLE`|정수 1개|같은 시드면 같은 난수가 나옵니다.|

## 문법 및 사용 시 주의

### PI

```sql
SELECT PI() FROM m$sys_users WHERE name = 'SYS';
```

`DOUBLE`을 반환하며, 인자를 넣으면 오류가 발생합니다.

### SQRT / FLOOR / CEIL / SIN / COS / TAN / LN / EXP

모든 함수는 숫자형 인자 1개만 허용하고 결과는 `DOUBLE`입니다.

```sql
SELECT SQRT(9), FLOOR(3.2), CEIL(-1.2), SIN(PI()/2), LN(2), EXP(2)
FROM m$sys_users WHERE name = 'SYS';
```

### POWER / POW

`POWER`와 `POW`는 완전히 동일한 동작입니다.

```sql
SELECT POWER(3, 4), POW(2, -1) FROM m$sys_users WHERE name = 'SYS';
```

### LOG

* `LOG(n)`은 `LN(n)`과 동일합니다.
* `LOG(base, n)`은 `log_base(n)` 계산입니다.

```sql
SELECT LOG(2, 8), LOG(100) FROM m$sys_users WHERE name = 'SYS';
```

### MOD

음수 입력이 들어오더라도 0 방향으로 절사한 몫을 기준으로 나머지를 계산합니다.

```sql
SELECT MOD(-10, 3), MOD(10, -3), MOD(-10, -3)
FROM m$sys_users WHERE name = 'SYS';
```

### RAND

* `RAND(seed)`는 정수 시드만 허용합니다. 같은 시드는 반복 실행 시 동일한 값입니다.
* `RAND()`는 내부 상태 기반이라 같은 쿼리 안에서 호출할수록 다른 값이 나옵니다.
* 반환 범위는 `[0, 1)` 입니다.

```sql
SELECT RAND(), RAND(), RAND(5), RAND(5), RAND() FROM m$sys_users WHERE name = 'SYS';
```

## 오류 처리

|오류 유형|코드|발생 조건|
|---|---|---|
|인자 타입 오류|`ERR-02036`, `ERR-02037`|숫자 타입이 아닌 값을 넣었거나 `PI`에 인자를 전달한 경우|
|실행 오류|`ERR-02317`|`SQRT`의 음수 입력, `MOD`의 0 나누기, `LOG`의 잘못된 밑/값, `EXP`/`POWER`의 범위 초과 등|

입력이 `NULL`이면 결과도 `NULL`입니다.
