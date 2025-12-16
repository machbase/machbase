# TRACE_LOG_LEVEL

Machbase 서버에서 문제가 발생했을 때 로그 파일을 통해 상세한 동작을 확인할 수 있습니다. 
TRACE_LOG_LEVEL을 설정하여 각 모듈별로 출력할 로그 레벨을 조절할 수 있습니다.

- **기본값**: 277 (MM_1 + QP_1 + SM_1 + XM_1)
- **범위**: 0 ~ 524287
- **동적 변경**: 가능
- **로그 파일**: `$MACHBASE_HOME/trc/machbase.trc`

## 레벨 값

| 레벨 | 값 | 모듈 |
|------|-----|------|
| MM_1 | 1 | Main Module log level 1 |
| MM_2 | 2 | Main Module log level 2 |
| QP_1 | 4 | Query Processor log level 1 |
| QP_2 | 8 | Query Processor log level 2 |
| SM_1 | 16 | Storage Manager log level 1 |
| SM_2 | 32 | Storage Manager log level 2 |
| CC_1 | 64 | Cluster coordinator log level 1 |
| CC_2 | 128 | Cluster coordinator log level 2 |
| XM_1 | 256 | Cluster query distribution log level 1 |
| XM_2 | 512 | Cluster query distribution log level 2 |
| LM_1 | 1024 | Cluster link management log level 1 |
| LM_2 | 2048 | Cluster link management log level 2 |
| RP_1 | 4096 | Cluster replication log level 1 |
| RP_2 | 8192 | Cluster replication log level 2 |
| MISC_1 | 65536 | Miscellaneous log level 1 |
| MISC_2 | 131072 | Miscellaneous log level 2 |
| DEBUG | 262144 | Debug |


## 설정 방법
```sql
-- 현재 값 확인
select name, value from v$property where name = 'TRACE_LOG_LEVEL';

-- 여러 레벨 조합 (값을 더함)
alter system set TRACE_LOG_LEVEL = {level1 + level2 + ...};
```
