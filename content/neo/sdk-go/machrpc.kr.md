---
title: gRPC 클라이언트
type: docs
weight: 200
---

## 개요

`machrpc` 패키지는 machbase-neo 서버에 연결하고 상호작용하기 위한 표준 Go 데이터베이스 인터페이스를 제공합니다. gRPC를 기반으로 구현되어 Go의 `database/sql` 패키지 규칙과의 호환성을 유지하면서 고성능 연결을 제공합니다.

표준 Go `database/sql` 인터페이스는 **SQL 드라이버** 섹션을 참조하세요.

## 설치

Go 프로젝트에서 machbase-neo SQL 드라이버를 사용하려면 다음 패키지를 설치하세요:

```sh
go get github.com/machbase/neo-server/v8
```

## TLS 설정

machbase-neo SQL 드라이버는 gRPC를 기반으로 하므로, 클라이언트와 서버 간의 안전한 통신을 위해 **TLS 인증서가 필요**합니다. 다음 인증서 파일들을 준비해야 합니다:

- **서버 인증서** (`server-cert.pem`): 서버의 공개 인증서
- **클라이언트 인증서** (`client-cert.pem`): 클라이언트의 공개 인증서
- **클라이언트 키** (`client-key.pem`): 클라이언트의 개인 키

### 인증서 생성

드라이버에 필요한 TLS 인증서(`server-cert.pem`, `client-cert.pem`, `client-key.pem`)를 생성하는 단계별 지침은 [API 보안](/kr/neo/security/) 가이드를 참조하세요. 이 가이드에서는 CA 생성 및 인증서 서명 방법을 설명합니다.

## 기본 사용법

### 연결 설정

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
	// Configure server address and TLS certificates
	serverAddr := "127.0.0.1:5655"
	serverCert := "/path/to/server-cert.pem"
	clientKey := "/path/to/client-key.pem"
	clientCert := "/path/to/client-cert.pem"

	// Create a new gRPC client
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

	// Connect with authentication
	ctx := context.Background()
	conn, err := cli.Connect(ctx, api.WithPassword("sys", "manager"))
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	fmt.Println("Successfully connected to machbase-neo")
}
```

### 설정 옵션

`machrpc.Config` 구조체는 다음 옵션을 허용합니다:

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| `ServerAddr` | string | `host:port` 형식의 서버 주소 (기본값: `127.0.0.1:5655`) |
| `Tls` | *TlsConfig | 안전한 통신을 위한 TLS 설정 |

`machrpc.TlsConfig` 구조체:

| 필드 | 타입 | 설명 |
|-------|------|-------------|
| `ServerCert` | string | 서버 인증서 파일 경로 |
| `ClientCert` | string | 클라이언트 인증서 파일 경로 |
| `ClientKey` | string | 클라이언트 개인 키 파일 경로 |

## 데이터 조회

### 간단한 SELECT 쿼리

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

	// Execute query with parameters
	sqlText := `SELECT name, time, value FROM example LIMIT ?`
	rows, err := conn.Query(ctx, sqlText, 3)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// Iterate through results
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

	// Check for errors during iteration
	if err = rows.Err(); err != nil {
		log.Fatal(err)
	}
}
```

### 파라미터화된 쿼리

SQL 인젝션을 방지하기 위해 항상 파라미터화된 쿼리를 사용하세요:

```go {linenos=table}
// 좋음: 파라미터 사용
rows, err := conn.Query(ctx, 
	"SELECT * FROM sensors WHERE name = ? AND time > ?", 
	"sensor1", startTime)

// 나쁨: 문자열 연결 (SQL 인젝션에 취약)
// rows, err := conn.Query(ctx, 
//     fmt.Sprintf("SELECT * FROM sensors WHERE name = '%s'", userInput))
```

## 명령 실행

### INSERT 문

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

### DELETE 문

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

## 고성능 대량 삽입 (Appender)

대용량 데이터 삽입을 위해서는 `Appender` 인터페이스를 사용하세요. 이는 시계열 데이터 수집에 최적의 성능을 제공합니다:

```go
// 중요: Appender를 위한 별도 연결을 사용하세요
// 활성 Appender가 있는 연결은 다른 작업에 사용하면 안됩니다

apd, err := conn.Appender(ctx, "example")
if err != nil {
	panic(err)
}
defer apd.Close() // 남은 데이터를 플러시하기 위해 항상 appender를 닫으세요

// 고속 대량 삽입
for i := range 10_000 {
	err := apd.Append("grpc", time.Now(), 1.23*float64(i))
	if err != nil {
		panic(err)
	}
}
```

{{< callout type="warning" >}}
**연결 격리**: 활성 Appender가 있는 연결을 다른 데이터베이스 작업에 절대 사용하지 마세요. 추가 작업을 위한 전용 연결을 만드세요.
{{< /callout >}}

{{< callout type="tip" >}}
**성능**: Appender는 시계열 워크로드를 위해 설계되었으며, 적절한 배치 처리를 통해 초당 수십만 건의 삽입을 달성할 수 있습니다.
{{< /callout >}}

## 모범 사례

**1. 항상 Context 사용**

적절한 타임아웃 및 취소 처리를 위해 모든 작업에 context를 전달하세요:

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

rows, err := conn.Query(ctx, "SELECT * FROM large_table")
```

**2. 리소스 닫기**

항상 연결, 명령문, 결과 세트를 닫으세요:

```go
defer cli.Close()
defer conn.Close()
defer rows.Close()
```

**3. 오류를 적절하게 처리**

오류를 무시하지 말고, 더 나은 디버깅을 위해 컨텍스트와 함께 래핑하세요:

```go
if err != nil {
	return fmt.Errorf("failed to query sensor data: %w", err)
}
```

**4. 프로덕션에서 연결 풀링 사용**

오버헤드를 줄이고 성능을 향상시키기 위해 연결을 재사용하세요.

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

## 완전한 예제

다양한 작업을 보여주는 완전한 예제입니다:

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

	// Create table
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

	// Insert data
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

	// Query data
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

## 문제 해결

### 일반적인 문제

**연결 거부**
- 서버가 실행 중이고 접근 가능한지 확인하세요
- 서버 주소와 포트를 확인하세요
- 방화벽 규칙이 연결을 허용하는지 확인하세요

**TLS 인증서 오류**
- 인증서 파일 경로가 올바른지 확인하세요
- 인증서가 유효하고 만료되지 않았는지 확인하세요
- 인증서 파일의 파일 권한을 확인하세요

**인증 실패**
- 사용자 이름과 비밀번호가 올바른지 확인하세요
- machbase-neo에서 사용자 권한을 확인하세요

**쿼리 타임아웃**
- 오래 실행되는 쿼리에 대해 context 타임아웃을 늘리세요
- 적절한 인덱스로 쿼리 성능을 최적화하세요
- 큰 결과 세트에 대해서는 페이지네이션을 고려하세요
