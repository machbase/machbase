---
type: docs
title: '11.8 애플리케이션 연동'
weight: 80
toc: true
---

사용하는 언어의 예제만 선택해 실행합니다. 재귀 Python 예제에는 그래프 실습 테이블이 필요합니다.

SQL의 ID·KB·깊이는 문자열 연결 대신 바인딩합니다. `prepared=True` 커서를 재사용하면 같은 SQL을 다른 시작점/깊이로 실행할 수 있습니다. 다음 코드를 `89_recursive.py`로 저장합니다. DBMS 8.9와 Python SDK가 설치되어 있고 11.5절 테이블이 남아 있어야 합니다.

[전체 코드 다운로드: 89_recursive.py](/assets/dbms-8.9/89_recursive.py)

<details>
<summary>전체 코드 보기</summary>

```python
"""그래프 설정 SQL로준비한실습DB에서동일prepared 재귀문을재실행한다."""
import os
from machbaseAPI import connect

SQL='''WITH RECURSIVE R(NODE_ID,DEPTH) AS (
 SELECT node_id,CAST(0 AS LONG) FROM M89_G_NODE
 WHERE kb_id=:kb AND node_id=:seed
 UNION ALL
 SELECT E.target_id,R.depth+1 FROM M89_G_EDGE E,R
 WHERE E.kb_id=:kb AND E.state='APPROVED'
   AND E.source_id=R.node_id AND R.depth<:max_depth
)
SELECT NODE_ID,DEPTH FROM R ORDER BY DEPTH,NODE_ID'''


def main():
    conn=connect(host=os.environ['M89_HOST'],port=int(os.environ['M89_PORT']),
                 user=os.environ['M89_USER'],password=os.environ['M89_PASSWORD'])
    cur=conn.cursor(prepared=True)
    try:
        for seed,depth in [(2,2),(999,2),(2,1)]:
            cur.execute(SQL,dict(kb=1,seed=seed,max_depth=depth))
            rows=cur.fetchall()
            print('seed=',seed,'depth=',depth,'rows=',rows)
            expected=5 if seed==2 and depth==2 else 4 if seed==2 else 0
            if len(rows)!=expected:raise AssertionError('unexpected recursive row count')
    finally:
        cur.close()
        conn.close()


if __name__=='__main__':main()
```

</details>

```bash
python3 89_recursive.py
```

행 수는 순서대로5·0·4입니다. 없는 시작점으로 빈 결과를 읽은 다음에도 같은 statement를 재실행합니다. 한 커서를 여러 스레드에서 동시에 사용하지 않습니다. SQL 식별자/문법을 값 바인딩으로 대체할 수는 없으므로 앱의 테이블명·술어 정책은 별도 검증합니다.

EXPLAIN은 prepared mode로 실행하지 않습니다. Python에서 계획을 읽을 때는 별도의 일반 `conn.cursor()`로 `EXPLAIN ...` 또는 `EXPLAIN FULL ...`을 실행합니다.

## 언어별 VECTOR 연동

이 절은 모델 다운로드 없이 native bind·조회만 확인합니다. 먼저 다음 SQL을 실행합니다. 각 언어는 별도 ID를 쓰므로 원하는 언어만 실행하거나 모두 실행할 수 있습니다. 재실행으로 PK가 충돌하면 아래 실습 테이블을 명시적으로 정리/재생성하세요.

```sql
CREATE TRANSACTION TABLE M89_SDK(ID INTEGER PRIMARY KEY,V VECTOR(3));
```

### Python: native bind·NULL·APPEND

11.3절의 최신 Python SDK를 사용해 `89_sdk_python.py`로 저장하고 `python 89_sdk_python.py`로 실행합니다. 임베딩 패키지는 이 코드에 필요 없습니다.

```python
import os
from machbaseAPI import connect

conn = connect(host=os.environ['M89_HOST'], port=int(os.environ['M89_PORT']),
               user=os.environ['M89_USER'], password=os.environ['M89_PASSWORD'])
cur = conn.cursor(prepared=True)
try:
    cur.execute('INSERT INTO M89_SDK VALUES(?,?)', [1, [0.25, -1]])
    cur.execute('SELECT ID,V FROM M89_SDK WHERE ID=?', [1])
    print(cur.fetchone())
    conn.append('M89_SDK', [[11, [1, 0, 0]], [12, None]], columns=['ID', 'V'])
finally:
    cur.close()
    conn.close()
```

