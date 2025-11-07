---
title: 타이머
type: docs
weight: 80
---

타이머는 특정 시점 혹은 일정 간격으로 실행해야 하는 작업을 정의합니다.

## 새 타이머 추가

지정한 일정에 따라 실행할 작업을 등록합니다. 타이머 관리용 웹 UI는 {{< neo_since ver="8.0.20" />}}부터 제공됩니다.

1. 좌측 메뉴에서 <img src=/neo/timer/img/timer_icon.png style="display:inline; width:32px;"/> 아이콘을 클릭합니다.

2. 좌측 상단의 `+` 아이콘 <img src=/neo/timer/img/timer_icon2.png style="display:inline; height:22px;"/>을 클릭합니다.

3. 타이머 ID(이름), 스케줄(Timer spec), 실행할 TQL 경로를 입력합니다.

{{< figure src="/neo/timer/img/timer_form.png" width="488" >}}

4. “Create” 버튼을 클릭해 타이머를 생성합니다.


## 타이머 시작/중지/삭제

토글 버튼 <img src=/neo/timer/img/timer_toggle.png style="display:inline; height:25px;">을 눌러 시작하고, <img src=/neo/timer/img/timer_toggle_stop.png style="display:inline; height:25px;">을 눌러 중지합니다.

{{< figure src="/neo/timer/img/timer_detail.png" width="738" >}}

## 타이머 스케줄 규격

사용 가능한 스케줄 표현 예시는 다음과 같습니다.

```
0 30 * * * *           Every hour on the half hour
@every 1h30m           Every hour thirty
@daily                 Every day
```

### CRON 표현식

  | 필드 이름    | 필수 여부  | 허용 값         | 특수 문자 |
  | :----------  | :--------: | :-------------  | :------------------------- |
  | Seconds      | Yes        | 0-59            | * / , -                    |
  | Minutes      | Yes        | 0-59            | * / , -                    |
  | Hours        | Yes        | 0-23            | * / , -                    |
  | Day of month | Yes        | 1-31            | * / , - ?                  |
  | Month        | Yes        | 1-12 or JAN-DEC | * / , -                    |
  | Day of week  | Yes        | 0-6 or SUN-SAT  | * / , - ?                  |

- Asterisk `*`<br/>
  해당 필드의 모든 값을 의미합니다.  
  예: 5번째 필드(월)에 `*`를 사용하면 매월을 의미합니다.

- Slash `/`<br/>
  범위 내 간격을 나타냅니다. 예를 들어 1번째 필드(분)에 `3-59/15`를 사용하면 매 시간 3분부터 15분 간격으로 실행됩니다.  
  `*/...`는 해당 필드의 전체 범위에서 일정 간격을 의미합니다. `N/...`는 `N-MAX/...`와 동일하게 해석됩니다.

- Comma `,`<br/>
  여러 값을 지정할 때 사용합니다. 예: 5번째 필드(요일)에 `MON,WED,FRI`를 입력하면 월/수/금에 실행됩니다.

- Hyphen `-`<br/>
  범위를 지정합니다. 예: `9-17`은 오전 9시부터 오후 5시까지 매시간을 의미합니다.

- Question mark `?`<br/>
  일(day-of-month) 또는 요일(day-of-week) 필드를 비워 둘 때 `*` 대신 사용할 수 있습니다.

### 미리 정의된 스케줄

  |Entry                  | Description                                | Equivalent To |
  |:-----                 | :-----------                               | :------------ |
  |@yearly (or @annually) | Run once a year, midnight, Jan. 1st        | 0 0 0 1 1 *   |
  |@monthly               | Run once a month, midnight, first of month | 0 0 0 1 * *   |
  |@weekly                | Run once a week, midnight between Sat/Sun  | 0 0 0 * * 0   |
  |@daily (or @midnight)  | Run once a day, midnight                   | 0 0 0 * * *   |
  |@hourly                | Run once an hour, beginning of hour        | 0 0 * * * *   |

### 간격 지정

`@every <duration>` 구문을 사용합니다. duration은 `300ms`, `-1.5h`, `2h45m`처럼 부호와 소수, 단위를 포함할 수 있으며 사용 가능한 단위는 `ms`, `s`, `m`, `h`입니다.

```
@every 10h
@every 1h10m30s
```

## 명령줄

**타이머 추가**

