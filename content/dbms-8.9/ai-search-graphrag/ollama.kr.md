---
type: docs
title: '11.7 Ollama로 근거 있는 답변 만들기'
weight: 70
toc: true
---

로컬 Ollama와 DBMS를 연결해 근거를 인용하는 답변을 생성합니다. 모델 없는 SQL 실습과 별도로 실행합니다.

## 예제 설치

[GraphRAG 예제 패키지 다운로드](/assets/dbms-8.9/graph-rag-example.zip)

11.1절의 접속 환경변수와 DBMS 8.9 Python SDK를 준비합니다. Ollama를 설치한 뒤 다음 명령을 실행합니다.

```bash
unzip graph-rag-example.zip
cd graph-rag-example
python3 -m venv .venv
. .venv/bin/activate
python -m pip install "$M89_PYTHON_WHEEL"
python -m pip install .
ollama pull bge-m3:latest
ollama pull qwen3.5:9b
```

Ollama 서비스는 `http://127.0.0.1:11434`에서 실행되어 있어야 합니다.

다운로드한 예제 패키지와 Ollama를 준비합니다.

| 구성 | 기본값/역할 |
|---|---|
| Ollama | http://127.0.0.1:11434 |
| 임베딩 | bge-m3:latest,1024차원/L2 |
| 생성 LLM | qwen3.5:9b,문맥32768 |
| 데이터 | 제공된 한·영 TAG 매뉴얼26개와 원문 대조 관계 명세 |
| DB 객체 | GRRAG_전용5개 테이블. 위 M89_G_실습과별도 |
| 기본 캐시 | graph-rag-cache |

현재 기본 prepare는 원문 SHA/정확 인용과 대조한 semantic_assertions.json을 사용합니다. 임의 새 문서를 넣으면 자동으로 완성된 온톨로지가 나온다는 뜻이 아닙니다. 문서를 바꾸면 명세도 다시 검토해야 합니다. `rebuild-ontology --propose`의 LLM 제안은 DRAFT/REVIEW이며 자동 게시하지 않습니다. 게시 전에 원문과 관계의 정확성을 검토합니다.

예제 디렉터리에서 다음을 실행합니다. 별도 M89_G_실습을 정리했더라도 이 프로그램은 자신의 GRRAG_객체를 사용합니다. 기존 GRRAG_이름 공간이나 다른 snapshot은 자동 덮어쓰지 않습니다.

```bash
export GRAPH_RAG_CACHE="$PWD/graph-rag-cache"
export GRAPH_RAG_HOST="$M89_HOST" GRAPH_RAG_PORT="$M89_PORT" GRAPH_RAG_USER="$M89_USER"
export GRAPH_RAG_PASSWORD="$M89_PASSWORD"
machbase-graph-rag doctor
machbase-graph-rag prepare
machbase-graph-rag export-review --output graph-rag-cache/review
machbase-graph-rag verify
# 검토가 끝나지 않으면 종료 코드 2와 NOT_REVIEWED가 표시됩니다.
# 아래 init/load는 비어 있는 GRRAG_ 이름 공간에서 실행합니다.
machbase-graph-rag init
machbase-graph-rag load
machbase-graph-rag chat --save-session graph-rag-cache/session.jsonl
```

`verify`가 `NOT_REVIEWED`를 반환하면 캐시 디렉터리의
`semantic-review-template.csv`, `edge-review-template.csv`, `alias-review-template.csv`를
각각 `semantic-review.csv`, `edge-review.csv`, `alias-review.csv`로 복사합니다.
검토 HTML과 원문을 대조하고 각 검토 항목의 `verdict`에 `PASS` 또는 `FAIL`,
`reviewer`에 검토자, `notes`에 판정 근거를 기록한 뒤 `verify`를 다시 실행합니다.
검토를 통과한 자료만 적재합니다.

질문마다 다음 단계를 실행합니다.

1. LLM 질문 해석·개념 후보 추출
2. 질문 임베딩
3. 정확 이름/별칭과 개념 Hybrid 검색
4. 관계 탐색과 문서 후보 Hybrid 검색
5. 승인 명제와 현재 원문 조회
6. 관련 명제 선별, 필요하면 SQL 예제 주변 문맥 추가 조회
7. LLM이 명제·조건·원문을 근거로 자연어 답변 작성
8. 답변 상태·인용 검사, 필요하면1회 보정

각 단계의 시작/완료·소요/누적 시간과 전체 시간을 표시하고, 긴 단계는5초마다 진행 시간을 보여 줍니다. `/trace`와 저장 세션의 timing에서도 확인합니다. DB 검색 시간만을 전체 RAG 응답 시간으로 보고하지 않습니다.

| 채팅 명령 | 기능 |
|---|---|
| /sources, /source S1 | 답변 근거 목록과 선택 원문 |
| /graph, /concept ID | 연결 경로와 DB의 개념·관계·출처 |
| /trace, /status | 질의 분석·SQL·바인딩·시간 및 적재 상태 |
| /mode direct, graph, hybrid | 직접 검색/그래프 후보 검색/빈 그래프 결과의 직접 검색 보완 |
| /policy context, taxonomy | 문맥 관계만/분류 관계도 확장 |
| /clear, /quit | 대화 초기화/종료 |

현재 상태는 자연어 생성 답변의 CITED 또는 근거 부족의 INSUFFICIENT로 구분합니다. 인용 ID·원문 SQL 문장·관측된 일부 범위 강화에 대한 검사는 전체 의미 정확도 인증이 아닙니다. taxonomy의 공통 CLASS를 경유하면 후보가 크게 넓어질 수 있으므로 목적에 맞게 사용합니다. 기본 문맥 탐색은 클래스 공유만으로 모든 노드를 확장하지 않습니다.



[다음: 애플리케이션 연동](../application-integration/)

## 검색 계획과 성능 비교

적재를 완료한 동일 데이터에 대해 검색 모드별 경로를 확인합니다.

```bash
machbase-graph-rag explain '펌프 진동 점검 절차는?' --mode graph
machbase-graph-rag explain '펌프 진동 점검 절차는?' --mode graph --full
machbase-graph-rag benchmark '펌프 진동 점검 절차는?' --output graph-rag-cache/benchmark
```

`explain --full`은 실제 검색을 실행합니다. benchmark는 direct·graph·hybrid 각각의
첫 실행과 반복 실행, p50·p95와 실행 계획을 저장합니다. 모드별 후보 범위가 다르므로
시간뿐 아니라 반환 근거와 경로도 비교합니다.

DB 검색 시간은 질문 해석·임베딩·LLM 답변 생성까지의 전체 시간이 아닙니다.
전체 응답 지연은 `/trace`의 단계별 시간과 함께 확인합니다.