ID1의 값은 `[0.25,-1,0]`, ID11은 `[1,0,0]`, ID12는 SQL NULL입니다. Python은 list/tuple을 native VECTOR 대상으로 bind하며 결과는 list입니다. 이름 bind·executemany도 사용할 수 있습니다. JSON 경로는 숫자 문자열을 `TO_VECTOR(?,3)`에 넘깁니다.

### JDBC

`JDBC_JAR`에 제공받은 최신 JAR 경로를 지정합니다. 다음 코드를 `SdkVector89.java`로 저장합니다.

```java
import java.sql.*;
import java.util.Arrays;
import com.machbase.jdbc.MachVector;

public class SdkVector89 {
    public static void main(String[] args) throws Exception {
        String url = "jdbc:machbase://" + System.getenv("M89_HOST") + ":" +
                     System.getenv("M89_PORT") + "/MACHBASEDB";
        try (Connection c = DriverManager.getConnection(url,
                System.getenv("M89_USER"), System.getenv("M89_PASSWORD"))) {
            try (PreparedStatement p = c.prepareStatement("INSERT INTO M89_SDK VALUES(?,?)")) {
                p.setInt(1, 2);
                p.setObject(2, new MachVector(new double[] {0.25, -1}));
                p.executeUpdate();
            }
            try (PreparedStatement p = c.prepareStatement("SELECT V FROM M89_SDK WHERE ID=?")) {
                p.setInt(1, 2);
                try (ResultSet r = p.executeQuery()) {
                    if (r.next()) {
                        MachVector value = r.getObject(1, MachVector.class);
                        System.out.println(Arrays.toString(value.toArray()));
                    }
                }
            }
        }
    }
}
```

```bash
export JDBC_JAR=/path/to/current/machbase.jar
javac -cp "$JDBC_JAR" SdkVector89.java
java -cp ".:$JDBC_JAR" SdkVector89
```

Linux/macOS classpath 구분자는 `:`, Windows native Java에서는 `;`입니다. 예상 출력은 `[0.25, -1.0, 0.0]`입니다. `MachVector`는 FLOAT32 값의 독립 사본을 관리합니다. metadata는 `Types.OTHER`, 타입명 VECTOR, precision은 차원입니다. SQL NULL은 VECTOR 대상의 `setObject(i,null)` 또는 `setNull(i,Types.OTHER)`로 처리하고 `getObject`의 NULL을 확인하세요.

### Node.js / TypeScript

전용 디렉터리를 만들고 DBMS 8.9용 Node.js SDK 패키지를 설치합니다.

```bash
mkdir m89-node
cd m89-node
npm init -y
npm install /path/to/current/machbase-ts-client.tgz
```

다음을 이 디렉터리의 `89_sdk_node.cjs`로 저장해 `node 89_sdk_node.cjs`로 실행합니다. M89_* 환경변수는 같은 shell에 있어야 합니다.

```javascript
const {createConnection, Vector} = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({host:process.env.M89_HOST,
    port:Number(process.env.M89_PORT), user:process.env.M89_USER,
    password:process.env.M89_PASSWORD});
  try {
    await conn.execute('INSERT INTO M89_SDK VALUES(?,?)',
      [3, new Vector(new Float64Array([0.25, -1]))]);
    const [rows] = await conn.query('SELECT V FROM M89_SDK WHERE ID=?', [3]);
    console.log(Array.from(rows[0].V.toArray()));
  } finally { await conn.end(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
```

출력은 `[0.25,-1,0]` 값입니다. `new Vector(number[]/Float32Array/Float64Array)`를 사용하며 조회값은 Vector입니다. `toArray()`는 독립 Float32Array 사본입니다. VECTOR 대상의 `null`은 전체 SQL NULL입니다. stream APPEND는 `appendOpen(table, columns)` → `stream.append(rows)` → `stream.close()`이고, 연결 종료는 `conn.end()`입니다.

### .NET 4.0/full 또는 Universal

