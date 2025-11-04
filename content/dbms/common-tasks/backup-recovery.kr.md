---
type: docs
title: '백업 및 복구'
weight: 50
---

적절한 백업 전략과 복구 절차로 Machbase 데이터를 보호하는 방법을 학습합니다.

## 백업 개요

### 백업 유형

| 유형 | 방법 | 다운타임 | 복구 지점 |
|------|--------|----------|----------------|
| **전체 백업** | machadmin -b | 오프라인 | 완전 |
| **온라인 백업** | Database mount | 없음 | 특정 시점 |
| **내보내기 백업** | CSV export | 없음 | 테이블 수준 |

## 전체 데이터베이스 백업

### 오프라인 백업 (권장)

```bash
# 1. 서버 중지
machadmin -s

# 2. 데이터베이스 백업
machadmin -b /backup/machbase_backup_20251010

# 3. 서버 시작
machadmin -u
```

**장점**:
- 완전한 일관성
- 가장 빠른 백업
- 가장 작은 백업 크기

**단점**:
- 다운타임 필요
- 전체 서버 종료

### 백업 스크립트

```bash
#!/bin/bash
# daily_backup.sh

BACKUP_DIR="/backup/machbase"
DATE=$(date +%Y%m%d)
BACKUP_PATH="$BACKUP_DIR/backup_$DATE"

# 백업 디렉토리 생성
mkdir -p $BACKUP_DIR

# 서버 중지
machadmin -s

# 백업
machadmin -b $BACKUP_PATH

# 서버 시작
machadmin -u

# 백업 확인
if [ -d "$BACKUP_PATH" ]; then
    echo "Backup successful: $BACKUP_PATH"
    # 백업 압축
    tar -czf ${BACKUP_PATH}.tar.gz -C $BACKUP_DIR backup_$DATE
    rm -rf $BACKUP_PATH
else
    echo "Backup failed!" | mail -s "Backup Error" admin@company.com
fi

# 오래된 백업 제거 (최근 7일 유지)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

### 자동화된 백업 (cron)

```bash
# crontab 편집
crontab -e

# 매일 오전 2시에 백업 추가
0 2 * * * /opt/scripts/daily_backup.sh >> /var/log/machbase_backup.log 2>&1
```

## 데이터베이스 복구

### 전체 복구

```bash
# 1. 서버 중지 (실행 중인 경우)
machadmin -s

