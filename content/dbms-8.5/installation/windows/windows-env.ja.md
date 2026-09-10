---
title : 'Windows 環境の準備'
type : docs
weight: 10
toc: true
---

## ファイアウォールのポート開放 {#open-firewall-port}

Windows に Machbase をインストールする場合は、使用するポートを Windows ファイアウォールで開放する必要があります。

通常、ネイティブリスナーには **5656**、HTTP REST には
**5657** を使用します。

1. コントロールパネルから Windows ファイアウォールまたは Windows Defender ファイアウォールを開きます。
    表示された画面で「詳細設定」をクリックします。

![winenv1](/dbms-8.5/installation/windows/winenv1.png)

2. 「詳細設定」で **「受信の規則」→「新しい規則」**を選択します。

![winenv2](/dbms-8.5/installation/windows/winenv2.png)

![winenv3](/dbms-8.5/installation/windows/winenv3.png)

3. 規則の作成ウィザードで「ポート」を選択し、「次へ」をクリックします。

![winenv4](/dbms-8.5/installation/windows/winenv4.png)

4. **TCP(T)** を選択し、**「特定のローカル ポート」**に **5656,5657** を入力して「次へ」をクリックします。

![winenv5](/dbms-8.5/installation/windows/winenv5.png)

5. **「接続を許可する」**を選択し、**「次へ」**をクリックします。

![winenv6](/dbms-8.5/installation/windows/winenv6.png)

6. **「ドメイン」「プライベート」「パブリック」**を選択し、**「次へ」**をクリックします。

![winenv7](/dbms-8.5/installation/windows/winenv7.png)

7. **「名前」**と**「説明」**を入力し、**「完了」**をクリックします。

![winenv8](/dbms-8.5/installation/windows/winenv8.png)
    
