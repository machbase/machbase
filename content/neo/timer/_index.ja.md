---
toc: true
title: タイマー
type: docs
weight: 80
---

タイマーは、指定した時刻または一定の間隔で実行する処理を定義します。

## 新しいタイマーの追加 {#새-타이머-추가}

指定したスケジュールで実行する処理を登録します。タイマー管理のWeb UIは、{{< neo_since ver="8.0.20" />}}から利用できます。

1. 左側のメニューで<img src=/neo/timer/img/timer_icon.png style="display:inline; width:32px;"/>アイコンをクリックします。

2. 左上の`+`アイコン<img src=/neo/timer/img/timer_icon2.png style="display:inline; height:22px;"/>をクリックします。

3. タイマーID（名前）、スケジュール（Timer spec）、実行するTQLのパスを入力します。

{{< figure src="/neo/timer/img/timer_form.png" width="488" >}}

4. 「Create」ボタンをクリックしてタイマーを作成します。


## タイマーの開始・停止・削除 {#타이머-시작중지삭제}

トグルボタン<img src=/neo/timer/img/timer_toggle.png style="display:inline; height:25px;">を押して開始し、<img src=/neo/timer/img/timer_toggle_stop.png style="display:inline; height:25px;">を押して停止します。

{{< figure src="/neo/timer/img/timer_detail.png" width="738" >}}

## タイマーのスケジュール仕様 {#타이머-스케줄-규격}

使用できるスケジュール表現の例は以下のとおりです。

```
0 30 * * * *           毎時30分に実行
@every 1h30m           1時間30分ごとに実行
@daily                 毎日実行
```

### CRON式 {#cron-표현식}

  | フィールド名    | 必須かどうか  | 使用できる値         | 特殊文字 |
  | :----------  | :--------: | :-------------  | :------------------------- |
  | 秒      | 必須        | 0-59            | * / , -                    |
  | 分      | 必須        | 0-59            | * / , -                    |
  | 時        | 必須        | 0-23            | * / , -                    |
  | 日 | 必須        | 1-31            | * / , - ?                  |
  | 月        | 必須        | 1-12またはJAN-DEC | * / , -                    |
  | 曜日  | 必須        | 0-6またはSUN-SAT  | * / , - ?                  |

- アスタリスク `*`<br/>
  対応するフィールドのすべての値を表します。  
  例：第5フィールド（月）に`*`を指定すると、毎月を表します。

- スラッシュ `/`<br/>
  範囲内の間隔を表します。たとえば、第2フィールド（分）に`3-59/15`を指定すると、毎時3分から15分間隔で実行します。  
  `*/...`は、`first-last/...`と同じで、そのフィールドの全範囲を一定間隔で扱います。`N/...`は`N-MAX/...`と同じで、Nから範囲の末尾までを指定間隔で扱い、先頭には戻りません。

- カンマ `,`<br/>
  複数の値を指定します。例：第6フィールド（曜日）に`MON,WED,FRI`を指定すると、月・水・金曜日に実行します。

- ハイフン `-`<br/>
  範囲を指定します。例：`9-17`は、午前9時から午後5時まで、両端を含む毎時を表します。

- 疑問符 `?`<br/>
  日（day-of-month）または曜日（day-of-week）のフィールドを空にする場合、`*`の代わりに使用できます。

### 定義済みスケジュール {#미리-정의된-스케줄}

  |項目                  | 説明                                | 等価な式 |
  |:-----                 | :-----------                               | :------------ |
  |@yearly （または@annually） | 毎年1月1日の午前0時に実行        | 0 0 0 1 1 *   |
  |@monthly               | 毎月1日の午前0時に実行 | 0 0 0 1 * *   |
  |@weekly                | 毎週日曜日の午前0時に実行  | 0 0 0 * * 0   |
  |@daily （または@midnight）  | 毎日午前0時に実行                   | 0 0 0 * * *   |
  |@hourly                | 毎時0分に実行        | 0 0 * * * *   |

### 間隔の指定 {#간격-지정}

`@every <duration>`構文を使用します。durationは、`300ms`、`-1.5h`、`2h45m`のように符号、小数、単位を含められます。使用できる単位は`ms`、`s`、`m`、`h`です。

```
@every 10h
@every 1h10m30s
```

## コマンドライン {#명령줄}

**タイマーの追加**

*構文：* `timer add [--autostart] <name> <timer_spec> <tql-path>`

- `--autostart` : machbase-neoの起動時に自動的に実行します。  
  自動起動を使用しない場合は、`timer start <name>`と`timer stop <name>`で手動操作します。
- `<name>` : タイマー名  
- `<timer_spec>` : 実行スケジュール（前述のスケジュールを参照）  
- `<tql-path>` : 実行するTQLスクリプトのパス

**タイマー一覧**

*構文：* `timer list`

**タイマーの開始・停止**

*構文：* `timer [start | stop] <name>`

**タイマーの削除**

*構文：* `timer del <name>`


## Hello Worldの例 {#hello-world-예제}

タイマーの基本動作を確認します。

### 「Hello World」TQLの作成 {#hello-world-tql-작성}

TQLエディターを開き、以下のコードを入力して`helloworld.tql`として保存します。

```js
CSV(`helloworld,0,0`)
MAPVALUE(1, time('now'))
MAPVALUE(2, random())
INSERT("name", "time", "value", table("example"))
```

スクリプトを実行すると、EXAMPLEテーブルに1件のデータが挿入されます。  
クエリで結果を確認してください。

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

### タイマーの登録 {#타이머-등록}

Web UI（8.0.20で導入）の設定は、以下のシェルコマンドと同じ動作になります。

{{< figure src="/neo/timer/img/timer_new.jpg" width="630px" >}}

以下のコマンドと同じです。

```
timer add helloworld "@every 5s" helloworld.tql; 
```

「Auto Start」オプションを選択するか、<img src=/neo/timer/img/timer_toggle.png style="display:inline; height:25px;">ボタンを押してタイマーを開始します。  
開始すると、5秒ごとに新しいレコードがテーブルに挿入されます。

**タイマーの実行結果の確認**

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

**ダッシュボード**

自動更新するダッシュボードを作成すると、タイマーが正常に動作しているかをリアルタイムに確認できます。

{{< figure src="/neo/timer/img/helloworld-dsh-form.png" width="700px" >}}

### タイマーの管理 {#타이머-관리}

詳細ページで、変更・開始・停止・削除を行えます。

{{< figure src="/neo/timer/img/timer_status.png" width="775px" >}}


**コマンドライン**

`timer list`コマンドは、タイマーの状態を表示します。

```
sys machbase-neo» timer list;
┌────────────┬───────────┬────────────────┬───────────┬─────────┐
│ NAME       │ SPEC      │ TQL            │ AUTOSTART │ STATE   │
├────────────┼───────────┼────────────────┼───────────┼─────────┤
│ HELLOWORLD │ @every 5s │ helloworld.tql │ false     │ RUNNING │
└────────────┴───────────┴────────────────┴───────────┴─────────┘
```

コマンドラインからタイマーを開始・停止することもできます。

```
timer start helloworld;
```

```
timer stop helloworld;
```
