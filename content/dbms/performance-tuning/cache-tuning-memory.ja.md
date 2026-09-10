---
type: docs
title: '12.6 PVO Cache とメモリのチューニング'
weight: 60
toc: true
aliases:
  - /dbms/tag-table-usage/tag-cache-operations/
---

<a id="pvo-cache"></a>

## PVO Cache の運用

PVO Cache は SQL 実行計画を再利用します。クエリ結果の行を保存するキャッシュではありません。

<a id="tuning-memory-configuration"></a>

## メモリ設定のチューニング

PVO Cache、Min-Max Cache、プロセス上限、クエリの一時メモリを、利用可能な物理メモリの
予算内でまとめて計画します。
