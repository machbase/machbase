---
title : 'パッケージの概要'
type : docs
weight: 10
toc: true
---

## パッケージの種類 {#package-type}

MACHBASE は、手動インストール用ファイルとパッケージインストール用ファイルを提供します。

| インストール方法 | 説明 | 備考 |
|--|--|--|
| 手動インストール | Unix 用の tgz 圧縮ファイルです。<br>tar と GNU gzip で展開してインストールします。 | コンソール環境でのみインストール可能 |
| パッケージインストール | OS 別のパッケージを提供します。<br> - Windows：msi<br> - Linux：tgz | コンソール環境でのみインストール可能 |

## パッケージファイル名の構成 {#package-file-name-structure}

パッケージファイル名は、次の要素で構成されます。

```
machbase-EDITION-VERSION-OS-CPU-BIT-MODE[-OPTIONAL].EXT
```

| 項目 | 説明 |
|--|--|
| EDITION | エディション。<br> - standard：Standard Edition<br> - cluster：Cluster Edition |
| VERSION | パッケージのバージョン。数字と文字による _MajorVersion.MinorVersion.FixVersion.AUX_ 形式です。<br>- Major Version：製品のメジャーバージョン（数値）<br>- Minor Version：同じメジャーバージョン内で比較的大きな機能を追加した版。DB ファイルとプロトコルの互換性は保証されません（数値）。<br>- Fix Version：同じメジャーバージョン内での不具合修正や小規模な機能追加。DB ファイルとプロトコルの互換性は保証されます（数値）。<br>- AUX：パッケージの区分。<br> -- official：一般パッケージ<br> -- community：Community Edition パッケージ |
| OS | OS 名。例：LINUX、WINDOWS |
| CPU | CPU の種類。例：X86、IA64 |
| BIT | バイナリーが 32 ビットか 64 ビットかを示します。例：32、64 |
| MODE | バイナリーのリリースモード。例：release、debug、prerelease |
| OPTIONAL | 追加のパッケージ修飾子がある場合に表示されます。<br>lightweight：Coordinator に追加する軽量パッケージ |
| EXT | 拡張子。パッケージに応じて tgz、rpm、deb、msi があります。 |
