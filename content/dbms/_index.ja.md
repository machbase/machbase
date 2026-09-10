---
type: docs
title: 'Machbase DBMS マニュアル'
weight: 30
toc: true
---

Machbase DBMS マニュアルへようこそ。本書は Machbase 8.7.0 を対象に、インストール、
テーブルタイプ別の利用方法、アプリケーション開発、運用、セキュリティ、リファレンスを説明します。

初めて利用する場合は、1章の SQL 演習を実行し、2章でデータモデルとストレージ・運用の原理を学びます。
システムを設計する場合は、4章のテーブル選択基準を確認してから、必要なテーブルの章に進んでください。
利用中の機能の正確な構文やサポート範囲は16章で確認できます。

## マニュアルの構成

| 章 | タイトル | 内容 |
|----|------|------|
| 1 | [はじめに](./getting-started/) | 概要、接続確認、クイックスタート、基本コマンド |
| 2 | [基本概念](./core-concepts/) | テーブルタイプ、時間モデル、ROLLUP、Retention Policy |
| 3 | [インストール・デプロイ・アップグレード](./installation-deployment-upgrade/) | 事前準備、Standard Edition、Cluster Edition、アップグレード |
| 4 | [テーブルタイプの選択とスキーマ設計](./data-modeling-table-design/) | タイプの選択、スキーマ、変更ポリシー、モデリングパターン |
| 5 | [TAG テーブルの利用](./tag-table-usage/) | TAG 構造、メタデータ、入力、クエリ、補正、運用 |
| 6 | [TAG テーブルの ROLLUP](./tag-rollup-usage/) | ROLLUP の設計、作成、クエリ、再構築、運用、性能チューニング |
| 7 | [LOG テーブルの利用](./log-table-usage/) | LOG 構造、入力、テキスト検索 |
| 8 | [TRANSACTION テーブルの利用](./rdb-table-usage/) | TRANSACTION スキーマ、DML、トランザクション、JOIN、バックアップ・リストア |
| 9 | [LOOKUP テーブルの利用](./lookup-table-usage/) | 参照データ、PRIMARY KEY、JSON、一般的な述語を使う DML、JOIN |
| 10 | [VOLATILE テーブルの利用](./volatile-table-usage/) | インメモリテーブル、UPSERT、状態キャッシュ、再起動とデータ消失 |
| 11 | [開発とアプリケーション連携](./development-tools-integration/) | 連携方式、共通概念、言語別 SDK/API |
| 12 | [性能チューニング](./performance-tuning/) | クエリ性能、取り込み性能、キャッシュ調整 |
| 13 | [運用・設定・復旧](./operations-configuration-recovery/) | サーバー管理、バックアップ、Cluster 運用 |
| 14 | [アカウント・権限・アクセス制御](./security-access-control/) | アカウント、権限、AUTH KEY、アクセス制御 |
| 15 | [トラブルシューティング](./troubleshooting/) | エラーの診断と解決 |
| 16 | [リファレンス](./reference/) | SQL 構文、関数、設定、システムカタログ |
