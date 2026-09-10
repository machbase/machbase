---
toc: true
title: gRPC クライアント
type: docs
weight: 200
draft: true
---

## 概要 {#개요}

`machrpc`パッケージは、machbase-neoサーバーに接続・操作するための標準的なGoデータベースインターフェースを提供します。gRPCに基づき、Goの`database/sql`の規則との互換性を維持しながら、高性能な接続を提供します。

標準のGo `database/sql`インターフェースについては、**SQLドライバー**を参照してください。

## インストール {#설치}

Goプロジェクトでmachbase-neo SQLドライバーを使用するには、以下のパッケージをインストールします。

```sh
go get github.com/machbase/neo-server/v8
```

## TLS設定 {#tls-설정}

このgRPCベースのドライバーでクライアントとサーバー間の安全な通信を行うには、**TLS証明書が必要**です。以下の証明書ファイルを用意してください。

- **サーバー証明書**（`server-cert.pem`）：サーバーの公開証明書
- **クライアント証明書**（`client-cert.pem`）：クライアントの公開証明書
- **クライアントキー**（`client-key.pem`）：クライアントの秘密鍵

### 証明書の生成 {#인증서-생성}

ドライバーに必要なTLS証明書（`server-cert.pem`、`client-cert.pem`、`client-key.pem`）の生成手順は、[APIセキュリティ](/neo/security/)を参照してください。CAの作成と証明書の署名方法を説明しています。

## 基本的な使用方法 {#기본-사용법}

### 接続設定 {#연결-설정}

```go {linenos=table,hl_lines=["20-27",31,35,39]}
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/machbase/neo-server/v8/api"
	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	// サーバーアドレスとTLS証明書を設定
	serverAddr := "127.0.0.1:5655"
	serverCert := "/path/to/server-cert.pem"
	clientKey := "/path/to/client-key.pem"
	clientCert := "/path/to/client-cert.pem"

	// 新しいgRPCクライアントを作成
	cli, err := machrpc.NewClient(&machrpc.Config{
		ServerAddr: serverAddr,
		Tls: &machrpc.TlsConfig{
			ClientKey:  clientKey,
			ClientCert: clientCert,
			ServerCert: serverCert,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	// 認証付きで接続
	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	fmt.Println("Successfully connected to machbase-neo")
}
```

### 設定オプション {#설정-옵션}

`machrpc.Config`構造体は、以下のオプションを受け取ります。

| フィールド | 型 | 説明 |
|-------|------|-------------|
| `ServerAddr` | string | `host:port`形式のサーバーアドレス（既定値：`127.0.0.1:5655`） |
| `Tls` | *TlsConfig | 安全な通信のためのTLS設定 |

`machrpc.TlsConfig`構造体：

| フィールド | 型 | 説明 |
|-------|------|-------------|
| `ServerCert` | string | サーバー証明書ファイルのパス |
| `ClientCert` | string | クライアント証明書ファイルのパス |
| `ClientKey` | string | クライアント秘密鍵ファイルのパス |

## データの検索 {#데이터-조회}

### 簡単なSELECTクエリ {#간단한-select-쿼리}

```go {linenos=table,hl_lines=[41,45,48,53]}
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/machbase/neo-server/v8/api"
	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	serverAddr := "127.0.0.1:5655"
	serverCert := "/path/to/server-cert.pem"
	clientKey := "/path/to/client-key.pem"
	clientCert := "/path/to/client-cert.pem"

	cli, err := machrpc.NewClient(&machrpc.Config{
		ServerAddr: serverAddr,
		Tls: &machrpc.TlsConfig{
			ClientKey:  clientKey,
			ClientCert: clientCert,
			ServerCert: serverCert,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	// パラメーター付きのクエリを実行
	sqlText := `SELECT name, time, value FROM example LIMIT ?`
	rows, err := conn.Query(ctx, sqlText, 3)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// 結果を反復処理
	for rows.Next() {
		var name string
		var ts time.Time
		var value float64
		
		err = rows.Scan(&name, &ts, &value)
		if err != nil {
			log.Fatal(err)
		}
		
		fmt.Printf("Name: %s, Time: %s, Value: %.2f\n", 
			name, ts.Format(time.RFC3339), value)
	}

	// 反復処理中のエラーを確認
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
}
```

