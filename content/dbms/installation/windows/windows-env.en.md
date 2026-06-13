---
title : 'Preparing Windows Environment for Installation'
type : docs
weight: 10
---

## Open Firewall Port

If you install Machbase in Windows, you must open the port that Machbase uses in the Windows Firewall.

In general, Machbase uses the native listener port **5656** and the HTTP REST
port **5657**.

1. To register the port on the  firewall , select Control Panel - Windows Firewall or Windows Defender Firewall. 
    On the Run screen, click the "Advanced Settings" menu.

![winenv1](/dbms/installation/windows/winenv1.png)

2. Under Advanced Settings, select **Inbound Rules - New Rule** and click.

![winenv2](/dbms/installation/windows/winenv2.png)

![winenv3](/dbms/installation/windows/winenv3.png)

3. When the New Rule Setup Wizard window is displayed, select the Port option as shown below and click Next.

![winenv4](/dbms/installation/windows/winenv4.png)

4. Select the **TCP(T)** option, enter **5656,5657** in the **Specific Local Ports** field, and then click Next.

![winenv5](/dbms/installation/windows/winenv5.png)

5. Select the **Allow The Connection** option and click **Next**.

![winenv6](/dbms/installation/windows/winenv6.png)

6. Check **Domain** , **Private** , and **Public** and click **Next**.

![winenv7](/dbms/installation/windows/winenv7.png)

7. Complete the **Name** and **Description** fields, and then click **Finish**.

![winenv8](/dbms/installation/windows/winenv8.png)
    
