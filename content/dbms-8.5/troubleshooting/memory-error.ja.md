---
title : 'メモリ不足'
type: docs
weight: 100
toc: true
---

クエリーの実行時にメモリ不足エラーが発生した場合の、プロパティの変更方法を説明します。

## クエリー実行時のメモリ不足エラー {#an-error-occurred-due-to-insufficient-memory-when-executing-the-query}

クエリーの実行に使用できるメモリには、次の理由から上限があります。

1 つのクエリーが大量のメモリを使用すると、同時に実行する他のクエリーがメモリ不足で実行できなくなる可能性があります。

メモリ不足エラーは、1 クエリーが使用できるメモリの上限値を増やすことで解消できます。

MAX_QPX_MEM プロパティで、1 つの SQL が使用できる最大メモリ量を管理します。

実行中の設定方法と、メモリ不足時のエラーメッセージや TRC メッセージは、[SET MAX_QPX_MEM](../../sql-reference/sys-session-manage/#set-max_qpx_mem) を参照してください。

SET コマンドによる設定は、Machbase の再起動後には引き継がれません。machbase.conf も次のように変更してください。

**Standard Edition**

machbase.conf の MAX_QPX_MEM を、より大きな値に変更します。

**Cluster Edition**

Standard Edition と同様です。ただし、すべてのクラスタノードの machbase.conf を変更する必要があります。