### パラメーター化クエリ {#파라미터화된-쿼리}

SQLインジェクションを防ぐため、常にパラメーター化クエリを使用してください。

```go {linenos=table}
// 適切：パラメーターを使用
rows, err := conn.Query(ctx, 
	"SELECT * FROM sensors WHERE name = ? AND time > ?", 
	"sensor1", startTime)

// 不適切：文字列を連結（SQLインジェクションの危険あり）
// rows, err := conn.Query(ctx, 
//     fmt.Sprintf("SELECT * FROM sensors WHERE name = '%s'", userInput))
```

## コマンドの実行 {#명령-실행}

### INSERT文 {#insert-문}

```go {linenos=table}
func insertData(conn api.Conn) error {
	ctx := context.Background()

	sqlText := `INSERT INTO example (name, time, value) VALUES (?, ?, ?)`
	result := conn.Exec(ctx, sqlText, "sensor1", time.Now(), 123.45)
	if err := result.Err(); err != nil {
		return err
	}
	rowsAffected := result.RowsAffected()
	fmt.Printf("Inserted %d row(s)\n", rowsAffected)

	return nil
}
```

### DELETE文 {#delete-문}

```go {linenos=table}
func deleteData(conn api.Conn) error {
	ctx := context.Background()

	sqlText := `DELETE FROM example WHERE name = ?`
	result := conn.Exec(ctx, sqlText, "sensor1")
	if err := result.Err(); err != nil {
		return err
	}

	rowsAffected := result.RowsAffected()
	fmt.Printf("Deleted %d row(s)\n", rowsAffected)

	return nil
}
```

## 高性能な一括挿入 (Appender) {#고성능-대량-삽입-appender}

大量のデータ挿入には、`Appender`インターフェースを使用してください。時系列データの取り込みに最適な性能を提供します。

```go
// 重要：Appender専用の接続を使用してください
// 使用中のAppenderがある接続を他の処理に使用しないでください

apd, err := conn.Appender(ctx, "example")
if err != nil {
	panic(err)
}
defer apd.Close() // 残りのデータをフラッシュするため、必ずAppenderを閉じてください

// 高速な一括挿入
for i := range 10_000 {
	err := apd.Append("grpc", time.Now(), 1.23*float64(i))
	if err != nil {
		panic(err)
	}
}
```

{{< callout type="warning" >}}
**接続の分離**：使用中のAppenderがある接続を、他のデータベース操作に使用しないでください。append専用の接続を作成してください。
{{< /callout >}}

{{< callout type="tip" >}}
**性能**：Appenderは時系列ワークロード向けに設計されており、適切なバッチ処理により毎秒数十万件の挿入を達成できます。
{{< /callout >}}

## 推奨事項 {#모범-사례}

**1. 常にContextを使用する**

適切なタイムアウトと取り消し処理のため、すべての操作にcontextを渡してください。

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

rows, err := conn.Query(ctx, "SELECT * FROM large_table")
```

**2. リソースを閉じる**

接続、ステートメント、結果セットを必ず閉じてください。

```go
defer cli.Close()
defer conn.Close()
defer rows.Close()
```

**3. エラーを適切に処理する**

エラーを無視せず、デバッグしやすいように状況を示す情報とともにラップしてください。

```go
if err != nil {
	return fmt.Errorf("failed to query sensor data: %w", err)
}
```

**4. 本番環境で接続プールを使用する**

接続を再利用して、オーバーヘッドを減らし、性能を向上させます。

```go {linenos=table}
type ConnectionPool struct {
	mu      sync.Mutex
	client  *machrpc.Client
	maxSize int
	conns   []api.Conn
	config  *machrpc.Config
}

