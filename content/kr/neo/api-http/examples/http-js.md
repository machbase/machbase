---
title: JavaScript 클라이언트
type: docs
weight: 61
---

## 조회

**JSON**

`format=json`을 지정하거나 생략하여 기본값을 사용합니다.

```js {{linenos=table}}
q = "select * from example"
fetch(`http://127.0.0.1:5654/db/query?q=${encodeURIComponent(q)}`)
  .then(res => {
    return res.json();
  })
  .then(data => {
    console.log(data)
  });
```

**CSV**

`format=csv`를 명시적으로 지정합니다.

```js {{linenos=table}}
q = "select * from example"
fetch(`http://127.0.0.1:5654/db/query?q=${encodeURIComponent(q)}&format=csv`)
  .then(res => {
    return res.text();
  })
  .then(data => {
    console.log(data)
  });
```

## 쓰기

**JSON**

```js  {{linenos=table,hl_lines=[14]}}
payload = {
    data: {
        columns: ["NAME", "TIME", "VALUE"],
        rows: [
            ['temperature',1677033057000000000,21.1],
            ['humidity',1677033057000000000,0.53]
        ]    
    }
}

fetch('http://127.0.0.1:5654/db/write/example', {
    method: 'POST',
    headers: {
        'Content-Type':'application/json'
    },
    body: JSON.stringify(payload)
  });
```

**CSV**

```js  {{linenos=table,hl_lines=[7]}}
payload = `temperature,1677033057000000000,21.1
humidity,1677033057000000000,0.53`

fetch('http://127.0.0.1:5654/db/write/example', {
    method: 'POST',
    headers: {
        'Content-Type':'text/csv'
    },
    body: payload
  });
```