*Syntax:* `timer add [--autostart] <name> <timer_spec> <tql-path>`

- `--autostart` : machbase-neo 시작 시 자동으로 실행합니다.  
  자동 시작을 사용하지 않는 경우 `timer start <name>`, `timer stop <name>` 명령으로 수동 제어합니다.
- `<name>` : 타이머 이름  
- `<timer_spec>` : 실행 일정 (위 스케줄 참조)  
- `<tql-path>` : 수행할 TQL 스크립트 경로

**타이머 목록**

*Syntax:* `timer list`

**타이머 시작/중지**

*Syntax:* `timer [start | stop] <name>`

**타이머 삭제**

*Syntax:* `timer del <name>`


## Hello World 예제

타이머의 기본 동작을 확인해 보겠습니다.

### “Hello World” TQL 작성

TQL 에디터를 열어 아래 코드를 입력하고 `helloworld.tql`로 저장합니다.

```js
CSV(`helloworld,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, random())
INSERT("name", "time", "value", table("example"))
```

스크립트를 실행하면 EXAMPLE 테이블에 한 건의 데이터가 입력됩니다.  
쿼리로 결과를 확인해 보십시오.

```sql
select * from example where name = 'helloworld';
```

```
sys machbase-neo» select * from example where name = 'helloworld';
┌────────┬────────────┬─────────────────────────┬────────────────────┐
│ ROWNUM │ NAME       │ TIME(LOCAL)             │ VALUE              │
├────────┼────────────┼─────────────────────────┼────────────────────┤
│      1 │ helloworld │ 2024-06-19 18:20:07.001 │ 0.6132387755535856 │
└────────┴────────────┴─────────────────────────┴────────────────────┘
a row fetched.
```

### 타이머 등록

웹 UI(8.0.20 도입)에서의 설정은 아래 셸 명령과 동일한 효과를 냅니다.

{{< figure src="/neo/timer/img/timer_new.jpg" width="630px" >}}

아래 명령과 동일합니다.

```
timer add helloworld "@every 5s" helloworld.tql; 
```

“Auto Start” 옵션을 선택하거나 <img src=/neo/timer/img/timer_toggle.png style="display:inline; height:25px;"> 버튼을 눌러 타이머를 시작합니다.  
시작과 동시에 5초마다 새로운 레코드가 테이블에 삽입됩니다.

**타이머 실행 결과 확인**

```
sys machbase-neo» select * from example where name = 'helloworld';
┌────────┬────────────┬─────────────────────────┬─────────────────────┐
│ ROWNUM │ NAME       │ TIME(LOCAL)             │ VALUE               │
├────────┼────────────┼─────────────────────────┼─────────────────────┤
│      1 │ helloworld │ 2024-07-03 09:49:47.002 │ 0.14047743934840562 │
│      2 │ helloworld │ 2024-07-03 09:49:42.002 │ 0.7656153597963373  │
│      3 │ helloworld │ 2024-07-03 09:49:37.002 │ 0.11713331640146182 │
│      4 │ helloworld │ 2024-07-03 09:49:32.002 │ 0.5351642943247759  │
│      5 │ helloworld │ 2024-07-03 09:49:27.001 │ 0.6588127185612987  │
└────────┴────────────┴─────────────────────────┴─────────────────────┘
5 rows fetched.
```

**대시보드**

자동 새로 고침 기능을 갖춘 대시보드를 만들면 타이머가 정상적으로 동작하는지 실시간으로 확인할 수 있습니다.

{{< figure src="/neo/timer/img/helloworld-dsh-form.png" width="700px" >}}

### 타이머 관리

상세 페이지에서 수정·시작·중지·삭제 작업을 수행할 수 있습니다.

{{< figure src="/neo/timer/img/timer_status.png" width="775px" >}}


**명령줄**

The command `timer list` shows the status of timers.

```
sys machbase-neo» timer list;
┌────────────┬───────────┬────────────────┬───────────┬─────────┐
│ NAME       │ SPEC      │ TQL            │ AUTOSTART │ STATE   │
├────────────┼───────────┼────────────────┼───────────┼─────────┤
│ HELLOWORLD │ @every 5s │ helloworld.tql │ false     │ RUNNING │
└────────────┴───────────┴────────────────┴───────────┴─────────┘
```

Also it is possible to start, stop the timer from the command line.

```
timer start helloworld;
```

```
timer stop helloworld;
```