func NewConnectionPool(config *machrpc.Config, maxSize int) *ConnectionPool {
	return &ConnectionPool{
		conns:   make([]api.Conn, 0, maxSize),
		config:  config,
		maxSize: maxSize,
	}
}

func (p *ConnectionPool) Close() {
	p.mu.Lock()
	defer p.mu.Unlock()
	for _, conn := range p.conns {
		conn.Close()
	}
	p.client.Close()
}

func (p *ConnectionPool) GetConnection(ctx context.Context) (api.Conn, error) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if len(p.conns) > 0 {
		conn := p.conns[len(p.conns)-1]
		p.conns = p.conns[:len(p.conns)-1]
		return conn, nil
	}

	if p.client == nil {
		cli, err := machrpc.NewClient(p.config)
		if err != nil {
			return nil, err
		}
		p.client = cli
	}

	conn, err := p.client.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		return nil, err
	}

	return conn, nil
}

func (p *ConnectionPool) ReleaseConnection(conn api.Conn) {
	p.mu.Lock()
	defer p.mu.Unlock()

	if len(p.conns) < p.maxSize {
		p.conns = append(p.conns, conn)
	} else {
		conn.Close()
	}
}
```

## 完全な例 {#완전한-예제}

各種の操作を示す完全な例です。

```go {linenos=table}
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/machbase/neo-server/v8/api"
	"github.com/machbase/neo-server/v8/api/machrpc"
)

func main() {
	serverAddr := "192.168.1.165:5655"
	serverCert := "./server.pem"
	clientKey := "./client_key.pem"
	clientCert := "./client_cert.pem"

	cli, err := machrpc.NewClient(&machrpc.Config{
		ServerAddr: serverAddr,
		Tls: &machrpc.TlsConfig{
			ClientKey:  clientKey,
			ClientCert: clientCert,
			ServerCert: serverCert,
		},
	})
	if err != nil {
		log.Fatal(err)
	}
	defer cli.Close()

	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	// テーブルを作成
	result := conn.Exec(ctx, `
		CREATE TAG TABLE IF NOT EXISTS example (
			name VARCHAR(20) PRIMARY KEY,
			time DATETIME BASETIME,
			value DOUBLE SUMMARIZED
		)
	`)
	if err := result.Err(); err != nil {
		log.Fatal(err)
	}

	// データを挿入
	for i := 0; i < 5; i++ {
		result = conn.Exec(ctx,
			`INSERT INTO example (name, time, value) VALUES (?, ?, ?)`,
			fmt.Sprintf("sensor%d", i),
			time.Now().Add(time.Duration(i)*time.Second),
			float64(i)*10.5)
		if err := result.Err(); err != nil {
			log.Fatal(err)
		}
	}

	// データを検索
	sqlText := `SELECT name, time, value FROM example LIMIT ?`
	rows, err := conn.Query(ctx, sqlText, 3)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	fmt.Println("Query Results:")
	for rows.Next() {
		var name string
		var ts time.Time
		var value float64

		err = rows.Scan(&name, &ts, &value)
		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("Name: %s, Time: %s, Value: %.2f\n",
			name, ts.Format(time.RFC3339), value)
	}

	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
}
```

## トラブルシューティング {#문제-해결}

### 一般的な問題 {#일반적인-문제}

**接続の拒否**
- サーバーが実行中で、アクセスできることを確認
- サーバーアドレスとポートを確認
- ファイアウォールの規則が接続を許可していることを確認

**TLS証明書のエラー**
- 証明書ファイルのパスが正しいことを確認
- 証明書が有効で、期限切れではないことを確認
- 証明書ファイルのアクセス権限を確認

**認証の失敗**
- ユーザー名とパスワードが正しいことを確認
- machbase-neoのユーザー権限を確認

**クエリのタイムアウト**
- 長時間実行するクエリのcontextのタイムアウトを延長
- 適切なインデックスでクエリ性能を最適化
- 大きな結果セットではページ分割を検討