다음은 net8 콘솔 + 최신 로컬 Universal nupkg 예시입니다. `M89_NUGET_VERSION`에는 실제 받은 nupkg의 패키지 버전을 넣습니다. CMI 4.0.5와 NuGet 버전 문자열은 같은 값이 아닙니다.

```bash
dotnet new console --framework net8.0 --output m89-dotnet
export M89_NUGET_VERSION=실제_패키지_버전
dotnet add m89-dotnet package UniMachNetConnector \
  --version "$M89_NUGET_VERSION" --source /path/to/local/nupkg-directory
```

`m89-dotnet/Program.cs`를 다음으로 바꾸고 `dotnet run --project m89-dotnet`으로 실행합니다. 4.0/full provider를 직접 참조하는 경우 연결 문자열의 Universal 전용 `Protocol` 키를 제거합니다.

```csharp
using System;
using Mach.Data.MachClient;

string host = Environment.GetEnvironmentVariable("M89_HOST")!;
string port = Environment.GetEnvironmentVariable("M89_PORT")!;
string user = Environment.GetEnvironmentVariable("M89_USER")!;
string password = Environment.GetEnvironmentVariable("M89_PASSWORD")!;
using var conn = new MachConnection(
    $"SERVER={host};PORT_NO={port};UID={user};PWD={password};Protocol=4.0-full");
conn.Open();
using (var cmd = new MachCommand(conn) {
    CommandText = "INSERT INTO M89_SDK VALUES(?,?)" }) {
    cmd.Parameters.Add(new MachParameter {ParameterName="id", Value=4});
    cmd.Parameters.Add(new MachParameter {ParameterName="v",
        Value=new MachVector(new double[] {0.25, -1})});
    cmd.Prepare();
    cmd.ExecuteNonQuery();
}
using (var cmd = new MachCommand(conn) {
    CommandText = "SELECT V FROM M89_SDK WHERE ID=4" })
using (var reader = cmd.ExecuteReader()) {
    if (reader.Read()) {
        MachVector value = reader.GetFieldValue<MachVector>(0);
        Console.WriteLine(string.Join(",", value.ToArray()));
    }
}
```

출력은 `0.25,-1,0` 값입니다. `MachVector`, `MachDBType.VECTOR`, `GetFieldValue<MachVector>()` 또는 `GetFieldValue<float[]>()`를 사용합니다. 명시 NULL은 `MachDBType=MachDBType.VECTOR, Value=DBNull.Value`로 지정합니다. 구형 2.x/3.0 provider를 native VECTOR 지원 공급자로 사용하지 않습니다.

### Go database/sql

DBMS 8.9를 지원하는 `neo-client/v2`를 설치합니다. `M89_GO_SDK_VERSION`에는 사용할 SDK 릴리스 버전을 지정합니다.

```bash
mkdir m89-go
cd m89-go
go mod init example.com/m89-vector
go get "github.com/machbase/neo-client/v2@$M89_GO_SDK_VERSION"
```

아래를 `main.go`로 저장하고 `go mod tidy` 후 실행합니다. DSN 형식은 `server=tcp://USER:PASSWORD@HOST:PORT`이며 실제 비밀번호는 URL encoding 규칙을 따릅니다. DSN은 명령 이력에 직접 적기보다 입력받습니다.

```bash
read -rsp 'Go 실습 DSN: ' M89_DSN
export M89_DSN
printf '\n'
go mod tidy
go run -buildvcs=false .
```

```go
package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"
	"time"

	_ "github.com/machbase/neo-client/v2"
	"github.com/machbase/neo-client/v2/api"
)

func run() error {
	db, err := sql.Open("machbase", os.Getenv("M89_DSN"))
	if err != nil {
		return err
	}
	defer db.Close()
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	// Go의 고정 VECTOR 컬럼에는 정확히 3차원을 전달한다.
	if _, err = db.ExecContext(ctx, "INSERT INTO M89_SDK VALUES(?,?)",
		int32(5), api.Vector{0.25, -1, 0}); err != nil {
		return err
	}
	var vector api.Vector
	if err = db.QueryRowContext(ctx, "SELECT V FROM M89_SDK WHERE ID=?", int32(5)).Scan(&vector); err != nil {
		return err
	}
	fmt.Println(vector)
	return nil
}

func main() {
	if err := run(); err != nil {
		log.Fatal(err)
	}
}
```

