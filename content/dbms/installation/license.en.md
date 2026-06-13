---
title : 'License Installation'
type : docs
weight: 40
---

License key installation is usually performed after MACHBASE installation is finished. If you do not install a specific license after installation, you can use MACHBASE with some restrictions. This section describes MACHBASE's license policy, structure, and installation method.


## License File Structure

The MACHBASE license is managed in the license.dat file. Licenses purchased for the product or for testing are displayed in a text file.

```bash
mach@localhost:~$ cat license.dat 
 
\#License ID: 00000001
\#Issue DATE: 20991231
\#License Type\(Version 3\): FOGUNLIMITED
\#Company: MACHBASE
\#Project\(Product\): NONE
\#Country Code: KR
 dXlIm7cdJjV1eUibtx0mNQ-GMxH+xLveLI-ewu63w8qMx33l77I+Ot0hY9sBCI...
```


## No License File

The server will run even if there is no license, but there are some limitations. The server can only be used for evaluation purposes, so if you intend to use it formally, you must obtain the license in a legitimate procedure.

If there is no license file, the following functional limitations will exist.

    1. If you enter more than 100 million records through the Append protocol in one session, a warning message is displayed. Append input is then stopped. The input limit state is released only when the server is restarted.

    2. When creating a tablespace, you can not create more than two disk directories. If you use more than one disk, the following warning indicating that the parallel I / O function for high performance data input can not be used will be displayed. 

```bash
CREATE TABLESPACE tbs1 DATADISK disk1 (disk_path="tbs1_disk1"), disk2 (disk_path="tbs1_disk2"), disk3 (disk_path="tbs1_disk3");
[ERR-00867 : Error in adding disk to tablespace. You cannot use multiple disks for tablespace without valid license.]
```


## License Installation

The MACHBASE license must be installed in $MACHBASE_HOME/conf, and the default name is license.dat .

Copy the license file to `$MACHBASE_HOME/conf`.

At this time, the name of the license file issued must be changed to **license.dat** and copied. Then, when the server is started, it will determine if the license is appropriate and begin the installation.

Launch **machadmin -t 'licensefile_path'**

The advantage of this method is that it can be easily installed with commands without having to adjust the license file name or location. 

Installing as a query: This is a way to install a license using a query statement while the server is running.


## Verifying License Installation

### License Installed

If the license file is installed, the following is displayed in machbase.trc after the server is started.

```bash
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [License ID] [00000001]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Issue DATE] [20991231]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [License Type(Version 3)] [FOGUNLIMITED]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Company] [MACHBASE]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Project(Product)] [NONE]
[2026-04-16 22:22:08 P-101180 T-135618783719296][INFO] LICENSE [Country Code] [KR]
```

You can also use the machadmin -f command.

### License Not Installed

If the license file is not installed or an invalid file is used, check the license status with `machadmin -f` or `V$LICENSE_INFO`. In Standard 8.5, the same Version 3 fields are used, and violation details are exposed through the `VIOLATE_STATUS` and `VIOLATE_MSG` columns of `V$LICENSE_INFO`.

```sql
SELECT ID, ISSUE_DATE, TYPE, CUSTOMER, PROJECT, COUNTRY_CODE,
       INSTALL_DATE, VIOLATE_STATUS, VIOLATE_MSG
FROM V$LICENSE_INFO;
```
