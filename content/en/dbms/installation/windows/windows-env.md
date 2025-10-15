---
type: docs
title : 'Preparing Windows Environment for Installation'
type : docs
weight: 10
---

## Open Firewall Port

If you install Machbase in Windows, you must open the port that Machbase uses in the Windows Firewall.

In general, Machbase uses  two ports: **5656 and 5001**

1. To register the port on the  firewall , select Control Panel - Windows Firewall or Windows Defender Firewall. 
    On the Run screen, click the "Advanced Settings" menu.

![winenv1](../winenv1.png)

2. Under Advanced Settings, select **Inbound Rules - New Rule** and click.

![winenv2](../winenv2.png)

![winenv3](../winenv3.png)

3. When the New Rule Setup Wizard window is displayed, select the Port option as shown below and click Next.

![winenv4](../winenv4.png)

4. Select the **TCP(T)** option , enter **5656,5001** in the **Specific Local Ports** field, and then click Next.

![winenv5](../winenv5.png)

5. Select the **Allow The Connection** option and click **Next**.

![winenv6](../winenv6.png)

6. Check **Domain** , **Private** , and **Public** and click **Next**.

![winenv7](../winenv7.png)

7. Complete the **Name** and **Description** fields, and then click **Finish**.

![winenv8](../winenv8.png)
    