Go의 일반 고정 VECTOR(3)에는 정확히3개 요소를 넘깁니다. 다른 SDK의 short padding과 혼동하지 않습니다. 모델을 다른 프로세스/서비스에서 돌리는 경우에도 얻은 float32 배열을 `api.Vector(vector)`로 전달하면 되며 Go DB client 자체에 ONNX는 필요 없습니다.

### SDK 공통 확인과 C·embedded 경계

다섯 언어를 모두 한 번씩 실행했다면 ID1~5는 `[0.25,-1,0]`, ID11은 `[1,0,0]`, ID12는 NULL로 총7행입니다.

```sql
SELECT ID,VECTOR_TO_JSON(V) AS VJSON FROM M89_SDK ORDER BY ID;
SELECT COUNT(*) AS N FROM M89_SDK;
SELECT COUNT(*) AS NULL_ROWS FROM M89_SDK WHERE V IS NULL;
```

C CLI/ODBC는 `SQL_MACHBASE_VECTOR`와 `SQL_C_CHAR` 숫자 JSON 또는 `SQL_C_BINARY` little-endian FLOAT32를 사용합니다. 예를 들어 이미 연결된 유효한 `SQLHSTMT`에서 다음 함수로 ID80을 삽입할 수 있습니다. 연결/진단/handle 수명은 기존 C 프로그램이 관리합니다.

```c
#include <machbase_sqlcli.h> /* 배포 SDK에서 SQL_MACHBASE_VECTOR를 선언한 헤더 사용 */

SQLRETURN insert_vector(SQLHSTMT stmt) {
    SQLINTEGER id = 80;
    SQLLEN id_len = sizeof(id), vector_len = 12;
    unsigned char v[12] = {0,0,128,63, 0,0,0,0, 0,0,0,0}; /* [1,0,0] */
    SQLRETURN rc = SQLPrepare(stmt, (SQLCHAR*)"INSERT INTO M89_SDK VALUES(?,?)", SQL_NTS);
    if (!SQL_SUCCEEDED(rc)) return rc;
    rc = SQLBindParameter(stmt,1,SQL_PARAM_INPUT,SQL_C_SLONG,SQL_INTEGER,
                          0,0,&id,sizeof(id),&id_len);
    if (!SQL_SUCCEEDED(rc)) return rc;
    rc = SQLBindParameter(stmt,2,SQL_PARAM_INPUT,SQL_C_BINARY,SQL_MACHBASE_VECTOR,
                          3,0,v,sizeof(v),&vector_len);
    if (!SQL_SUCCEEDED(rc)) return rc;
    return SQLExecute(stmt);
}
```

V2 APPEND는 payload 길이를 선언 차원×4바이트에 맞춰야 합니다. 길이 없는 구형 `SQLAppendData(void**)`에 VECTOR를 넘기지 않습니다. embedded C는 `MachEngineBindParam`/`MachEngineAppendParam`의 `mVector`와 `MachBindParam`/`MachAppendData`/`MachColumnDataVector` 경로를 사용합니다. MachEngine public API는 성공0, 실패는 **양수일 수도 있는 nonzero error code**이므로 `<0`만 검사하지 않습니다.

---

[이전: Ollama로 근거 있는 답변 만들기](../ollama/) · [다음: 운영과 성능 관리](../operations/)

## SDK별 상세 계약

NULL 요소와 SQL NULL, 배열 복사와 메타데이터 처리 규칙은 SDK마다 다릅니다.

- [Python](/kr/dbms-8.9/development-tools-integration/python/#vector-값과-바인딩)
- [JDBC](/kr/dbms-8.9/development-tools-integration/jdbc/#vector-값과-바인딩)
- [Node.js](/kr/dbms-8.9/development-tools-integration/node-js-typescript/#vector-값과-바인딩)
- [.NET](/kr/dbms-8.9/development-tools-integration/net-connector/#vector-값과-바인딩)
- [Go](/kr/dbms-8.9/development-tools-integration/go/#vector-값과-바인딩)
