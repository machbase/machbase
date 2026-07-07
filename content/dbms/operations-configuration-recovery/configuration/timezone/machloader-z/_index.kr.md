---
type: docs
title: 'machloader -z'
weight: 30
---

`machloader`는 CSV 등 텍스트 파일의 데이터를 Machbase에 대량으로 로드하거나 내보내는 도구입니다. `-z` 옵션으로 DATETIME 값의 해석 기준 타임존을 지정할 수 있습니다.

## 사용법

```bash
machloader -z +-HHMM [기타 옵션]
```

## 데이터 로드 시 타임존 지정

CSV 파일에 포함된 DATETIME 값을 지정한 타임존으로 해석하여 UTC로 변환한 뒤 저장합니다.

```bash
# KST(UTC+9) 기준 DATETIME이 담긴 CSV 파일을 로드
machloader -i -t sensor_data -d data.csv -z +0900
```

위 명령어는 `data.csv`의 DATETIME 컬럼 값을 KST 시각으로 간주하고, UTC로 변환하여 `sensor_data` 테이블에 저장합니다.

예를 들어 CSV 파일에 `2026-07-07 10:00:00`이 있으면, 이를 KST(+09:00)로 해석하여 UTC 기준 `2026-07-07 01:00:00`으로 변환해 저장합니다.

## 데이터 추출 시 타임존 지정

데이터를 파일로 내보낼 때도 `-z` 옵션으로 출력 타임존을 지정합니다.

```bash
# 테이블 데이터를 KST 기준으로 CSV 파일에 내보내기
machloader -o -t sensor_data -d output.csv -z +0900
```

내보낸 CSV 파일의 DATETIME 값이 지정된 타임존 기준으로 변환되어 출력됩니다.

## 주의 사항

- `-z` 옵션을 지정하지 않으면 서버의 기본 타임존이 적용됩니다.
- 로드와 추출 방향 모두 동일한 타임존 옵션(`-z`)을 사용합니다.
- 원본 데이터의 실제 타임존과 `-z` 옵션에 지정한 값이 일치하지 않으면 시각이 잘못 저장됩니다. CSV 파일이 어떤 타임존 기준으로 생성되었는지 먼저 확인합니다.
- 대용량 데이터를 로드할 때 타임존 변환은 성능에 거의 영향을 주지 않습니다.
