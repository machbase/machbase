---
title: 철도 압축 공기 장치 상태 진단
type: docs
weight: 975
---

철도 차량 APU 센서 데이터를 적재하고 시각화해 상태 진단까지 이어지는 Machbase Neo의 시계열 데이터 처리 흐름을 소개합니다.

{{< icon "github" >}} https://github.com/machbase/neo-train-apu-demo
<p/>

{{< youtube UmttgrKJWwM >}}

이 데모에서는 UCI Machine Learning Repository의 MetroPT-3 데이터셋을 Machbase Neo에 저장하고, 철도 차량의 압축 공기 공급 장치(APU) 상태를 대화형 대시보드에서 살펴볼 수 있도록 구성했습니다.


데이터셋에 기록된 공기 누출(Failure) 구간과 센서 변화, 설명 가능한 건전성 점수(Health Score)를 함께 확인하며 시간에 따른 데이터를 분석할 수 있습니다.


**주요 기능**

- MetroPT-3 전체 데이터셋(약 151만 시점) 탐색
- 철도 APU의 공기 흐름과 장비 상태 시각화
- 압력, 온도, 전류, 밸브, 스위치 등 15종 센서 데이터 분석
- 데이터셋에 기록된 공기 누출(Failure) 구간 표시
- 설명 가능한 규칙 기반 Health Score와 이벤트 표시
- 시간축에서 센서 데이터 재생 및 탐색
- 영어·한국어 UI 지원
- Machbase Neo JSON Rollup을 이용한 고속 시계열 조회
- Live Query 기반 Frame / Window / Signal API 제공
- SQL, 실행 시간, Rollup 정보를 확인할 수 있는 Evidence API


이 데모의 Health Score와 이벤트는 머신러닝 모델이 아니라 프로젝트에서 정의한 규칙 기반 지표이며, 각 결과의 근거를 확인할 수 있습니다.

데이터셋에 포함된 고장(Failure) 구간과 프로젝트에서 계산한 이벤트를 구분해 표시하므로, 실제 센서 데이터에 기반한 분석 과정을 투명하게 확인할 수 있습니다.

Industrial AI와 Predictive Maintenance에서는 이상 여부를 예측하는 데 그치지 않고, 센서 데이터와 시간축을 함께 분석해 결과를 설명하는 것이 중요합니다.

Machbase Neo는 대용량 시계열 데이터를 저장하고 JSON Rollup으로 필요한 구간을 빠르게 조회합니다. 이 데이터를 웹 기반 모니터링 및 분석 화면과 연계할 수 있습니다.

이 데모는 철도 차량 APU의 시계열 데이터가 실시간 분석과 설명 가능한 상태 진단 화면으로 이어지는 과정을 보여줍니다.