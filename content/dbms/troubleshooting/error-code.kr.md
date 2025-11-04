---
layout : post
title : 'Error Code'
type: docs
weight: 10
---

|code|mssage|설명입니다.|
|--|--|--|
|1|Failed to create file<%s>, errno = %d.|파일 생성에 실패했습니다.|
|2|Failed to truncate file<%s>, errno = %d.|파일 truncate에 실패했습니다.|
|3|Failed to duplicate file<%s>, errno = %d.|파일 복제에 실패했습니다.|
|4|Failed to copy file<%s> to file<%s>, errno = %d.|파일 복제에 실패했습니다.|
|5|Failed to rename file<%s> to file<%s>, errno = %d.|파일 rename에 실패했습니다.|
|6|Failed to remove file<%s>, errno = %d.|파일 삭제에 실패했습니다.|
|7|Failed to get key file<%s>, errno = %d.|파일의 key 획득에 실패했습니다.|
|8|Failed to create pipe<%s>, errno = %d.|파이프 생성에 실패했습니다.|
|9|Failed to statistic file<%s>, errno = %d.|파일 통계정복 획득에 실패했습니다.|
|10|Failed to open file<%s>, errno = %d.|파일 open에 실패했습니다.|
|11|Failed to close file<%s>, errno = %d.|파일 close에 실패했습니다.|
|12| Failed to seek file<%s>, offset:%lld, Whence:%d, errno = %d.  |파일 seek에 실패했습니다.|
|13|Failed to read file<%s>, size:%llu, errno = %d.|파일 read에 실패했습니다.|
|14|Failed to write file<%s>, size:%llu, errno = %d.|파일 write에 실패했습니다.|
|15|Failed to read file<%s> (offset:%llu, req size:%llu, read size: %llu), errno = %d.|파일 read에 실패했습니다.|
|16|Failed to write file<%s> (offset:%llu, req size:%llu, read size: %llu), errno = %d.|파일 write에 실패했습니다.|
|17|Failed to sync file<%s>, errno = %d.|파일 sync에 실패했습니다.|
|18|Failed to lock file<%s>, errno = %d.|파일 lock에 실패했습니다.|
|19|Failed to trylock file<%s>, errno = %d.|파일 try lock에 실패했습니다.|
|20|Failed to unlock file<%s>, errno = %d.|파일 unlock에 실패했습니다.|
|21|There is no file extension.|파일 확장자 오류가 발생했습니다.|
|22|Failed to rename file<%s> to file<%s>, retry count<%d>, msec<%d>, errno = %d.|파일 조작 실패 시 발생하는 에러가 발생했습니다.|
|31|Error occurred during snprintf: buffer size<%d>, errno = %d.|파일 조작 실패 시 발생하는 에러가 발생했습니다.|
|61|Failed to getenv variable<%s>, errno = %d.|환경변수 조회에 실패했습니다.|
|62|Failed to setenv variable<%s> to value<%s>, errno = %d.|환경변수 설정에 실패했습니다.|
|67|Failed to opendir <%s>, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|68|Failed to closedir, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|69|Failed to readdir, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|70|Failed to rewinddir, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|71|Failed to makedir <%s>, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|72|Failed to removedir, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|73|Failed to setcwd, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|74|Failed to getcwd, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|75|Failed to gethome, errno = %d.|홈디렉토리 조회에 실패했습니다.|
|76|Path<%s> is too long, errno = %d.|File path 관련 에러가 발생했습니다.|
|77|Path<%s/%s> is too long, errno = %d.|File path 관련 에러가 발생했습니다.|
|78|Path<%s/%s/%s> is too long, errno = %d.|File path 관련 에러가 발생했습니다.|
|79|The directory does not exist in this path<%s>, errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|80|Failed to call removedir (%s), errno = %d.|디렉터리 관련 함수에 실패했습니다.|
|91|%1$s(): [%2$d: %3$s]|Meta DB 관련 함수에 실패했습니다.|
|92|%1$s(): [%2$d: %3$s]|Meta DB 관련 함수에 실패했습니다.|
|121|Stack create failed, errno = %d.|stack 자료구조 에러가 발생했습니다.|
|122|Stack push failed, errno = %d.|stack 자료구조 에러가 발생했습니다.|
|123|Stack pop failed, errno = %d.|stack 자료구조 에러가 발생했습니다.|
|131|Failed to allocate memory(%lu bytes), errno = %d.|메모리 할당에 실패했습니다.|
|132|Memory allocation error (alloc'd: %llu, max: %llu).|메모리 할당에 실패했습니다.|
|133|Failed to allocate memory (ID = %d) (Request Size = %llu) : (Current Allocated Size / PROCESS_MAX_SIZE (%llu/%llu)).|메모리 할당에 실패했습니다.|
|141|Failed to create memory pool, errno = %d.|메모리 할당에 실패했습니다.|
|142|Failed to allocate memory from memory pool, errno = %d.|메모리 할당에 실패했습니다.|
|151|Failed to create mutex, errno = %d.|mutex 객체 에러가 발생했습니다.|
|152|Failed to destroy mutex, errno = %d.|mutex 객체 에러가 발생했습니다.|
|153|Failed to lock mutex, errno = %d.|mutex lock 에러가 발생했습니다.|
|154|Failed to trylock mutex, errno = %d.|mutex lock 에러가 발생했습니다.|
|155|Failed to unlock mutex, errno = %d.|mutex unlock 에러가 발생했습니다.|
|161|Failed to create queue, errno = %d.|queue 자료구조 에러가 발생했습니다.|
|162|Failed to destroy queue, errno = %d.|queue 자료구조 에러가 발생했습니다.|
|163|Failed to enqueue queue, errno = %d.|queue 자료구조 에러가 발생했습니다.|
|164|Failed to dequeue queue, errno = %d.|queue 자료구조 에러가 발생했습니다.|
|171|Failed to create thread_attr, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|172|Failed to destroy thread_attr, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|173|Failed to set thread_attr bound, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|174|Failed to set thread_attr detach, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|175|Failed to set thread_attr stack size, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|176|Failed to create thread, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|177|Failed to detach thread, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|178|Failed to join thread, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|179|Failed to get id of thread, errno = %d.|thread 관련 함수 에러가 발생했습니다.|
|191|Failed to create thread condition variable, errno = %d.|Thread 조건 변수를 생성에 실패했습니다.|
|192|Failed to destroy thread condition variable, errno = %d.|Thread 조건 변수를 삭제에 실패했습니다.|
|193|Failed to call cond_timedwait, errno = %d.|cond_timedwait 호출에 실패했습니다.|
|194|Failed to call cond_signal, errno = %d.|cond_signal 호출에 실패했습니다.|
|195|Failed to call cond_broadcast, errno = %d.|cond_broadcast 호출에 실패했습니다.|
|196|Failed to call cond_wait, errno = %d.|cond_wait 호출에 실패했습니다.|
|201|Failed to create rwlock, errno = %d.|rwlock 생성에 실패했습니다.|
|202|Failed to destroy rwlock, errno = %d.|rwlock 제거에 실패했습니다.|
|203|Failed to call rwlock_lock_read, errno = %d.|rwlock_lock_read 호출에 실패했습니다.|
|204|Failed to call rwlock_trylock_read, errno = %d.|rwlock_trylock_read 호출에 실패했습니다.|
|205|Failed to call rwlock_lock_write, errno = %d.|rwlock_lock_write 호출에 실패했습니다.|
|206|Failed to call rwlock_trylock_write, errno = %d.|rwlock_trylock_write 호출에 실패했습니다.|
|211|RBTREE buffer<%d> is too small for value<%d>, errno = %d.|Value를 위한 RBTREE buffer가 너무 작음입니다.|
|212|RBTREE cursor op not applicable. errno = %d.|RBTREE cursor 옵션 적용는 불가능합니다.|
|213|RBTREE node is already freed, errno = %d.|RBTREE 노드가 이미 해제됩니다.|
|216|Key already exists.|키가 이미 존재합니다.|
|221|LZO compress failed, errno = %d.|LZO 압축에 실패했습니다.|
|222|LZO decompress failed, errno = %d.|LZO 압축해제에 실패했습니다.|
|231|Failed to get CPU count, errno = %d.|CPU개수 조회에 실패했습니다.|
|232|Configuration file does not exist(%S).|사용되지 않습니다|
|251|Tlsf memory manager initialization failed, errno = %d.|TLSF 메모리 관리자 초기화에 실패했습니다.|
|252|Tlsf memory manager finalization failed, errno = %d.|TLSF 메모리 관리자 정리에 실패했습니다.|
|253|Tlsf memory manager allocation(%lld) failed, errno = %d.|TLSF 메모리 관리자 할당에 실패했습니다.|
|254|Tlsf memory manager free failed, errno = %d.|TLSF 메모리 관리자 해제에 실패했습니다.|
|255|Tlsf memory manager control failed, errno = %d.|TLSF 메모리 관리자 제어에 실패했습니다.|
|256|Tlsf memory manager shrink failed, errno = %d.|TLSF 메모리 관리자 shrink에 실패했습니다.|
|257|Tlsf memory manager getstatistics failed, errno = %d.|TLSF 메모리 관리자 통계 가져오기에 실패했습니다.|
|271|The session is closed.|세션이 종료됩니다|
|272|The session is canceled.|세션이 취소됩니다|
|291|The license is invalid or expired.|라이선스가 올바르지 않거나 만료되었음입니다.|
|292|The value<%s> does not exist in the license file.|해당 값이 라이선스파일에 없습니다.|
|293|Failed to get hardware key, errno =%d|Hardware 키를 가져오기에 실패했습니다.|
|294|Failed to verify the license, errno = %d|라이선스 확인에 실패했습니다.|
|300|Invalid date value.(%s)|올바른 datetime 타입이 아님입니다.|
|301|Invalid network string.(%s)|올바른 IP 타입이 아님입니다.|
|321|Error in initializing sha1, errno = %d|sha1 초기화에 실패했습니다.|
|322|Error in updating sha1, errno = %d|sha1 갱신에 실패했습니다.|
|323|Error in finalizing sha1, errno = %d|sha1 정리에 실패했습니다.|
|324|Invalid SHA type.(%d)|잘못된 SHA 타입입니다.|
|326|Invalid SHA hex string.(%s)|잘못된 SHA hax 문자열입니다.|
|341|Parallel job thread abnormally terminated|병렬 작업 thread 비정상 종료입니다.|
|342|The thread count should be between %d and %d| thread 수는 범위내에 있어야 합니다.|
|361|Error in setting a log to the buffer of the result file: %s, errno = %d|결과 파일 buffer에 로그 설정중에서 오류가 발생했습니다.|
|381|Regular expression error: an error occurred at offset %d of (%s).|정규 표현식 오류: 해당 위치에서에서 오류가 발생했습니다.|
|400|This DB file is older than binary (no meta-version table). Check database image and binary.|DB 파일이 실행파일보다 오래됩니다. DB 이미지 및 실행파일 확인가 필요합니다.|
|401|Version mismatched. In Executable DB(%d.%d) META(%d.%d) CM(%d.%d) But, In File DB(%d.%d) META(%d.%d) CM(%d.%d)|버전 불일치. 실행 가능한 데이터베이스와 파일 데이터베이스가 다름입니다.|
|420|Error in getting system information by the sysinfo, errno = %d|시스템 정보를 가져오는 중 오류가 발생입니다.|
|421|Error in getting stack information by the pmuSysSetStackSize, errno = %d|pmuSysSetStackSize를 통해 스택 정보를 가져오는 중에서 오류가 발생했습니다.|
|422|Error in setting stack information by the pmuSysSetStackSize, errno = %d|pmuSysSetStackSize를 통해 스택 정보를 설정하는 중에서 오류가 발생했습니다.|
|431|mmap (size<%u>) error, errno = %d|mmap 오류가 발생했습니다.|
|432|unmap (address<%p>, size<%u>) error, errno = %d|unmap 오류가 발생했습니다.|
|451|Failed to set the CPU affinity [%u, %u), errno = %d|CPU affinity 설정에 실패했습니다.|
|452|The IDs of CPUs should be between [0, %u), but [%u, %u) given.|CPU ID는 주어진 범위 내에 있어야 합니다.|
|453|Maximum abs value of CPU_AFFINITY_COUNT(%d) should be less than CPU count(%u).|CPU_AFFINITY_COUNT의 최대 abs 값은 CPU 수보다 작아야 합니다.|
|461|Failed to get the number of CPUs in sysconf, errno = %d|sysconf에서 CPU 수를 가져오는 데 실패했습니다.|
|471|Failed to initialize a heap.|heap 자료구조 에러가 발생했습니다.|
|472|Heap push failed, errno = %d|heap 자료구조 에러가 발생했습니다.|
|491|Error in json dump.|json 조작 및 변환 관련 에러가 발생했습니다.|
|492|Error in json load.|json 조작 및 변환 관련 에러가 발생했습니다.|
|493|json object error: %s|json 조작 및 변환 관련 에러가 발생했습니다.|
|494|Error in json-array.|json 조작 및 변환 관련 에러가 발생했습니다.|
|495|Error in json-string (%s).|json 조작 및 변환 관련 에러가 발생했습니다.|
|496|Error in json-integer (%lld).|json 조작 및 변환 관련 에러가 발생했습니다.|
|497|Error in json-real (%lf).|json 조작 및 변환 관련 에러가 발생했습니다.|
|498|Error in json copy.|json 조작 및 변환 관련 에러가 발생했습니다.|
|499|Error in json pack.|json 조작 및 변환 관련 에러가 발생했습니다.|
|500|Error in json unpack.|json 조작 및 변환 관련 에러가 발생했습니다.|
|501|No data matches for the json path (%s)|json 조작 및 변환 관련 에러가 발생했습니다.|
|502|Json path is too long.|json 조작 및 변환 관련 에러가 발생했습니다.|
|503|Error json object set (%s).|json 조작 및 변환 관련 에러가 발생했습니다.|
|504|Error json array append.|json 조작 및 변환 관련 에러가 발생했습니다.|
|505|Error encode base64.|Base64 인코딩 오류가 발생했습니다.|
|506|Error decode base64.|Base64 디코딩 오류가 발생했습니다.|
|600|Invalid property value: %s.|잘못된 property 값입니다.|
|601|Failed to convert %s to UTF8. (%s, errno=%d)|UTF8로 변환에 실패했습니다.|
|602|Buffer size is not enough for code conversion. (%d > %d)|코드 변환을 위한 버퍼 크기가 충분하지 않습니다.|
|701|Geohash invalid precision (%u)|geohash 유효하지 않은 정확도입니다.|
|702|Geohash invalid length|geohash 유효하지 않은 길이입니다.|
|703|Geohash invalid direction|geohash 유효하지 않은 방향입니다.|
|1000|File<%s> is invalid.|잘못된 파일입니다.|
|1001|Invalid object storage id, errno = %d.|잘못된 객체 저장소입니다.|
|1002|Object storage<%d> already freed, errno = %d.|객체 저장소가 이미 해제됩니다.|
|1003|Group storage dir<%s> already exists, errno = %d.|그룹 저장소가 디렉토리가 이미 존재합니다.|
|1004|Object filename<%s> is invalid, errno = %d.|객체 파일이름이 유효하지 않습니다.|
|1005|Disk file<%s> is in use, errno = %d.|디스크 파일이 사용중입니다입니다.|
|1006|Functionality is not supported yet.|기능이 아직 지원되지 않습니다.|
|1007|There is no available disk space for writing <%lld>bytes to the file<%s>, errno = %d.|파일에 write 하기 위한 사용 가능한 디스크 공간이 없습니다.|
|1008|Error in the duplicating file<%s>, errno = %d.|파일 복제 중에서 오류가 발생했습니다.|
|1009|Error in the read file size.(<io: %u>, <disk: %u>)|파일 read size 오류. read하려고한 size와 실제 read한 size가 다름입니다.|
|1010|Used media space is reached to threshold. (%4.1lf%% cap < %4.1lf%% used)|사용중인 미디어 공간이 임계값에 도달합니다.|
|1011|Error in the write file size.(<write: %u>, <written: %u>)|파일 write size 오류. write하려고한 size와 실제 write된 size가 다름입니다.|
|1031|The database in <%s> has already been mounted.|Database 가 이미 마운트 됩니다.|
|1032|The database in <%s> is not mounted.|Database 마운트되지 않습니다.|
|1033|The mount operation of database in <%s> is not completed.|Database 마운트 작업이 완료되지 않습니다.|
|1034|The mounted database<%s> is busy.|마운트된 database가 사용중입니다입니다.|
|1035|The database creation is not complete. Destroy it and create a new one.|Database 생성이 완료되지 않습니다. 삭제후 다시 생성 필요합니다.|
|1036|The database creation is not complete. Destroy it and create a new one.|Database 생성이 완료되지 않습니다. 삭제후 다시 생성 필요합니다.|
|1037|The mount database<%s> is not backed up from the primary database|마운트된 database 가 기본 데이터베이스에서 백업되지 않습니다.|
|1038|Cannot find MountDB with <TBSID: %lld>.|해당 TBSID와 관련된 MountDB를 찾을 수 없습니다.|
|1039|Mount DB<%s>'s state is invalid.|잘못된 마운트 DB 상태입니다.|
|1101|Error in reading column partition cache block. Reading block of RID<%lld> in the column partition<%lld> failed, errno = %d.|칼럼 파티션 cache 블록을 읽는 중에서 오류가 발생했습니다.|
|1102|Invalid cache object.|잘못된 cache 객체입니다.|
|1103|Error occurred in checkpoint thread. Processing abnormal shutdown.|체크포인트 thread에서 오류 발생. 처리 중 비정상 종료됩니다.|
|1104|Error in waiting to read a page.|페이지 read 대기중 오류가 발생했습니다.|
|1105|Error in clear thread of the page cache.|페이지 cache clear thread 오류가 발생했습니다.|
|1106|It<%llu> is smaller than the max size value of the page cache currently set<%llu>.|현재 설정된 페이지 cache의 최대 크기 값보다 작습음입니다.|
|1107|It<%llu> is impossible to set a value larger than the memory size set in the current process<%llu>.|현재 프로세스에 설정된 메모리 크기보다 큰 값을 설정할 수 없습니다.|
|1108|Invalid page id in column partition. Page id<%d> is greater than the page max id<%d>.|칼럼 파티션 잘못된 페이지 ID. 페이지 ID가 최대 페이지 ID보다 큼입니다.|
|1201|Duplicated table id<%llu> in SYS_STORAGE_TABLES, errno = %d.| SYS_STORAGE_TABLES에 중복된 테이블 ID가 있습니다.|
|1202|Duplicated table id<%llu>, column id<%u> in the SYS_STORAGE_COLUMNS, errno = %d.|SYS_STORAGE_COLUMNS에 중복된 테이블 ID와 칼럼 ID가 있습니다.|
|1203|Table id<%lld> does not exist in SYS_STORAGE_TABLES, errno = %d.|테이블 ID가 SYS_STORAGE_TABLES에 존재하지 않습니다.|
|1204|Duplicated (table id<%llu>, index id<%llu>) in SYS_STORAGE_INDEXES, errno = %d.|SYS_STORAGE_INDEXES에 중복된 항목이 있습니다.|
|1205|Duplicated (table id<%llu>, index id<%llu>, column id<%u>) in SYS_STORAGE_INDEXES_COLUMNS, errno = %d.|SYS_STORAGE_INDEXES_COLUMNS에 중복된 항목이 있습니다.|
|1206|Index id<%llu> of table id<%llu> dose not exist in SYS_STORAGE_INDEXES, errno = %d.|테이블의 인덱스 ID<가 SYS_STORAGE_INDEXES에 존재하지 않습니다.|
|1207|Available recovery modes: simple, complex, reset|사용 가능한 복구 모드: simple, complex, reset입니다.|
|1301|Partition range does not exist. Partition id is less than <%lld> in the table(id<%lld>) with partitions between <%lld> and <%lld>.|파티션 범위가 존재하지 않습니다. 범위내에 파티션이 있는 테이블에 존재하지 않습니다.|
|1302|Invalid record range. No such record whose id is less than <%llu> in the table(id<%llu>) with records between <%llu> and <%llu>.|잘못된 레코드 범위. 범위내에 레코드가 있는 테이블이 존재하지 않습니다.|
|1303|Maximum number of columns in a table is %d.|테이블의 최대 칼럼 수입니다.|
|1304|Invalid column ID (<%d>).|잘못된 칼럼 ID입니다.|
|1305|Invalid table ID (<%llu>).|잘못된 테이블 ID입니다.|
|1306|Table has been dropped.|테이블이 drop됩니다.|
|1307|Table structure was modified.|테이블 구조가 변경됩니다.|
|1308|Invalid fixed column size. Invalid value size(<%u>) for the fixed column.|유효하지 않은 fixed 칼럼 열 크기입니다.|
|1309|Invalid varying column size. Value size(<%u>) for the variable column is greater than the max size (<%u>).|유효하지 않은 variable 칼럼 크기. 최대크기보다 큼입니다.|
|1310|Table flush thread terminated abnormally.|테이블 flush thread가 비정상 종료합니다.|
|1311|Table column partition prepare thread terminated abnormally.|테이블 칼럼 파티션 준비 thread가 비정상 종료합니다.|
|1312|Failed to read the head of the table column partition file (<%s>).|테이블 칼럼 파티션 파일 head read에 실패했습니다.|
|1313|Failed to read the table column partition file (<%s>).|테이블 칼럼 파티션 파일 read에 실패했습니다.|
|1314|Index build thread terminated abnormally.|인덱스 빌드 thread가 비정상 종료합니다.|
|1315|Invalid table type<%d>.|잘못된 테이블 타입입니다.|
|1316|Column size<%u> is too big.|칼럼의 크기가 너무 큼입니다.|
|1317|Value of the time column(<%lld>) is less than the last time value(<%lld>).|시간 칼럼의 값이 마지막 시간 값보다 작음입니다.|
|1318|The size of VARCHAR column must be less than (<%llu>).|VARCHAR 칼럼의 크기는 더 작아야 합니다.|
|1319|The size of column value must be less than (<%u>).|칼럼 값의 크기는 더 작아야 합니다.|
|1320|There is an index on the column(<%u>) of the table(<%llu>)|테이블의 칼럼에 인덱스가 있습니다.|
|1321|This feature is not supported on this table type.|기능이 이 테이블 타입에서 지원되지 않습니다.|
|1322|The new column size(<%u>) should be greater than the old one(<%u>)|새 칼럼의 크기는 기존 칼럼의 크기보다 커야 합니다.|
|1323|The table(%llu) reached max column count limit (%u) already.|테이블이 이미 최대 칼럼 수 제한에 도달합니다.|
|1324|An error occurred adjusting end rid of the table<%llu> column partition(<%llu>), errno = %d.|테이블 칼럼 파티션종료시 RID 조정 중에서 오류가 발생했습니다.|
|1325|The end RID<%lld> of the column<%d> is less than the end RID<%llu> of the table<%llu>|칼럼의 end RID가 테이블의 end RID 보다 작음입니다.|
|1330|The column with ID<%hu> does not exist in the table with ID<%llu>| 해당 ID를 가진 칼럼이 테이블에 존재하지 않습니다.|
|1331|Table checkpoint thread terminated abnormally.|테이블 체크포인트 thread가 비정상적으로 종료됩니다.|
|1332|Partition ID <%llu> of the table(id<%llu>) does not exist between <%llu> and <%llu>.|테이블)의 파티션 ID가 범위내에 존재하지 않습니다.|
|1333|The table<%llu> in the backup database<%s> has been mounted already.| 백업 database 의 테이블이 이미 마운트됩니다.|
|1334|The table is busy with mounting.|테이블이 마운트중입니다입니다.|
|1335|The mounted table is busy with unmounting.|마운트된 테이블이 언마운트중입니다입니다.|
|1336|The mounted table is invalid.|마운트된 테이블이 유효하지 않습니다.|
|1337|The mounted table is busy.|마운트된 테이블이 사용중입니다입니다.|
|1338|The table is not mounted.|테이블이 마운트되지 않습니다.|
|1339|The table<%llu> of the backup tablespace<%s> is different from the table in main database.|백업 tablespace의 테이블이 기본 database의 테이블과 다름입니다.|
|1340|The table<%llu> of the backup tablespace<%s> is dropped from the main database.|백업 tablespace의 테이블이 기본 database에서 삭제됩니다.|
|1341|There is a mounted table in the table<%llu>.|테이블에 마운트된 테이블이 있습니다.|
|1342|The mount table<end_rid:%llu> has more furture data than the base table<end_rid:%llu.>|마운트된 테이블이 기본 테이블보다 더 많은 미래 데이터를 가지고 있습니다.|
|1343|Cannot update columns with indexes in VOLATILE / LOOKUP table.|VOLATILE / LOOKUP 테이블에서 인덱스가 있는 칼럼을 업데이트 할 수 없습니다.|
|1344|The memory size<%llu bytes> of VOLATILE / LOOKUP tables exceeds <%llu bytes>.|VOLATILE / LOOKUP 테이블 메모리 크기 초과입니다.|
|1345|The value of the column<%u> must not be NULL|해당 칼럼의 값은 NULL이면 안됩니다.|
|1346|Current Allocate Memory / PROCESS_MAX_SIZE (%llu/%llu), increase PROCESS_MAX_SIZE property and restart.|현재 할당된 메모리를 늘리고 재시작 필요합니다. (PROCESS_MAX_SIZE 증가 필요)입니다.|
|1401|Invalid index type. Index type<%d> does not exist.|잘못된 인덱스 타입. 해당 인덱스 타입이 존재하지 않습니다.|
|1402|Index id(<%llu>) does not exist in table id <%llu>.|테이블에 해당 인덱스의 ID가 존재하지 않습니다.|
|1403|Index has invalid column count(<%d>).|인덱스의 칼럼 개수가 유효하지 않습니다.|
|1404|Index has invalid key value count(<%d>).|인덱스의 키 값 개수가 유효하지 않습니다.|
|1405|Index has invalid key value size(<%d>).| 인덱스의 키 값 크기가 유효하지 않습니다.|
|1406|Index column file(<%s>) is invalid.|잘못된 인덱스 칼럼 파일입니다.|
|1407|Failed to read the head of the index column partition file(<%s>).|인덱스 칼럼 파티션 파일 head read에 실패했습니다.|
|1408|Failed to read the index column partition file(<%s>).|인덱스 칼럼 파티션 파일 read에 실패했습니다.|
|1409|Type of the column for the index is invalid.|인덱스를 위한 칼럼타입이 유효하지 않습니다.|
|1410|Index flush thread terminated abnormally.|인덱스 flush thread가 비정상 종료합니다.|
|1411|Index build thread terminated abnormally.|인덱스 빌드 thread가 비정상 종료합니다.|
|1412|The keyword size<%d> should be less than the max size<%d>.|키워드 크기는 최대 크기보다 작아야 합니다.|
|1413|The word bit count(%d) is over than %d in the partition<%lld> of the index <%lld>|파티션 인덱스 비트 수 초과입니다.|
|1414|Invalid key count <%u> is not equal to the count <%u> in partition <%lld> of index <%lld>.|유효하지 않은 키 개수. 인덱스 파티션 내 개수와 불일치입니다.|
|1415|The level<%u> of the index is bigger than the max level<%u>|인덱스의 레벨이 최대 레벨보다 큼입니다.|
|1416|The partition size<%u> of level<%u> is bigger than the max level<%u>|이 레벨의 파티션 크기가 최대 레벨의 파티션 크기 보다 큼입니다.|
|1417|The index has been dropped.|인덱스가 drop됩니다.|
|1418|The key already exists in the unique index.|유니크 인덱스에 이미 키가 존재합니다.|
|1419|The primary index is already created on the table.|테이블에 이미 기본 인덱스가 생성됩니다.|
|1420|The number<%llu> of key values is different from the number<%llu> of bitvectors.|키 값의 수와 비트벡터의 수가 다름입니다.|
|1421|The partition file<%llu> on the level<%u> of the index<%llu> is invalid.(KPC:%u, BPC:%u)|인덱스 해당 레벨 있는 파티션 파일이 유효하지 않습니다.|
|1422|NULL value is not allowed for the primary index column|기본 인덱스에 NULL값이 허용되지 않습니다.|
|1423|TAG cache exhausted, increase TAG_CACHE_MAX_MEMORY_SIZE(%llu)|TAG cache 소진. TAG_CACHE_MAX_MEMORY_SIZE 증가 필요합니다.|
|1424|Could not allocate TAG cache: (Table,part=%llu,%llu) offset/size=%llu/%llu|TAG cache를 할당할 수 없습니다.|
|1425|Failed to allocate index memory (Current Allocated Size / Threshold size (%llu/%llu)).|인덱스 메모리 할당에 실패했습니다.|
|1426|Not ready to build keyvalue index (Current Count / Target Count (%llu/%llu) in File).|keyvalue 인덱스를 빌드할 준비가 안됩니다.|
|1501|Invalid page id in cpfile. Page id<%d> for the column partition file<%s> is greater than the page max id.|유효하지 않은 cpfile의 page ID. Page ID가 page의 최대 ID를 초과합니다.|
|1502|Error in reading page<%d> in the column partition file<%s>. Page timestamps <head:%lld, tail:%lld> are invalid.|칼럼 파티션 파일 read 중 오류 발생. 잘못된 timestamp입니다.|
|1503|Error in reading page<%d> in the column partition file<%s>. Page checksum <write:%#X, read:%#X> are invalid|칼럼 파티션 파일 read 중 오류 발생. 잘못된 페이지 체크섬입니다.|
|1504|The size<%u> of the column partition file<%s> is too small. It is supposed to be greater than the size<%u>|칼럼 파티션 파일의 사이즈가 너무 작음입니다.|
|1505|The offset<%u> and size<%u> of the update value for the page<id:%u, offset:%u, size:%u> in the column partition file<%s> is invalid| 칼럼 파티션 파일의 페이지 업데이트 오프셋과 크기의 값이 유효하지 않습니다.|
|1506|The checksum<write:%#X, read:%#X> of the head of the column partition file<%s> is invalid.| 칼럼 파티션 파일 헤드 체크섬이 유효하지 않습니다.|
|1551|Error in getting the fd of the file<%s> from the fd cache.|File fd를 fd cache로부터 가져오는도중에서 오류가 발생했습니다.|
|1601|Ager thread terminated abnormally.|Ager thread가 비정상적으로 종료됩니다.|
|1631|There is no root dir<%s> for the database backup.|Database 백업을 위한 root 디렉토리가 없습니다.|
|1632|The database is not destroyed.|Database가 삭제되지 않습니다.|
|1633|Failed to write data<%u> of the backup stat file<%s>.|백업 stat 파일 write에 실패했습니다.|
|1634|Failed to read data<%u> of the backup stat file<%s>.|백업 stat 파일 read에 실패했습니다.|
|1635|The backup statfile<%s> is invalid(CRC<H:%u, B:%u, T:%u).|잘못된 백업 stat 파일입니다.|
|1636|The backup <%s> is not completed.|백업이 완료되지 않습니다.|
|1637|The backup <%s> has already exist.|백업이 이미 존재합니다.|
|1638|The end rid<%llu> of the table<%llu> in the restored database is invalid.| 복원된 database 테이블의 END RID가 유효하지 않습니다.|
|1639|The name<%s> of backup is too long, errno = %d.|너무 긴 백업 이름입니다.|
|1640|The backup file<%s> already exists.|백업파일이 이미 존재합니다.|
|1641|The backup file<%s> has the invalid magic string<%s>.|백업파일의 매직문자가 유효하지 않습니다.|
|1642|The header of backup file<%s> has the invalid crc32<%u>.|백업파일 헤더가 유효하지 않은 crc32 값을 가짐입니다.|
|1643|Length<%u> of backup file<%s> is too long.|너무 큰 백업파일입니다.|
|1644|The page size <%u> of backup file<%s> is invalid.|백업파일의 페이지 크기 유효하지 않습니다.|
|1645|The file size <%llu> of the head is different from the size<%llu> on the disk.|head의 파일 크기가 디스크의 파일 크기와 다름입니다.|
|1646|The backup file is invalid since the backup is not completed.|백업 미완료로 인한 잘못된 백업파일입니다.|
|1647|Incremental backup should be preceded by the last backup.|증분백업은 기존 백업에 이어서 수행해야 합니다.|
|1648|Backup targets are different from that of previous target.|백업 target이 기존 target과 다름입니다.|
|1701|The tablespace<%s> is still referenced by other objects such as tables and indexes.|Tablespace가 다른 테이블과 인덱스 객체등에 의해 참조되고 있습니다.|
|1702|The tablespace<%s> does not exist in the database.|Tablespace가 database에 존재하지 않습니다.|
|1703|The SYSTEM_TABLESPACE cannot be dropped.|YSTEM_TABLESPACE는 drop할 수 없습니다.|
|1704|Tablespace already exists. <%s>|Tablespace가 이미 존재합니다.|
|1705|The dir<%s> for the tablespace<%s> of datadisk<%s> already exists.|Tablespace에 디스크가 이미 존재합니다.|
|1706|Disk<%s> does not exist in the tablespace<%s>.|디스크가 table space에 존재하지 않습니다.|
|1707|The parallel I/O of a disk should be between %d and %d.|디스크의 병렬 I/O 값이 허용된 범위 밖에 있습니다.|
|1708|Failed to read <%ld> bytes from the file<%s>, errno = %d.|파일 read에 실패했습니다.|
|1709|The page<offset:%u, size:%u> of the file<%s> is invalid because it has the invalid timestamp<head:%lld, tail:%lld>|유효하지 않은 파일 페이지 timestamp값입니다.|
|1710|The page<offset:%u, size:%u> of the file<%s> is invalid because it has the invalid crc<memory:%u, disk:%u>|유효하지 않은 파일 페이지 CRC값입니다.|
|1711|Failed to create directory<%s> for virtual disk.|Virtual disk를 위한 디렉토리 생성에 실패했습니다.|
|1712|Failed to allocate memory for directory to be removed.|디렉토리 삭제를 위한 메모리 할당에 실패했습니다.|
|1801|Error in waiting to read value: value offset<%lld>, value size<%u>, and file<%s>|값을 읽는 동안에서 오류가 발생했습니다.|
|1821|The image in the DWFile<%s> is invalid.|잘못된 DW 파일 이미지가입니다.|
|1841|The operation is aborted by ART.|작업이 ART(Automatic Recovery Test)에 의해 중단됩니다.|
|1851|Variable length columns are not allowed in tag table.|TAG 테이블에서는 variable length 칼럼이 허용되지 않습니다.|
|1852|Another deletion is in progress for table <%llX>.|이미 수행중인 삭제 프로세스가 있습니다.|
|1853|Cannot create append file for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 append 파일을 생성 할 수 없습니다.|
|1854|Cannot sync append file for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 append 파일을 sync 할 수 없습니다.|
|1855|Cannot close append file for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 append 파일을 close 할 수 없습니다.|
|1856|Cannot create data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 데이터 파일을 생성 할 수 없습니다.|
|1857|Cannot open data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 데이터 파일을 open 할 수 없습니다.|
|1858|Cannot read data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 데이터 파일을 read 할 수 없습니다.|
|1859|Cannot write data file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 데이터 파일에 write 할 수 없습니다.|
|1860|Data file <%llX> is corrupted for Key-Value table <%llX>.|keyvalue 테이블의 데이터 파일 손상입니다.|
|1861|Cannot create index file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 인덱스 파일을 생성 할 수 없습니다.|
|1862|Cannot open index file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 인덱스 파일을 open 할 수 없습니다.|
|1863|Cannot read <.%s> file <%llX> for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 파일을 read 할 수 없습니다.|
|1864|Cannot write <.%s> file <%llX> for Key-Value table <%llX>, errno = %d.| keyvalue 테이블의 파일에 write 할 수 없습니다.|
|1865|Index file <%llX> is corrupted for Key-Value table <%llX>.|keyvalue 테이블의 인덱스 파일 손상입니다.|
|1866|Cannot perform I/O for Key-Value table <%llX>.|keyvalue 테이블에 대해 I/O 작업을 수행할 수 없습니다|
|1867|Invalid path to append file for Key-Value table <%llX>, errno = %d.|잘못된 keyvalue 테이블 append 파일 경로입니다.|
|1868|Cannot open append file for Key-Value table <%llX>, errno = %d.|keyvalue 테이블의 append 파일을 open 할 수 없습니다.|
|1869|RID-based SELECT is not allowed without datafile, Table<%llX>/RID<%llu>.|데이터 파일이 없으면 RID 기반 SELECT가 허용되지 앖음입니다.|
|1870|Cannot open append file for mounted Key-Value table <%llX>, errno = %d.|마운트된 keyvalue 테이블의 append 파일을 open 할 수 없습니다.|
|1871|Cannot read append file for mounted Key-Value table <%llX>, errno = %d.|마운트된 keyvalue 테이블의 append 파일을 read 할 수 없습니다.|
|1872|Another backup is in progress for table <%llX>.|이 테이블에 대한 백업이 진행중입니다입니다.|
|1873|No index-file <%llx> for Key-Value table Table<%llX>.|keyvalue 테이블을 위한 인덱스파일이 없습니다.|
|1874|Cannot open file <%llX> for Key-Value table <%llX> path<%s>, errno = %d.|keyvalue 테이블 파일 open에 실패했습니다.|
|1875|Cannot find unpurged node for Key-Value table <%llX>.|keyvalue 테이블에서 purge되지 않은 node를 찾을 수 없습니다.|
|1876|Fail to %s decompress file <%llX> for key-value table<%llx>, error = %d|keyvalue 테이블 파일 압축해제에 실패했습니다.|
|1877|Tag stat for id[%llu] is not found.|ID에 대한 Tag stat 이 없습니다.|
|1878|Cannot write stat file for Key-Value table <%llX> path<%s> errno = %d.|keyvalue 테이블 stat 파일 write에 실패했습니다.|
|1879|Cannot read stat file for Key-Value table <%llX> path<%s> errno = %d.|keyvalue 테이블 stat 파일 read에 실패했습니다.|
|1880|Cannot open stat file for Key-Value table <%llX> path<%s>, errno = %d.|keyvalue 테이블 stat 파일 open에 실패했습니다.|
|1881|Stat File Invalid TableID[%llu], TablePath[%s].|잘못된 stat파일입니다.|
|1882|No kvindex-file <%llx> for Key-Value table Table<%llX>.|이 테이블을 위한 kvindex 파일이 없습니다.|
|1883|Value of the time column(<%lld>) must be greater than or equal to <%lld>.|잘못된 시간 칼럼 값입니다.|
|1884|keyvalue table<%llx> thread for [%s] stopped.|keyvalue 테이블 thread 종료됩니다.|
|1885|Data row value is corrupted: required RID<%llu>, value RID<%llu>.|Data row 값 손상입니다.|
|1886|%s varchar data is corrupted: required VRID<%u>, value VRID<%u>.|Varchar 데이터 손상입니다.|
|1900|Snapshot ID <%s> is invalid.|잘못된 snapshot ID입니다.|
|1901|Cannot snapshot with no table.|존재하지 않는 테이블에 snapshot을 사용할 수 없습니다.|
|1902|Snapshot timed out.|Stanpshot 시간 초과입니다.|
|1903|Snapshot ID <%s> does not exist.|Snapshot ID가 존재하지 않습니다.|
|1904|Snapshot ID <%s> already exists.|Snapshot ID가 이미 존재합니다.|
|1910|Cannot freeze with no table.|존재하지 않는 테이블을 동결할 수 없습니다.|
|1911|Snapshot already frozen.|Snapshot이 이미 동결된 상태임입니다.|
|1951|Failed to call function <%s>, errno=%d|함수호출에 실패했습니다.|
|1952|Table (0x%llx) resource busy (%s).|테이블 자원이 부족합니다.|
|2000|Memory allocation error, Error code = %d|메모리 할당 오류가 발생했습니다.|
|2001|Error in opening meta.|meta open 중에서 오류가 발생했습니다.|
|2002|Error in executing meta.|meta 실행 중에서 오류가 발생했습니다.|
|2003|Error in closing meta.|meta close 중에서 오류가 발생했습니다.|
|2004|Error in creating hash. (errno=%d)|해시 생성 중에서 오류가 발생했습니다.|
|2005|Error in allocating memory.|메모리 할당 중에서 오류가 발생했습니다.|
|2006|Error in adding hash. (errno=%d)|해시 추가 중에서 오류가 발생했습니다.|
|2007|Error in fetching meta.|meta fetch 중에서 오류가 발생했습니다.|
|2008|Error in traversing hash.|해시 탐색 중에서 오류가 발생했습니다.|
|2009|Insufficient parser memory.|충분하지 않은 파서 메모리입니다.|
|2010|Syntax error: near token (%s).|구문 오류가 발생했습니다.|
|2011|Unrecognized token (%s).|인식할 수 없는 토큰입니다.|
|2012|Single row error. Single-row subquery returns more than one row. (NOT USED)|단일 row 오류. 단일 row 서브쿼리가 1개 이상의 행을 반환. (NOT USED)입니다.|
|2013|A GROUP BY clause is required before HAVING.|HAVING 절 앞에 GROUP BY 절이 필요합니다.|
|2014|Column name is duplicated: (%s).|칼럼이름 중복입니다.|
|2015|Invalid column type: (%s).|잘못된 칼럼 타입입니다.|
|2016|Table property (%s) does not exist.|테이블 property가 존재하지 않습니다.|
|2017|Error in converting table property. Cannot convert string (%s) to integer.|테이블 property 변환 오류. 문자열을 정수로 변환할 수 없습니다.|
|2018|Table property value is out of range: (%s).|테이블 property 값 범위 초과입니다.|
|2019|Column size should be specified on a variable column type.|Variable 칼럼 타입에 대해서만 칼럼 크기를 지정해야 합니다.|
|2020|Invalid size specified. Cannot specify type size to (%s).|잘못된 크기 지정입니다.|
|2021|Cannot create bitmap index on data type (%s)|데이터타입에 비트맵인덱스 생성할 수 없습니다.|
|2022|Cannot create keyword index on data type (%s)|데이터타입에 키워드인덱스 생성할 수 없습니다.|
|2023|snprintf function error (%d).|snprintf 함수 오류가 발생했습니다.|
|2024|Table %s already exists.|테이블이 이미 존재합니다.|
|2025|Table %s does not exist.|테이블이 존재하지 않습니다.|
|2026|The number of insert values and that of columns are mismatched.|입력 값의 수와 칼럼의 수 불일치입니다.|
|2027|Error in table insert column integer conversion. Insert value conversion to integer error (%s).|테이블 입력 칼럼의 정수 변환 오류. 정수로 변환하는 값 입력 오류가 발생했습니다.|
|2028|Error in table insert column double conversion. Insert value conversion to double error (%s)|테이블 입력 칼럼의 double 변환 오류. 값을 double로 변환하는 중에서 오류가 발생했습니다.|
|2029|Error in table insert column time format. Insert _arrival_time value conversion error.|테이블 입력 칼럼의 시간 형식 오류. _arrival_time 값 변환 중에서 오류가 발생했습니다.|
|2030|Column name (%s) does not exist.|칼럼이름이 존재하지 않습니다.|
|2031|Resource busy (%s).|자원이 부족합니다.|
|2032|Type conversion error: error occurred while comparing the values of type (%s) and type (%s).|타입 변환 오류: 타입의 값을 비교하는 동안에서 오류가 발생했습니다.|
|2033|Cannot concatenate non varchar types.|VARCHAR가 아닌 타입은 연결할 수 없습니다.|
|2034|Invalid format of time expression.|잘못된 시간 표현식 형식입니다.|
|2035|Function [%s] does not exist.|함수가 존재하지 않습니다.|
|2036|Function [%s] argument is mismatched.|함수의 인수 데이터 불일치입니다.|
|2037|Function [%s] argument data type is mismatched.|함수의 인수 데이터 타입 불일치입니다.|
|2038|Table [%s] does not exist.|테이블이 존재하지 않습니다.|
|2039|No table specified in the target list.|대상 목록에 지정된 테이블이 없습니다.|
|2040|Invalid time range.|잘못된 시간범위입니다.|
|2041|Time value must be positive.|시간값은 양수이어야 합니다.|
|2042|Expression cannot have a NULL value.|표현식에 NULL 값을 사용할 수 없습니다.|
|2043|Group function is not allowed here.|Group함수가 허용되지 않습니다.|
|2044|Not a GROUP BY expression.|GROUP BY 표현식이 아님입니다.|
|2045|Type is not supported(typecode is %u). Internal error.|타입이 지원되지 않습니다.|
|2046|String buffer is not enough.|문자열 Buffer가 부족합니다.|
|2047|Lock buffer is not enough. Table counts are too many.|Lock buffer가 부족합니다. 테이블 수가 너무 많음입니다.|
|2048|Bind parameter count is overflowed. (max=%u)|Bind 매개변수 수 초과입니다.|
|2049|Cannot apply bind parameter.|Bind 매개변수를 적용할 수 없습니다.|
|2050|Bind data from client is corrupted.|클라이언트에서 bind 된 데이터 손상입니다.|
|2051|Bind data type unknown (typecode is %u).|알 수 없는 bind 데이터 타입입니다.|
|2052|Cannot insert data into this table (%s).|이 테이블에 데이터를 입력할 수 없습니다.|
|2053|Failed to convert type (%s) to type (%s).|타입 변환에 실패했습니다.|
|2054|Aggregation error on function usage (NOT USED)|함수 사용에 대한 집계 오류 (NOT USED)입니다.|
|2055|Invalid insert value.|잘못된 입력 값입니다.|
|2056|Column name (%s) not found.|칼럼이름을 찾을 수 없습니다.|
|2057|Only literal type can be used in SEARCH keyword.|SEARCH 키워드에는 리터럴 타입만 사용할 수 있습입니다.|
|2058|Index %s already exists|인덱스가 이미 존재합니다.|
|2059|Index %s does not exist|인덱스가 존재하지 않습니다.|
|2060|Composite index is not supported.|composite 인덱스 지원 안됩니다.|
|2061|Cannot divide a value by zero.|값을 0로 나눌 수 없습니다.|
|2062|Cannot calculate date type.|날짜타입은 계산할 수 없습니다.|
|2063|Invalid search type. Search type must be VARCHAR.|못된 검색 타입. 검색 타입은 VARCHAR 이어야 합니다.|
|2064|Invalid time format. (format: \"year/mon/day hour:min:sec\")|잘못된 시간 형식. (format: \"year/mon/day hour:min:sec\")입니다.|
|2065|Index property (%s) dose not exist.|인덱스 property가 존재하지 않습니다.|
|2066|Invalid index property value: (%s).|잘못된 인덱스 property 값입니다.|
|2067|Error in TO_ADDR4 function aggregate. Argument type to TO_ADDR4 function must be an integer.|TO_ADDR4 함수 집계에서 오류 발생. TO_ADDR4 함수의 인수 타입은 정수이어야 합니다.|
|2068|Invalid IPv4 address format (%s).|잘못된 IPv4 주소 형식입니다.|
|2069|%s index can only be created for %s table.|인덱스가 특정 테이블에서만 생성될 수 있습니다.|
|2070|Search predicate needs keyword index.|검색 조건에 키워드 인덱스가 필요합니다.|
|2071|Only one index is allowed for a single column.|단일 칼럼에 단 1개의 인덱스만 허용됩니다.|
|2072|Cannot delete data from this table (%s).|이 테이블에서 데이터를 삭제할 수 없습니다.|
|2073|Invalid DELETE condition. %s|잘못된 DELETE 조건입니다.|
|2074|Invalid delete time range. BEFORE time range should be older than present.|잘못된 delete 시간 범위. BEFORE 시간 범위는 현재시간보다 이전이어야 합니다.|
|2075|Table(%s) record does not exist in meta database.|테이블 record가 meta database에 존재하지 않습니다.|
|2076|Table(%lld) record does not exist in meta database.|테이블 record가 meta database에 존재하지 않습니다.|
|2077|Invalid %s size. %s type size cannot be more than %d.|유효하지 않은 size입니다.|
|2078|Invalid statement type. Statement type(%d) is unsupported.|유효하지 않은 statement 타입. 지원되지 않는 statement 타입입니다.|
|2079|The number of function (%s) arguments is not matched.|함수의 인수개수 불일치입니다.|
|2080|User (%s) does not exist.|사용자가 존재하지 않습니다.|
|2081|Invalid username/password.|잘못된 사용자이름 및 패스워드입니다.|
|2082|User (%s) already exists.|사용자가 이미 존재합니다.|
|2083|You cannot drop yourself(%s).|사용자 스스로 자신을 드랍할 수 없습니다.|
|2084|User drop error. This user's tables still exist. Drop those tables first.|사용자 드랍 오류. 이 사용자의 테이블이 아직 존재합니다. 테이블 드랍을 먼저해야 합니다.|
|2085|The user(%s) does not have alter privileges.|사용자가 변경 권한이 없습니다.|
|2086|The user(%s) does not have connect privileges.|사용자가 연결 권한이 없습니다.|
|2087|The user does not have access privileges on table(%s.%s).|사용자가 테이블에 대한 접근 권한이 없습니다.|
|2088|Error in altering table. Only the LOG table can be altered.|테이블 변경 중 오류 발생. LOG테이블만 변경 가능합니다.|
|2089|Error in altering table. Column name(%s) already exists.|테이블 변경 중 오류 발생. 칼럼 이름이 이미 존재합니다.|
|2090|Error in altering table. Only varchar type can be modified.|테이블 변경 중 오류 발생. varchar타입만 변경이 가능합니다.|
|2091|Error in altering table. Varchar length should be greater than previous value length|테이블 변경 중 오류 발생. varchar 길이는 이전 값보다 커야 합니다.|
|2092|Error in altering table. Column (%s) cannot be dropped.|테이블 변경 중 오류 발생. 칼럼을 드랍할 수 없습니다.|
|2093|Error in altering table. Column (%s) having index cannot be dropped.|테이블 변경 중 오류 발생. 인덱스가 있으면 드랍할 수 없습니다.|
|2094|Error in altering table. Column (%s) already exists.|테이블 변경 중 오류 발생. 칼럼이 이미 존재합니다.|
|2095|Error in truncating table. Only the LOG table can be truncated.|테이블을 truncate 중 오류 발생. LOG테이블만 truncate할 수 있습니다.|
|2096|Error in truncating table. Table %s does not exist.|테이블을 truncate 중 오류 발생. 테이블이 존재하지 않습니다.|
|2097|Error in altering table. The table must have at least one column.|테이블 변경중 오류 발생. 테이블에 최소한 하나의 열이 있어야 합니다.|
|2098|Error in joining tables. Only equi-join is allowed.|테이블 조인 오류 발생. 동등 조인만 허용됩니다.|
|2099|Error in joining tables. The OR condition for a join predicate is not allowed.|테이블 조인 오류 발생. 조인 조건에서 OR 조건은 허용되지 않습니다.|
|2100|Error in joining tables. The join predicate cannot use functions.|테이블 조인 오류 발생. 조인 조건에 함수를 사용할 수 없습니다.|
|2101|Error in joining tables. Cannot join without join predicate.|테이블 조인 오류 발생. 조인 조건 없이 조인할 수 없습니다.|
|2102|Collector (%s.%s) does not exist.|Collector가 존재하지 않습니다.|
|2103|The collector (%s.%s) already exists.|Collector가 이미 존재합니다.|
|2104|The template file (%s) does not exist.|템플릿파일이 존재하지 않습니다.|
|2105|The template format (%s : %s : %d) is invalid.|잘못된 템플릿 형식입니다.|
|2106|The collector (%s.%s) is already running.|Collector가 이미 실행중입니다입니다.|
|2107|The collector (%s.%s) is not running.|Collector가 실행중이 아닙니다.|
|2108|Error in loading collector template. The value (%s) is invalid.|Collector 템플릿 로드중 오류 발생. 값이 유효하지 않습니다.|
|2109|Cannot join two or more LOG tables.|두 개 이상의 LOG 테이블을 조인할 수 없습니다.|
|2110|Search condition argument is too short. It needs more than (%d) characters.|검색 조건 인자는 너무 짧음입니다.|
|2111|Invalid option.|잘못된 옵션입니다.|
|2112|Cannot use DISTINCT with GROUP BY clause.|DISTINCT를 aggregation GROUP BY 절과 같이 쓸 수 없습니다.|
|2113|Cannot use DISTINCT with aggregation function.|DISTINCT를 aggregation 함수와 같이 쓸 수 없습니다.|
|2114|DISTINCT clause is not allowed here.|DISTINCT 절은 허용되지 않습니다.|
|2115|Internal column cannot be modified.|내부 칼럼은 변경할 수 없습니다.|
|2116|Search predicate must use an index.|검색 조건은 인덱스를 사용해야 합니다.|
|2117|DDL on table (%s) is forbidden.|이 테이블에 대한 DDL이 금지됩니다.|
|2118|Lock object was already initialized. (Do not use select and append simultaneously in single session.)|잠금 객체가 이미 초기화됩니다. (단일 세션에서 select와 append를 동시에 사용하면 안됩니다.)입니다.|
|2119|This functionality has not been implemented.|구현되지 않은 기능입니다.|
|2120|Invalid session ID (%s).|잘못된 세션ID입니다.|
|2121|No privileges to kill the session.|세션을 종료할 권한이 없습니다.|
|2122|No privileges to cancel the session.|세션을 취소할 권한이 없습니다.|
|2123|Table id (%lld) does not exist in meta database.|테이블ID가 meta database에 존재하지 않습니다.|
|2124|Column id (%llu) does not exist in table (%llu).|칼럼ID가 테이블에 존재하지 않습니다.|
|2125|Error in converting string (%s) to datetime with heuristic method. Check the default date string format in this session.|휴리스틱 방법으로 문자열을 날짜/시간으로 변환하는 중 오류 발생. 이 세션에서 기본 날짜 문자열 형식을 확인 필요합니다.|
|2126|ORDER BY clause is not allowed in a subquery|ORDER BY 절은 서브쿼리에서 허용되지 않습니다.|
|2127|Only integer constants must be used for ORDER BY column position.|ORDER BY 열 위치에는 정수 상수만 사용해야 합니다.|
|2128|ORDER BY column position %d is out of range - should be between 1 and %d.|ORDER BY 열 위치가 범위를 벗어남입니다.|
|2129|GROUP BY terms must be integer constants|GROUP BY 절의 term은 정수 상수여야 합니다.|
|2130|A GROUP BY clause is required before HAVING|HAVING 절 전에 GROUP BY 절이 필요합니다.|
|2131|Single row error. Single-row subquery returns more than one row.|단일 row 오류. 단일 row 서브쿼리가 1개 이상의 row를 반환입니다.|
|2132|Cannot use subquery on HAVING, ORDER BY and GROUP BY clauses.|HAVING, ORDER BY 및 GROUP BY 절에서 서브쿼리를 사용할 수 없습니다.|
|2133|Invalid subquery.|잘못된 서브쿼리입니다.|
|2134|Too many REGEXP in WHERE clause. No more than %d REGEXP in WHERE clause.|WHERE 절에 REGEXP가 너무 많음. WHERE 절에 설정값 이상의 REGEXP를 사용할 수 없습니다.|
|2135|WHERE clause has to return a boolean result.|WHERE 절은 boolean 결과를 반환해야 합니다.|
|2136|Invalid tablespace type.|잘못된 tablespace 타입입니다.|
|2137|There are too many disks<%ud> for tablespace %s.|Table space에 디스크가 너무 많음입니다.|
|2138|The PARALLEL_IO value<%d> for the disk<%s> must be higher than <%d>.|디스크의 PARALLEL_IO 값이 더 높아야 합니다.|
|2139|MINMAX CACHE is not allowed for VARCHAR column(%s).|VARCHAR 칼럼에서는 MINMAX CACHE를 사용할 수 없습니다.|
|2140|This type of tables do not support the tablespace functionality.|이 타입의 테이블은 tablespace 기능을 지원하지 않습니다.|
|2141|Type comparison error.|타입 비교 오류가 발생했습니다.|
|2142|Cannot use lob type in the GROUP BY clause.|GROUP BY 절에서 LOB 타입을 사용할 수 없습니다.|
|2143|Cannot use lob type in the ORDER BY clause.|ORDER BY 절에서 LOB 타입을 사용할 수 없습니다.|
|2144|Outerjoin permits only 2 tables.|외부 조인은 2개 테이블만 허용됩니다.|
|2145|The string cannot be converted to number value.(%s)|문자열을 숫자 값으로 변환할 수 없습니다.|
|2146|Cannot join tables with timeseries function.|타임 시리즈 함수와 함께 테이블을 조인할 수 없습니다.|
|2147|Cannot use inline view with timeseries function.|타임 시리즈 함수와 함께 인라인 뷰를 사용할 수 없습니다.|
|2148|Invalid IPv6 address format.(%s)|잘못된 IPv6 주소 형식입니다.|
|2149|Error in executing CONTAINS. Cannot convert from type(%d) to type(%d).|CONTAINS 실행 중 오류 발생. 타입을 변환할 수 없습니다.|
|2150|Network type error. Network Mask length does not match with the column's length.(mask=%s, column=%s)|네트워크 타입 오류. 네트워크 마스크 길이가 칼럼의 길이와 일치하지 않습니다.|
|2151|Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.|Tablespace 에 디스크 추가 중 오류 발생. 유효한 라이선스 없이 tablespace에 복수의 디스크를 사용할 수 없습니다.|
|2152|Error in setting column property. You should specify a positive value of column property PARTITION_PAGE_COUNT as well as PAGE_VALUE_COUNT.|칼럼 property 설정 중 오류 발생. PARTITION_PAGE_COUNT 및 PAGE_VALUE_COUNT은 양수 값 지정가 필요합니다.|
|2153|Wrong column property name(%s). You should specify a valid property name.|잘못된 칼럼 property 이름. 유효한 property 이름 지정가 필요합니다.|
|2154|Select set operator parsing error.|select set연산자 파싱 오류가 발생했습니다.|
|2155|Only UNION ALL set operator is supported.|UNION ALL set 연산자만 지원됩니다.|
|2156|Set operator column types are mismatched on (%d)th column.|SET 연산자 열타입이 일치하지 않습니다.|
|2157|Internal error on validating query|쿼리 유효성 검사 중 내부에서 오류가 발생했습니다.|
|2158|Error in evaluating data type. You must specify a valid data type.|데이터 타입 평가 중 오류 발생. 유효한 데이터 타입 지정가 필요합니다.|
|2159|FROM DATETIME' must be earlier than 'TO DATETIME'.|'FROM DATETIME'은 'TO DATETIME'보다 이른 시간이어야 합니다.|
|2160|Error in doing unmount table(%s). You can unmount only mounted tables.| 테이블 마운트 해제 중 오류 발생. 마운트된 테이블만 마운트 해제할 수 있습니다.|
|2161|Error in executing DDL. You cannot execute DDL with mounted DB. (*NOT USED*)|DDL 실행 중 오류 발생. 마운트된 database에서는 DDL을 실행할 수 없습니다. (*NOT USED*)입니다.|
|2162|Error in doing unmount DB. You cannot umount database which is not mounted.|Database 마운트 해제 중 오류 발생. 마운트되지 않은 database는 해제할 수 없습니다.|
|2163|Invalid directory path (%s). You should specify a valid path.|잘못된 디렉토리 경로. 경로를 지정해야 합니다.|
|2164|Invalid index property. Property (%s) for index cannot be altered.|잘못된 인덱스 property. 인덱스에 대한 peroperty는 변경할 수 없습니다.|
|2165|Function (%s) is not allowed here.|함수가 허용되지 않습니다.|
|2166|Cannot use ORDER BY clause with aggregation function.|Aggregation 함수와 함께 ORDER BY 절을 사용할 수 없습니다.|
|2167|GROUP_CONCAT function error. Separator should be a string constant.|GROUP_CONCAT 함수 오류. 구분자는 문자열 상수여야 합니다.|
|2168|Operator argument count or type is mismatched.|연산자 인수의 개수나 유형이 일치하지 않습니다.|
|2169|Invalid column property value: (%s)|잘못된 칼럼 속성 값입니다.|
|2170|Every specified table or inline view in FROM clause must have its own alias.|FROM 절에 지정된 각 테이블 또는 인라인 뷰는 고유한 별칭을 가져야 합니다.|
|2171|VOLATILE / LOOKUP table cannot have more than one primary key.|VOLATILE / LOOKUP 테이블은 기본 키를 둘 이상 가질 수 없습니다.|
|2172|Primary key is allowed only for VOLATILE / LOOKUP table.|기본 키는 VOLATILE / LOOKUP 테이블에서만 허용됩니다.|
|2173|Cannot create columns with data type (%s) in VOLATILE / LOOKUP table.|VOLATILE / LOOKUP 테이블에서 데이터 타입으로 칼럼을 생성할 수 없습니다.|
|2174|The index already exists in the column(%s).|인덱스가 이미 칼럼에 존재합니다.|
|2175|SET clause must be written as a list of 'column = value' expression.|SET 절은 '열 = 값' 표현식의 목록으로 작성되어야 합니다.|
|2176|Cannot update primary key column in SET clause.|SET 절에서 기본 키 칼럼을 업데이트할 수 없습니다.|
|2177|ON DUPLICATE UPDATE clause is allowed only in LOOKUP / VOLATILE table.|ON DUPLICATE UPDATE 절은 LOOKUP / VOLATILE 테이블에서만 허용됩니다.|
|2178|Error in updating table. Column name (%s) does not exist in this table.|테이블 업데이트 중 오류 발생. 칼럼이름이 이 테이블에 존재하지 않습니다.|
|2179|INSERT on a %s table without primary key value cannot be proceeded.|기본 키 값 없이 테이블에 입력할 수 없습니다.|
|2180|Primary key is mandatory for UPDATE.|UPDATE시 기본 키가 필수임입니다.|
|2181|Invalid index name starting with (%s) which is the same as primary key index.|기본 키 인덱스와 동일하게 시작하는 잘못된 인덱스 이름입니다.|
|2182|You cannot drop the primary key index (%s).|Primary key index를 drop할 수 없습니다.|
|2183|Append mode for table (%s) is not supported.|이 테이블에서 Append mode가 지원되지 않습니다.|
|2184|Specified property value is invalid in %s table.|테이블에서 지정된 property 값이 잘못됩니다.|
|2185|Invalid database name. This database name is already used for mount.|잘못된 database 이름. 이 Database 이름이 이미 마운트를 위해 사용되고 있습니다.|
|2186|Invalid database name.|잘못된 database 이름입니다.|
|2187|Error in unmounting database. Some tables in mounted database are accessed by other transactions|Database 마운트 해제 중 오류 발생. 다른 트랜잭션에서 마운트된 database의 일부 테이블을 참조하고 있습니다.|
|2188|The database is not mounted.|Database가 마운트되지 않습니다.|
|2189|Error in deleting rows. Only rows in VOLATILE / LOOKUP table can be deleted.|ROW 삭제 중 오류가 발생했습니다. VOLATILE / LOOKUP 테이블의 ROW만 삭제 가능합니다.|
|2190|Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)|잘못된 UPDATE/DELETE 조건. (기본 키 열) = (값)으로 지정입니다.|
|2191|WHERE clause in DELETE statement is not supported yet.|DELETE 문에서 WHERE 절은 아직 지원되지 않습니다.|
|2192|Index type for keyword index only supports keyword bitmap or keyword LSM.|키워드 인덱스의 인덱스 유형은 키워드 비트맵 또는 키워드 LSM만 지원합니다.|
|2193|Error in creating collector. The regular expression file (%s) does not exist.|Collector 생성 오류. 정규식 파일이 존재하지 않습니다.|
|2194|Error in creating collector. The regular expression file path has not specified.|Collector 생성 오류. 정규식 파일경로가 지정되지 않습니다.|
|2195|Buffer size insufficient.|Buffer size가 충분하지 않습니다.|
|2196|Error in loading data. File (%s) does not exist.|데이터 로드중 오류 발생. 파일이 존재하지 않습니다.|
|2197|Error in loading data with automatic mode. The table (%s) already exists.|자동모드로 데이터 로드중 오류 발생. 테이블이 이미 존재합니다.|
|2198|Error in loading data. The table (%s) doesn't exists.|데이터 로드중 오류 발생. 테이블이 존재하지 않습니다.|
|2199|CSV parsing error occurred in %d line: [%s]|CSV파싱중에서 오류가 발생했습니다.|
|2200|[%s] is not valid string terminator or encloser.|유효한 문자열 종결자 또는 인클로저가 아님입니다.|
|2201|The automatic loading mode is invalid.|자동 로딩 모드가 유효하지 않습니다.|
|2202|The automatic column detection has been failed. No data or invalid headers.|자동 칼럼 감지 실패. 데이터가 없거나 잘못된 헤더임입니다.|
|2203|Invalid encoding.|잘못된 인코딩입니다.|
|2204|Failed to convert %s to UTF8.|UTF8로 변환에 실패했습니다.|
|2205|A modulo operator can be applied only for integer types.|모듈로 연산자는 정수 타입에만 적용 가능합니다.|
|2206|Tablespace name cannot be specified in non automode|비자동 모드에서는 table space 이름을 지정할 수 없습니다.|
|2207|Error in saving table into file (%s). File already exists.|테이블을 파일로 저장중 오류 발생. 이미 존재하는 파일입니다.|
|2208|Expression argument type is mismatched.|표현식 인수 타입 불일치입니다.|
|2209|Error in connecting to collector manager. The collector manager (%s:%d) doesn't exists.| Collector manager 연결중 오류 발. Collector manger가 존재하지 않습니다.|
|2210|Error in executing CREATE command. The collector manager (%s) returns error.|CREATE command 실행 중 오류 발생. Collector manager 가 오류 반환입니다.|
|2211|Error in executing DROP command. The collector manager (%s) returns error.|DROP command 실행 중 오류 발생. Collector manager 가 오류 반환입니다.|
|2212|Error in running collector manager. The collector manager (%s) is already running.|Collector manager 실행 중 오류 발생. Collector manager가 이미 실행 중입니다.|
|2213|Error in stopping collector manager. The collector manager (%s) is not running.|Collector manager 중지중 오류 발생. Collector manager가 실행 중이 아닙니다.|
|2214|Error in starting collector manager. The collector manager (%s) is already started.|Collector manager 시작 중 오류 발생. Collector manager가 이미 실행 중입니다.|
|2215|Error in starting command execution. The collector manager (%s) returns error.|명령 실행 시작 중 오류 발생. Collector manager 가 오류 반환입니다.|
|2216|Error in executing collector CREATE command. The collector (%s.%s) returns error.|Collector 생성 명령 실행 중 오류가 발생. Collector 가 오류 반환입니다.|
|2217|Error in receiving meta data from collector manager (%s-%s:%d).|Collector manger로부터 메타 데이터를 수신하는 중 오류가 발생입니다.|
|2218|Collector manager (%s) does not exist.|Collector manager가 없습니다.|
|2219|Error in creating collector manager. The collector manager (%s) already exists.|Collector manager 생성 오류. Collector manager가 이미 존재합니다.|
|2220|Error in executing command. The collector manager (%s) returns error.|명령 실행 중 오류가 발생. Collector manager가 오류 반환입니다.|
|2221|Manager name is not specified.|Manager이름이 지정되지 않습니다.|
|2222|Error in read protocol. Send %s protocol, but received %d protocol.|프로토콜 read 에러가 발생했습니다.|
|2223|Unable to establish connection with collectormanager (%s).|collector manager와 연결을 할 수 없습니다.|
|2224|Manager name is not specified.|Manager이름이 지정되지 않습니다.|
|2225|Invalid set column unit.|잘못된 칼럼 단위 설정입니다.|
|2226|Invalid character ('%c').|잘못된 문자입니다.|
|2227|The collector source (%s.%s) already exists.|Collector 소스가 이미 존재합니다.|
|2228|Invalid procedure (%s).|잘못된 프로시저입니다.|
|2229|Invalid argument value for function (%s).|함수에 대한 잘못된 인수값입니다.|
|2230|Wrong number of arguments in call to '%s'.|함수 호출 시 함수 인수 개수가 잘못됩니다.|
|2231|strcpy function error (%d).|strcpy함수 오류가 발생했습니다.|
|2232|Calculation argument type (%s), (%s) error.|계산인자타입 오류가 발생했습니다.|
|2233|Error occurred at column (%u): (%s)|칼럼에서에서 에러가 발생했습니다.|
|2234|Set operator columns counts are mismatched by %d and %d.|Operator 칼럼 수 불일치입니다.|
|2235|SERIES BY clause is not allowed here.|SERIES BY 절이 허용되지 않습니다.|
|2236|For a table list in FROM clause, The number of tables should be less than 32.|FROM 절의 테이블 목록에서 테이블 수는 32개 미만이어야 합니다.|
|2237|The index <%s> is not an index for the table <%s>.|인덱스가 이테이블을 위한 인덱스가 아님입니다.|
|2238|This type of join is not allowed.|이런 타입의 조인은 허용되지 않습니다.|
|2239|Invalid use of aggregation function.|잘못된 aggregation 함수 사용입니다.|
|2240|Cannot fetch column with type (%s).|이 타입의 칼럼을 fetch할 수 없습니다.|
|2241|Join between LOG table and fixed table is not supported in Cluster Edition.|Cluster edtion 에서는 LOG 테이블과 fixed 테이블 간의 조인이 지원되지 않습니다.|
|2242|Only equal predicate for joining LOG tables is available in Cluster Edition.|cluster edtion 에서는 LOG 테이블을 조인할 때 오직 equal predicate 만 사용할 수 있습니다.|
|2243|DELETE statement with the number of rows is not supported in Cluster Edition.|rOW 수와 함께하는 DELETE statement는 cluster edtion 에서 지원되지 않습니다.|
|2244|Allocate collector columns meta failure.|Collector 칼럼 meta 할당에 실패했습니다.|
|2245|Allocate collector column target failure.|Collector 칼럼 target 할당에 실패했습니다.|
|2246|Identifier %.*s is too long.|너무긴 식별자입니다.|
|2247|DATETIME earlier than 1970-01-01 00:00:00 (UTC) is not valid.|1970-01-01 00:00:00 (UTC) 이전의 DATETIME은 유효하지 않습니다.|
|2248|Insufficient column definitions.|칼럼 정의가 충분하지 않습니다.|
|2249|Invalid DELETE condition.|잘못된 DELETE 조건입니다.|
|2250|You cannot execute DDL on compoment table/index of TAGDATA table explictly.|TAGDATA 테이블의 구성 테이블/인덱스에 대해 DDL을 명시적으로 실행할 수 없습니다.|
|2251|You cannot define columns with duplicate flag (%s) in TAGDATA table.|TAGDATA 테이블에 중복 플래그를 가진 열을 정의할 수 없습니다.|
|2252|Invalid column type (%s) for flag (%s) in TAGDATA table.|TAGDATA 테이블의 플래그에 대한 잘못된 칼럼타입입니다.|
|2253|Mandatory column definition (PRIMARY KEY / BASETIME) is missing.|필수칼럼 정의 (PRIMARY KEY / BASETIME)가 누락됩니다.|
|2254|Column flag (%s) is only allowed for TAG table.|칼럼플래그는 TAG 테이블에서만 허용됩니다.|
|2255|Primary key of TAGDATA table is not defined in metadata.|TAGDATA 테이블의 기본 키가 metadata에 정의되어 있지 않습니다.|
|2256|Metadata column definition is allowed only in TAGDATA table.|Metadata 칼럼 정의는 TAGDATA 테이블에서만 허용됩니다.|
|2257|Metadata insertion is allowed only in TAGDATA table.|Metadata 삽입은 TAGDATA 테이블에서만 허용됩니다.|
|2258|Metadata key (%.*s) for the TAG table has already been inserted.|TAG 테이블의 metadata 키가 이미 삽입됩니다.|
|2259|Metadata of TAGDATA table is not found. (Key = %s)|TAGDATA 테이블의 metadata를 찾을 수 없습니다.|
|2260|Failed to allocate new metadata of TAGDATA table (Current Size=%llu).|TAGDATA 테이블의 새로운 metadata를 할당하는데 실패했습니다.|
|2261|You cannot insert metadata into TAGDATA table with ON DUPLICATE KEY UPDATE clause.|ON DUPLICATE KEY UPDATE 절을 사용하여 TAGDATA 테이블에 metadata를 입력할 수 없습니다.|
|2262|Direct DML on component tables of TAGDATA table is not allowed.|TAGDATA 테이블의 구성 테이블에 대한 직접적인 DML은 허용되지 않습니다.|
|2263|You can create only one TAGDATA table.|TAGDATA 테이블은 하나만 생성 할 수 있습니다.|
|2264|Cannot read a column (%s) in ROLLUP query because it is not a ROLLUP column.|ROLLUP 쿼리에서 칼럼을 읽을 수 없습니다. ROLLUP 칼럼이 아님입니다.|
|2265|Reading TAGDATA table without primary key condition is not allowed.|기본 키 조건 없이 TAGDATA 테이블을 읽는 것은 허용되지 않습니다.|
|2266|You cannot delete raw data of TAGDATA table with WHERE condition.|WHERE 조건으로 TAGDATA 테이블의 원시 데이터를 삭제할 수 없습니다.|
|2267|Primary key in TAGDATA table should be compared by '=' or 'IN' operation.|TAGDATA 테이블의 기본 키는 '=' 또는 'IN' 연산으로 비교되어야 합니다.|
|2268|Primary key in TAGDATA table should be compared with constant value.|TAGDATA 테이블의 기본 키는 상수 값과 비교되어야 합니다.|
|2269|Outerjoin on TAGDATA table is not allowed.|TAGDATA 테이블에서 외부 조인은 허용되지 않습니다.|
|2270|TAGDATA table's name should be 'TAG'.|TAGDATA 테이블의 이름은 'TAG'이어야 합니다.|
|2271|You must insert key value of TAGDATA table as constant.|TAGDATA 테이블의 키 값은 상수로 삽입해야 합니다.|
|2272|Index id (%llu) does not exist in meta database.|인덱스 ID (%llu)가 meta database에 존재하지 않습니다.|
|2273|The user does not have privileges on TAGDATA DDL.|사용자에게 TAGDATA DDL에 대한 권한이 없습니다.|
|2274|Failed to free new metadata of TAGDATA table.|TAGDATA 테이블의 새 metadata를 해제하는 데 실패했습니다.|
|2275|The INSERT SELECT statement to the TAGDATA table is not allowed in enterprise edition.|Enterprise Edition에서는 TAGDATA 테이블에 대한 INSERT SELECT 문이 허용되지 않습니다.|
|2276|Component table (%s) of TAGDATA table already exists.|TAGDATA 테이블의 구성 테이블이 이미 존재합니다.|
|2277|Table or index name that starts with '_TAG' is reserved.|_TAG로 시작하는 테이블 또는 인덱스 이름은 예약되어 있습니다.|
|2278|UPDATE statement is not allowed for %s.|UPDATE statement가 허용되지 않습니다.|
|2279|Invalid tag name insertion to TAGDATA table (name = '%s').|잘못된 tag 이름이 TAGDATA 테이블에 삽입됩니다.|
|2280|Invalid tag name insertion due to wrong bind variable.|잘못된 bind 변수로 인해 잘못된 tag 이름이 삽입됩니다.|
|2281|DURATION clause is not applicable on %s.|DURATION 절을 적용할 수 없습니다.|
|2282|The DELETE statement for table '%s' is already been executed.|테이블에 대한 DELETE statement가 이미 실행됩니다.|
|2283|IN subquery on TAGDATA table is not allowed.|TAGDATA 테이블에서 IN 서브쿼리는 허용되지 않습니다.|
|2284|Internal NULL value exists in the condition expression.|조건 표현식에 내부 NULL 값이 존재합니다.|
|2285|Internal error: %s.|내부적인 에러가 발생했습니다.|
|2286|Memory allocation failed while creating TAGDATA table. You may need to decrease TAG_DATA_PART_SIZE in machbase.conf.|TAGDATA 테이블을 생성하는 동안 메모리 할당에 실패했습니다. machbase.conf에서 TAG_DATA_PART_SIZE를 줄여야 할 수 있습니다.|
|2287|TAGDATA name value (%s) is too long.|TAGDATA table의 이름이 너무 김입니다.|
|2288|Aggregate function is expected at (%.*s).|Aggregate 함수가 예상됩니다.|
|2289|Non-constant expression is not allowed for PIVOT values.|PIVOT 값에는 비상수 표현식이 허용되지 않습니다.|
|2290|%s cannot be altered.|변경할 수 없습니다.|
|2291|Table name 'TAG' must be used for TAGDATA table.|테이블 이름 TAG는 TAGDATA table을 위해서만 사용되어야 합니다.|
|2292|The order of columns in TAGDATA table must be (PRIMARY, BASETIME, SUMMARIZED, other columns, .. ).|TAGDATA 테이블의 칼럼 순서는 (PRIMARY, BASETIME, SUMMARIZED, 기타 칼럼 등)이어야 합니다.|
|2293|Column meta for bind param[%d] is not available.|칼럼 meta parameter bind는 사용할 수 없습니다.|
|2294|JOIN more than one TAGDATA table is not supported.|1개를 초과하는 TAG table 조인은 지원되지 않습니다.|
|2295|Invalid ordinal number ID_COLUMN (%lld) and TIME_COLUMN (%lld).|잘못된 순서 번호 ID_COLUMN, TIME_COLUMN입니다.|
|2296|Interpolation requires only one BETWEEN expression.|보간 쿼리는 1개의 BETWEEN 표현식만 필요합니다.|
|2297|BETWEEN has invalid expression (%s).|잘못된 BETWEEN 표현식입니다.|
|2298|FREQUENCE must be a factor of INTERPOLATION_INTERVAL (%lld).|FREQUENCE는 보간 INTERVAL 의 배수여야 합니다|
|2299|Only BETWEEN condition is supported.|BETWEEN 조건만 지원됩니다|
|2300|Interpolation column is missing. (%s)|보간 칼럼이 누락됩니다.|
|2301|Some properties are missing for interpolation.|보간을 위한 일부 property가 누락됩니다.|
|2302|Invalid interpolation interval property: %lld.|잘못된 보간 interval property입니다.|
|2303|You must use higher ROLLUP unit.|더 높은 ROLLUP 단위를 사용가 필요합니다.|
|2304|Interpolation is not applicable on (%s).|보간을 적용할 수 없습니다.|
|2305|JOIN is not applicable for interpolation.|JSON은 보간에 적용할 수 없습니다.|
|2306|Interpolation interval value(%lld) should be less than checkpoint interval value(%lld).|보간 interval 값은 체크포인트 interval 값보다 작아야 합니다.|
|2307|Interpolation interval value(%lld) should be less than ROLLUP unit (%s).|보간 interval 값은 ROLLUP 단위보다 작아야 합니다.|
|2308|Checkpoint interval value(%lld) should be less than ROLLUP unit (%s).|체크포인트 interval 값은 ROLLUP 단위보다 작아야 합니다.|
|2309|Checkpoint interval value(%lld) should be divide by interpolation value(%lld).|체크포인트 intervale 값은 보간 값으로 나누어 떨어져야 합니다.|
|2310|Invalid interpolation checkpoint property: %lld.|잘못된 보간 체크포인트 property입니다.|
|2311|%s cannot be used in interpolation query.|보간쿼리에서 사용할 수 없습니다.|
|2312|Rollup delete can only be done on the Interpolation Tag table.|롤업 삭제는 보간 TAG 테이블에서만 수행할 수 있습니다.|
|2313|Unable to execute ROLLUP DELETE with the given range.|주어진 범위로 ROLLUP DELETE를 실행할 수 없습니다.|
|2314|Regular duration backup does not support a backup of the TAG table (Try incremental backup which permits the action on the TAG table).|정기 백업은 TAG 테이블의 백업을 지원하지 않음(TAG 테이블에 대한 작업을 허용하는 증분 백업 시도 권장)입니다.|
|2315|Snapshot is not supported.|snapshot이 지원되지 않습니다.|
|2316|Invalid expression in DURATION clause: %.*s|DURATION 절에 잘못된 표현식이 있습니다.|
|2317|Function execution failed: %s (errno=%d)|함수 실행에 실패했습니다.|
|2318|Can not connect Lookup Node|lookup node에 연결할 수 없습니다.|
|2319|Error on Lookup Node|lookup node 에러가 발생했습니다.|
|2320|Lookup Node is not ready|lookup node가 준비되지 않습니다.|
|2321|Data is not found in Lookup Node.|lokkup node에서 데이터를 찾을 수 없습니다.|
|2322|Mandatory column definition (PRIMARY KEY) is missing.|필수 칼럼(PRIMARY KEY) 정의 누락입니다.|
|2323|Table REFRESH is not applicable on %s.|테이블 리프레쉬를 적용할 수 없습니다.|
|2324|Cannot delete tagmeta. there exist data with deleted_tag key.|tagmeta를 삭제할 수 없습니다. deleted_tag 키가 있는 데이터 존재합니다.|
|2325|Integer %s type overflow.|정수형타입 overflow입니다.|
|2326|Backup/Mount is not supported.|Backup/Mount 가 지원되지 않습니다.|
|2327|Pivot is not supported in rollup query.|ROLLUP 쿼리에서는 pivot이 지원되지 않습니다.|
|2328|Cannot insert a new tag since the number of tags has exceeded MAX_TAG_COUNT(%lld).|TAG 수가 MAX_TAG_COUNT을 초과하여 새 TAG삽입는 불가능합니다.|
|2329|Cannot insert a new tag since the number of tags has exceeded TAG_COUNT_LIMIT(%lld).|TAG 수가 TAG_COUNT_LIMIT을 초과하여 새 TAG삽입는 불가능합니다.|
|2330|Mandatory column definition (ULONG / DATETIME) is missing.|필수 칼럼(ULONG / DATETIME) 정의 누락입니다.|
|2331|RANGE expression is not applicable on the table (%s).|이 테이블에 RANGE 표현식을 적용할 수 없습니다.|
|2332|Unable to create an index on the column (%s).|이 컬럼에 index를 생성할 수 없습니다.|
|2333|This column(%s) can't be more than %d.|이 칼럼은 %d개 이상 만들 수 없습니다.|
|2334|Tag Index is not yet supported.|Tag index가 아직 지원되지 않습니다.|
|2335|Failed to delete all on this table. It is recommended to use EXEC TABLE_REFRESH(%s).|테이블에서 모든 데이터 삭제 실패. EXEC TABLE_REFRESH 사용을 권장합니다.|
|2336|CASCADE option is not applicable on %s.|CASCADE 옵션을 적용할 수 없습니다|
|2337|Unable to define more than one column attribute (%s).|하나 이상의 칼럼 속성을 정의할 수 없습니다.|
|2339|The type of %s column (%s) is different from that of VALUE column (%s).|칼럼타입이 VALUE 칼럼타입과 다름입니다.|
|2340|SUMMARIZED column does not exist for %s.|summarized 칼럼이 없습니다.|
|2341|SUMMARIZED value is greater than UPPER LIMIT.|summarized 값이 UPPER LIMIT 보다 큼입니다.|
|2342|SUMMARIZED value is less than LOWER LIMIT.|summarized 값이 LOWER LIMIT 보다 작음입니다.|
|2343|LOWER LIMIT must not be greater than UPPER LIMIT.|LOWER LIMIT 은 UPPER LIMIT 보다 클 수 없습니다.|
|2344|Not numeric type. (%s)|숫자타입이 아님입니다.|
|2345|Column flag (%s) is only allowed for TAGMETA table.|칼럼 플래그는 TAGMETA table에서만 허용됩니다.|
|2346|Column type (%s) is not allowed for default value.|칼럼 타입은 기본값으로 허용되지 않습니다.|
|2347|SYSDATE is only allowed for default value.|SYSDATE은 기본값으로만 허용됩니다.|
|2348|Alter table set %s not support on cluster.|cluster에서는 alter table set이 지원되지 않습니다.|
|2349|Bind variable is not supported for new tag.|새 tag에 bind변수가 지원되지 않습니다.|
|2350|The function (%s) requires OVER clause.|OVER 절이 필요함 함수입니다.|
|2351|Window function is allowed only in SELECT list.|Window function은 SELECT list에서만 허용됩니다.|
|2352|OVER clause is not applicable on (%s).|OVER 절을 적용할 수 없습니다.|
|2353|Invalid data type (%s) in OVER clause.|OVER 절에서 잘못된 타입입니다.|
|2354|Constant is not allowed in OVER clause.|OVER 절에서는 상수가 허용되지 않습니다.|
|2355|Type (%s) is not supported.|지원되지 않는 타입입니다.|
|2356|Origin must be the first day of the month.|Origin은 해당 월의 첫 번째 날이어야 합니다.|
|2600|SEQUENCE property is not applicable in the table.|테이블에 SEQUENCE 속성이 적용되지 않습니다.|
|2601|Invalid function in a SEQUENCE column. NEXTVAL must be used.|SEQUENCE 칼럼에서 잘못된 함수. NEXTVAL이 사용됨야 합니다.|
|2602|NEXTVAL is applicable only in INSERT statement.|NEXTVAL은 INSERT statement에서만 적용 가능합니다.|
|2603|NEXTVAL is applicable only in SEQUENCE columns.|NEXTVAL은 SEQUENCE 칼럼에서만 적용 가능합니다.|
|2604|Sequence column must be LONG type.|Sequence 칼럼은 LONG 타입 이어야 합니다.|
|2651|Dependent ROLLUP table exists.|종속된 ROLLUP 테이블이 있습니다.|
|2652|Not a ROLLUP table. (%s)|ROLLUP 테이블이 아님입니다.|
|2653|Rollup interval must be greater than source rollup interval.|ROLLUP interval은 소스 ROLLUP interval보다 커야 합니다|
|2654|ROLLUP (%s) is not found.|ROLLUP을 찾을 수 없습니다|
|2655|Rollup interval source rollup interval Must Divide Zero.|ROLLUP interval은 소스 ROLLUP interval로 나누어 떨어져합니다.|
|2656|Rollup interval must positive integer.|ROLLUP interval은 양수이어야 합니다.|
|2657|Rollup interval must be smaller than year.|ROLLUP interval은 1년보다 작아야 합니다.|
|2658|ROLLUP is not enabled for %s.|ROLLUP이 활성화 되지 않습니다.|
|2659|Rollup maximum count is 100.|ROLLUP 최대 count는 100임입니다.|
|2670|Rollup user ID(%d) is not equal to Source user ID(%d)|ROLLUP의 사용자 ID와 Source 사용자 ID와 일치하지 않습니다.|
|2671|Invalid type for ROLLUP column (%s).|유효하지 않은 ROLLUP 칼럼 타입입니다.|
|2672|Json path is not specified on %s.|Json path가 지정되지 않습니다.|
|2673|Json path is not applicable on %s.|Json path를 적용할 수 없습니다.|
|2674|ROLLUP query must have a target column.|ROLLUP 쿼리는 반드시 target 칼럼이 있어야 합니다.|
|2675|Cannot use more than one ROLLUP column in a ROLLUP query.|ROLLUP 쿼리에서 1개를 초과하는 ROLLUP칼럼을 사용할 수 없습니다.|
|2676|Not a TAG table.|TAG 테이블이 아님입니다.|
|2677|Invalid rollup time unit (%s).|유효하지 않은 rollup 시간 단위입니다.|
|2678|WITH ROLLUP requires a SUMMARIZED column.|WITH ROLLUP은 summarized 칼럼이 필요합니다.|
|2679|Failed to create ROLLUP by WITH ROLLUP option.|WITH ROLLUP 옵션으로 ROLLUP생성에 실패했습니다.|
|2680|ROLLUP (%s) is already started.|ROLLUP이 이미 시작합니다.|
|2681|ROLLUP (%s) is already stopped.|ROLLUP이 이미 중단됩니다.|
|2682|ROLLUP extension type is different.|ROLLUP 표현식 타잎이 다름입니다.|
|2683|Cannot read a column (%s) in ROLLUP query because it is not a ROLLUP time column.|ROLLUP 쿼리에서 칼럼을 읽을 수 없습니다. ROLLUP 시간 칼럼이 아님입니다.|
|2684|Dependent ROLLUP table does not exist.|종속된 ROLLUP 테이블이 없습니다.|
|2685|There are no applicable ROLLUP tables.|적용가능한 ROLLUP 테이블이 없습니다.|
|2700|Policy (%s) already exists.|Policy가 이미 존재합니다.|
|2701|Policy (%s) does not exists.|Policy가 존재하지 않습니다.|
|2702|Policy (%s) is in use.|Policy가 사용중입니다입니다.|
|2703|Table (%s) has no retention policy.|테이블에 retention policy가 없습니다.|
|2704|Table (%s) already has a retention policy.|테이블에 이미 retention policy가 있습니다.|
|2705|Retention duration must be longer than 1 day.|Retention duration은 1일 이상이어야 합니다.|
|2706|Retention interval must be longer than 1 hour.|Retention interval은 1시간 이상이어야 합니다.|
|2707|Retention is not applicable on the table (%s).|Retention을 테이블에 적용할 수 없습니다.|
|2708|Only SYS user can create or drop RETENTION.|SYS 사용자만 RETENTION을 생성/삭제 할 수 있습니다.|
|2800|The stream query is too long. (max=2048)|너무 긴 스트림쿼리쿼리입니다.|
|2801|The stream query is not applicable.|스트림쿼리가 적용되지 않습니다.|
|2802|Cannot get table information.|테이블정보를 얻을 수 없습니다.|
|2803|Specified stream query statement has no LOG table.|지정된 스트림 쿼리에 LOG 테이블이 없습니다.|
|2804|Specified stream query statement has more than 1 LOG tables.|LOG테이블에 지정된 스트림쿼리 statement가 1개 이상임입니다.|
|2805|The stream query (%s) is not found.|스트림쿼리를 찾을 수 없습니다.|
|2806|The stream query (%s) already exists.|스트림쿼리가 이미 있습니다.|
|2807|The stream query (%s) is already started.|스트림쿼리 시작입니다.|
|2808|The stream query (%s) is already stopped.|스트림쿼리 멈춤입니다.|
|2809|The stream query (%s) is still running.|스트림쿼리 실행 중입니다.|
|2810|Cannot execute the stream query (%s).|스트림쿼리를 실행할 수 없습니다.|
|2811|The stream query (%s) is executed automatically by the system.|시스템에의한 스트림쿼리 자동 실행입니다.|
|2812|The Frequency clause is not allowed here.|Frequency 절을 사용할 수 없습니다.|
|2813|Invalid ROLLUP expression. (Token = %s, Unit = %ld)|유효하지 않은 ROLLUP 표현식입니다.|
|2814|Invalid ROLLUP target. BASETIME column of TAGDATA table is the only target.|유효하지 않은 ROLLUP target. Tag테이블 BASETIME칼럼만 target이 될 수 있습니다.|
|2815|Different ROLLUP expressions are used in a single SELECT query.|다른 ROLLUP 표현식이 단일 select 쿼리에서 사용됩니다.|
|2816|Only rollup column with aggregate function can be referenced in ROLLUP SELECT query.|ROLLUP SELECT 쿼리에서는 집계 함수가 있는 롤업 칼럼만 참조할 수 있습니다.|
|2817|ROLLUP expression must be used in SELECT query.|ROLLUP 표현식은 select 쿼리에서만 사용할 수 있습니다.|
|2818|Invalid ROLLUP target (%s).|유효하지 않은 ROLLUP target입니다.|
|2819|ROLLUP thread is running.|ROLLUP thread가 동작중입니다입니다.|
|2820|ROLLUP thread is not running.|ROLLUP thread가 동작하지 않습니다.|
|2821|Another DDL/DELETE/SNAPSHOT is in progress.|수행중인 DDL/DELETE/SNAPSHOT이 있습니다.|
|2822|Invalid expression in ROLLUP query : %.*s|ROLLUP 쿼리에 유효하지 않은 표현입니다.|
|2823|Invalid table in ROLLUP query: %s|RULLUP 쿼리에 유효하지 않은 테이블입니다.|
|2825|Extended column(%s) cannot be used in ROLLUP query.|확장된 칼럼은 ROLLUP 쿼리에서 사용할 수 없습니다.|
|2826|User (%s) can't revoke from table (%s.%s).|사용자가 테이블에 대한 권한을 취소를 할 수 없습니다.|
|2827|User does not have grant privileges.|사용자에게 grant 권한이 없습니다.|
|2828|User does not have revoke privileges.|사용자에게 취소권한이 없습니다.|
|2829|Only SYS user can create or drop user.|SYS사용자만 사용자를 생성/삭제 할 수 있습니다.|
|2830|The user does not have (%s) privilege on table(%s.%s).|사용자가 테이블에 대한 권한이 없습니다.|
|2831|You can't grant UPDATE privilege on Log Table.|Log 테이블에는 UPDATE 권한을 줄 수 없습니다.|
|2832|You can't revoke UPDATE privilege on Log Table.|Log 테이블에는 UPDATE 권한을 취소할 수 없습니다.|
|2833|You can only grant SELECT privileges on Mounted database.|마운트된 database 에는 SELECT권한만 줄 수 있습니다.|
|3000|Statement ID overflow (Limit = %u, Curr = %u).|Statement ID 초과입니다.|
|3001|Statement query length is zero.|Statement 쿼리 길이 0입니다.|
|3002|Task pool initialization error.|Task pool 초기화 에러가 발생했습니다.|
|3003|Statement pool initialization error.|Statement pool 초기화 에러가 발생했습니다.|
|3004|Queue creation error.|큐생성 에러가 발생했습니다.|
|3005|Statement allocation error.|Statement 할당 에러가 발생했습니다.|
|3006|Unknown meta type error (typecode is %u). Internal error.|알 수 없는 meta타입 오류.(Internal error)입니다.|
|3007|Insufficient protocol buffer size. Increase it.|충분하지 않은 프로토콜 버퍼 크기. 증가 필요합니다.|
|3008|Invalid protocol state. Check your application again. (Protocol = %s, State = %s)|유효하지 않은 프로토콜 상태. 애플리케이션 확인가 필요합니다.|
|3009|Invalid execute protocol data (%s).|유효하지 않은 실행프로토콜 데이터입니다.|
|3010|Error in fetch protocol: not enough buffer size to execute it. Increase the size.|버퍼 크기 부족으로 인한 fetch프로토콜 에러. 버퍼 크기 증가 필요합니다.|
|3011|Send error.|전송 에러가 발생했습니다.|
|3012|Memory allocation error.|메모리할당 에러가 발생했습니다.|
|3013|Invalid table name for append table. Table name is omitted.|입력에 유효하지 않은 테이블 이름입니다.|
|3014|Invalid append protocol data (%s).|유효하지 않은 입력 프로토콜 데이터입니다.|
|3015|Endian is not specified for append. Check endian information.|입력을 위한 엔디안 미지정. 엔디안 정보 확인입니다.|
|3016|Too many columns are specified for append. Cannot append more than %d columns|입력시 너무 많은 칼럼이 지정됩니다.|
|3017|Too large record size for append. Cannot append more than %d bytes per record.|입력하기에 너무큰 record size입니다.|
|3018|It exceeds the specified max. block size (%d). Check append data structure of your applcation.|지정된 최대 블록 크기 초과. 애플리케이션의 추가 데이터 구조 확인입니다.|
|3019|Explain plan error. Use it for SELECT statement only.|Explain plan에러. Explain plan은 select statement에서만 사용 가능합니다.|
|3020|Explain plan is not allowed in prepared mode.|Prepared모드에서는 explain plan을 사용할 수 없습니다|
|3021|Protocol versions are not matched: Server (%d.%d.%d) Client (%d.%d.%d)|서버와 클라이언트가 프로토콜버전 불일치입니다.|
|3022|Failed to get handle limit from the system.|시스템 핸들한도를 얻는데에 실패했습니다.|
|3023|Handle limit(%d) from the system is less than that of property(%d). Tune system handle limit or decrease the property 'HANDLE_LIMIT'|시스템의 핸들 한도가 속성값보다 작음. 시스템 핸들 한도를 조정하거나 'HANDLE_LIMIT' 속성을 낮출 필요가 있습니다|
|3024|Invalid session ID (%llu).|유효하지 않은 세션ID입니다.|
|3025|Not enough privileges to manipulate the session. (%llu)|세션조작을 위한 권한이 부족합니다.|
|3026|You should log in with the same user name in the target session. Now (%d) Target(%d)|로그인시 target세션과 같은 사용자 이름이 필요합니다.|
|3027|This statement has been canceled.|Statement가 취소됩니다.|
|3028|Invalid session property name. Name (%s) does not exist.|유효하지않은 세션 프로퍼티 name. Name이 존재하지 않습니다.|
|3029|Error in converting session property (%s). Cannot convert string (%s) to integer.|세션프로세스 변환 과정에서 에러 발생. 문자를 숫자료 변환할 수 없습니다.|
|3030|Invalid session property value. Check the session value (%s)|유효하지 않은 세션 프로퍼티값. 세션값 확인가 필요합니다.|
|3031|Protocol error.|프로토콜 에러가 발생했습니다.|
|3032|Error in getting license meta. Check DB image and binary.|라이선스 meta를 얻는도중 에러 발생. DB image와 binary파일 확인가 필요합니다.|
|3033|Error in opening meta.|Meta open도중에서 에러가 발생했습니다.|
|3034|Error in executing meta.|Meta 처리도중에서 에러가 발생했습니다.|
|3035|Error in closing meta.|Meta close도중에서 에러가 발생했습니다.|
|3036|The license is expired(%s).|라이선스가 만료됩니다.|
|3037|The license is invalid or the license file does not exist(%s).|라이선스파일이 없거나 유효하지 않습니다.|
|3038|License violation detected. You have exceeded your license limit(%u) or expiry date(%s). For more information, contact sales@machbase.com.|라이선스 위반. 라이선스가 한도를 초과했거나 만료됩니다. 자세한 정보 문의는 sales@machbase.com으로 연락입니다.|
|3039|Session count exceed: (maxcount =%llu).|세션수 허용치 초과입니다.|
|3040|Unable to shutdown since the server is busy.|종료되지 않은 작업으로 인해 서버를 종료할 수 없습니다.|
|3041|AppendBatch error: %s.|AppendBatch에 실패했습니다.|
|3042|Recovery in progress.|Recovery 수행 중입니다.|
|3043|Array Execute is not applicable for SELECT query.|Array execute는 select쿼리에서 사용할 수 없습니다.|
|3044|Wrong TIMEZONE string error: %s.|잘못된 타임존입니다.|
|3045|Invalid context at %s.|유효하지 않은 context입니다.|
|3046|Communication module error (rc=%d): [%s].|통신모율에 실패했습니다.|
|3047|Failed to call function %s (rc=%d)|함수호출에 실패했습니다.|
|3100|Append Operation is not supported in Cluster Edition|cluster 에디션에서는 입력이 지원되지 않습니다.|
|3101|Can't convert (%s) to number|숫자로 변환할 수 없습니다.|
|3102|Can't decode in base64|base64를 디코드 할 수 없습니다.|
|3103|not supported JSON type (%d)|지원되지 않는 JSON타입입니다.|
|3104|Column count for append is not matched with Meta|입력을 위한 칼럼의 수가 Meta와 불일치합니다.|
|3105|The table type for append is not valid|입력을 위한 테이블타입이 유효하지 않습니다.|
|3106|the JSON format is not valid|JSON포멧이 유효하지 않습니다.|
|3107|Can't get the meta info for append table|입력테이블을 위한 메타정보를 얻을 수 없습니다.|
|3108|Can't read data from or write data into network buffer|네트워크 buffer에서 데이터를 읽거나 쓸 수 없습니다.|
|3109|The URL (%s) is not valid format|URL이 유효한 포멧이 아님입니다.|
|3110|Timeout in waiting for response|response 타임아웃 발생입니다.|
|3111|Can't connect to proxy server (%s:%d)|poxsy server에 연결할 수 없습니다.|
|3112|Tag name in JSON must be string type|Tag name은 string타입 이어야 합니다.|
|3113|Tag name (%s) does not exist in meta list|Tag name이 메타 목록에 없습니다.|
|3114|The HTTP memory request exceeded the limit of (%lld). Change the property (HTTP_MAX_MEM) and restart server|HTTP 메모리 요청이 제한을 초과. 속성 (HTTP_MAX_MEM)을 변경후 서버 재시작입니다.|
|3115|Table name is omitted from the JSON format|테이블 이름이 JSON 형식에서 생략됩니다.|
|3116|Wrong Base64 Format Received|잘못된 base64 포멧입니다.|
|3117|Only Basic Authorization Accept To Login.|로그인시 basic authoriztion만 가능합니다.|
|3118|There is No Authorization Header.|인증 header가 없습니다.|
|3119|The value of tag default column<%d> must not be NULL|TAG의 기본칼럼 값은 NULL이 될 수 없습니다.|
|3120|The timezone (%s) is invalid.|유효하지 않은 타임존입니다.|
|3121|Fail to get json object|json객체를 얻는데 실패했습니다.|
|3122|There is no argument for Rest API|REST API 인수가 없습니다.|
|3123|Count value is not valid for Rest API|REST API Count값이 유효하지 않습니다.|
|3124|Interval value is not valid for Rest API|REST API Interval 값이 유효하지 않습니다.|
|3125|Interval type is not valid for Rest API|REST API Interval타입이 유효하지 않습니다.|
|3126|The requested URL for the REST API is not valid|요청된 REST API URL이 유효하지 않습니다.|
|3127|The requested URL for the REST API is not supported|요청된 REST API URL이 지원되지 않습니다.|
|3128|TAG_STAT is not available for table %s.|본 테이블에서는 TAG_STAT을 사용할 수 없습니다.|
|3200|Server is not running.|서버가 동작중이지 않은입니다.|
|3201|Invalid statement state: (%d)|유효하지 않은 statement 상태입니다.|
|3202|Column index is out of range.|칼럼 인덱스가 범위 밖임입니다.|
|3203|The length of data exceeded the size of buffer.|data의 길이가 buffer size를 초과합니다.|
|3204|Append data ip string is null.|입력 데이터 IP부분이 비어있습니다.|
|3205|Append data datetime string(%s) is null.|입력 데이터 시간부분이 비어있습니다.|
|3206|Invalid column type (%d).|유효하지 않은 칼럼 타입입니다.|
|3207|Invalid statement type (%d).|유효하지 않은 statement type입니다.|
|3208|Server thread error: %d - %s|서버 thread 문제 발생입니다.|
|3209|statement is busy. (%d)|statement자원이 부족합니다.|
|3210|This connection has been already disconnected|connection이 끊긴 상태입니다.|
|3211|Database already exists.|Database가 이미 생성된 상태입니다.|
|3212|Database does not exist.|Database가 존재하지 않습니다.|
|3213|Server is running.|서버가 동작중입니다입니다.|
|3214|Failed to open dbs(%s) directory.|dbs 디렉토리 open에 실패했습니다.|
|3215|ALTER SESSION statement is not supported.|ALTER SESSION이 지원되지 않습니다.|
