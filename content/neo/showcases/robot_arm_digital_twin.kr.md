---
title: 로봇 팔 디지털 트윈
type: docs
weight: 1000
---

로봇 팔의 움직임과 센서 데이터를 시계열로 저장하고 대시보드에서 분석하는 Machbase Neo Physical AI 데모입니다.

{{< icon "github" >}} https://github.com/machbase/neo-pkg-robot-demo
<p/>

{{< youtube JeABxt2JYFI >}}

DROID 로봇 데이터셋을 활용한 Physical AI 데모입니다.


**핵심 포인트**

- 32,212개의 로봇 프레임 저장
- 원본 로봇 궤적을 시간축 그대로 저장
- JSON 구조에 원시 상태와 파생 지표를 함께 보존
- 단일 TAG 테이블로 스키마 단순화
- JSON 경로 롤업으로 구간을 빠르게 분석
- 특정 시점의 프레임과 주변 윈도우 조회를 실시간 UI에 연결
- Physical AI 데이터의 재생, 이벤트 감지, 이상 시각화 가능성 확인