# 2. 기존 데이터베이스 제거
rm -rf $MACHBASE_HOME/dbs/*

# 3. 백업에서 복구
machadmin -r /backup/machbase_backup_20251010

# 4. 서버 시작
machadmin -u

# 5. 확인
machsql -f - <<EOF
SHOW TABLES;
SELECT COUNT(*) FROM sensors;
EOF
```

### 압축된 백업에서 복구

```bash
# 백업 압축 해제
tar -xzf /backup/backup_20251010.tar.gz -C /tmp

# 복구
machadmin -s
rm -rf $MACHBASE_HOME/dbs/*
machadmin -r /tmp/backup_20251010
machadmin -u

# 정리
rm -rf /tmp/backup_20251010
```

## 온라인 백업 (데이터베이스 마운트)

### 온라인 백업 생성

```bash
# 1. 데이터베이스 마운트 (일관된 스냅샷 생성)
machadmin -mount /backup/mount_point

# 2. 데이터베이스 파일 복사
cp -r $MACHBASE_HOME/dbs /backup/online_backup_20251010

# 3. 마운트 해제
machadmin -unmount /backup/mount_point
```

**장점**:
- 다운타임 없음
- 서버 계속 실행

**단점**:
- 디스크 공간 필요
- 더 복잡함

## 테이블 수준 백업 (CSV 내보내기)

### CSV로 테이블 내보내기

```bash
# 단일 테이블 내보내기
machsql -s localhost -u SYS -p MANAGER -f - -o sensors_backup.csv -r csv <<EOF
SELECT * FROM sensors;
EOF

# 시간 범위 지정 내보내기
machsql -s localhost -u SYS -p MANAGER -f - -o sensors_recent.csv -r csv <<EOF
SELECT * FROM sensors DURATION 7 DAY;
EOF
```

### 내보내기 스크립트

```bash
#!/bin/bash
# export_tables.sh

BACKUP_DIR="/backup/csv"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR

# 테이블 내보내기
for table in sensors logs devices; do
    echo "Exporting $table..."
    machsql -i -f - -o "$BACKUP_DIR/${table}_${DATE}.csv" -r csv <<EOF
SELECT * FROM $table;
EOF
done

# 내보내기 압축
tar -czf $BACKUP_DIR/csv_backup_${DATE}.tar.gz -C $BACKUP_DIR *_${DATE}.csv
rm $BACKUP_DIR/*_${DATE}.csv

echo "CSV backup complete: $BACKUP_DIR/csv_backup_${DATE}.tar.gz"
```

### CSV에서 복구

```bash
# CSV 데이터 가져오기
machloader -t sensors -d csv -i sensors_backup.csv
```

## 증분 백업 전략

### 일일 증분 + 주간 전체

```bash
#!/bin/bash
# incremental_backup.sh

BACKUP_DIR="/backup/machbase"
DAY_OF_WEEK=$(date +%u)  # 1=월요일, 7=일요일

if [ $DAY_OF_WEEK -eq 7 ]; then
    # 일요일: 전체 백업
    echo "Performing full backup..."
    machadmin -s
    machadmin -b $BACKUP_DIR/full_$(date +%Y%m%d)
    machadmin -u
else
    # 평일: CSV 내보내기
    echo "Performing incremental backup..."
    machsql -i -f - -o $BACKUP_DIR/incremental_$(date +%Y%m%d).csv -r csv <<EOF
    SELECT * FROM sensors WHERE _arrival_time >= SYSDATE - 1;
    EOF
fi
```

## 백업 검증

### 백업 무결성 확인

```bash
# 백업 디렉토리 존재 확인
ls -lh /backup/machbase_backup_20251010

# 백업 크기 확인 (너무 작으면 안 됨)
du -sh /backup/machbase_backup_20251010

# 임시 위치로 복구 테스트
TEST_DIR="/tmp/test_restore"
mkdir -p $TEST_DIR
machadmin -r /backup/machbase_backup_20251010 -d $TEST_DIR
ls -lh $TEST_DIR
rm -rf $TEST_DIR
```

### CSV 내보내기 확인

```bash
# CSV 파일 확인
head -10 sensors_backup.csv
wc -l sensors_backup.csv

# 컬럼 수 확인
awk -F',' '{print NF}' sensors_backup.csv | sort -u
```

## 재해 복구

### 복구 계획

**시나리오**: 완전한 서버 장애

1. **새 서버 준비**
2. **Machbase 설치**
3. **백업에서 복구**
4. **데이터 무결성 확인**
5. **운영 재개**

### 단계별 복구

```bash
# 1. Machbase 설치
wget http://machbase.com/dist/machbase-xxx.tgz
tar xzf machbase-xxx.tgz
export MACHBASE_HOME=$(pwd)/machbase_home
export PATH=$MACHBASE_HOME/bin:$PATH

# 2. 백업에서 복구
machadmin -r /backup/machbase_backup_20251010

# 3. 서버 시작
machadmin -u

# 4. 데이터 확인
machsql -f - <<EOF
SHOW TABLES;
SELECT COUNT(*) FROM sensors;
SELECT MAX(_arrival_time) FROM sensors;
EOF

# 5. 애플리케이션 연결 테스트
```

## 백업 모범 사례

### 1. 3-2-1 규칙

- **3**개의 데이터 복사본 (운영 + 백업 2개)
- **2**가지 다른 미디어 유형 (디스크 + 테이프/클라우드)
- **1**개의 오프사이트 복사본 (원격 위치/클라우드)

### 2. 정기적인 테스트

```bash
# 월별 복구 테스트
# 테스트 환경으로 복구 및 확인
```

### 3. 자동화된 백업

```bash
# Cron 일정
0 2 * * * /opt/scripts/daily_backup.sh  # 매일 오전 2시
0 3 * * 0 /opt/scripts/weekly_backup.sh  # 매주 일요일
```

### 4. 백업 성공 모니터링

```bash
# 백업 로그 확인
tail -50 /var/log/machbase_backup.log

# 실패 시 알림
if ! grep -q "Backup successful" /var/log/machbase_backup.log; then
    echo "Backup failed!" | mail -s "Alert" admin@company.com
fi
```

### 5. 절차 문서화

다음 내용을 포함하는 런북 작성:
- 백업 일정
- 복구 절차
- 연락처 정보
- 복구 시간 목표 (RTO)
- 복구 시점 목표 (RPO)

## 백업 저장소

### 로컬 저장소

```bash
# 전용 백업 디스크
/dev/sdb1 → /backup

# /etc/fstab에 마운트
/dev/sdb1  /backup  ext4  defaults  0  2
```

### 원격 저장소 (rsync)

```bash
# 원격 서버로 동기화
rsync -avz /backup/machbase/ backup-server:/backups/machbase/

# 백업 스크립트에서
tar -czf backup_${DATE}.tar.gz backup_${DATE}
rsync -avz backup_${DATE}.tar.gz backup-server:/backups/
```

### 클라우드 저장소 (AWS S3)

```bash
# S3로 업로드
aws s3 cp backup_${DATE}.tar.gz s3://my-backup-bucket/machbase/

# 백업 스크립트에서
tar -czf /tmp/backup_${DATE}.tar.gz -C /backup backup_${DATE}
aws s3 cp /tmp/backup_${DATE}.tar.gz s3://my-backup-bucket/machbase/
rm /tmp/backup_${DATE}.tar.gz
```

## 성능 영향

### 백업 성능

| 방법 | 소요 시간 (1TB) | CPU 영향 | I/O 영향 |
|--------|----------------|------------|------------|
| 전체 오프라인 | 30-60분 | 없음 (오프라인) | 높음 |
| 온라인 마운트 | 60-90분 | 낮음 | 중간 |
| CSV 내보내기 | 120분 이상 | 중간 | 높음 |

### 영향 최소화

```bash
# ionice를 사용하여 I/O 우선순위 감소
ionice -c3 machadmin -b /backup/machbase

# nice를 사용하여 CPU 우선순위 감소
nice -n 19 machadmin -b /backup/machbase
```

## 복구 시간 목표

### 일반적인 RTO

| 시나리오 | RTO 목표 | 방법 |
|----------|------------|--------|
| 단일 테이블 | < 1시간 | CSV 복구 |
| 전체 데이터베이스 | < 4시간 | 전체 복구 |
| 재해 복구 | < 24시간 | 전체 복구 + 검증 |

## 문제 해결

**"database in use" 오류로 백업 실패**:
```bash
# 서버가 중지되었는지 확인
machadmin -s
sleep 5
machadmin -e  # "not running" 표시되어야 합니다
machadmin -b /backup/path
```

**복구 실패**:
```bash
# 백업 무결성 확인
ls -lh /backup/machbase_backup

# 백업 디렉토리 구조 확인
tree /backup/machbase_backup

# 디스크 공간 확인
df -h $MACHBASE_HOME
```

**백업 중 디스크 공간 부족**:
```bash
# 백업 전 공간 확인
df -h /backup

# 오래된 백업 정리
find /backup -name "backup_*" -mtime +7 -delete
```

## 다음 단계

- **사용자 관리**: [사용자 관리](../user-management/) - 백업 사용자 권한
- **모니터링**: [문제 해결](../../troubleshooting/) - 백업 상태 모니터링
- **튜토리얼**: [시작하기](../../getting-started/) - 설정 절차

---

견고한 백업 전략을 구현하고 Machbase 데이터를 손실로부터 보호하세요!
