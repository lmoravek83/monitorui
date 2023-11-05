![MonitorUI](/img/monitorui_logo.png)

# <span style="color://37ABC8">**Monitor</span><span style="color://FF6600">~~UI~~</span> - Infrastructure, network and services monitoring**

Monitor~~UI~~ is agent less infrastructure, network and services monitoring

First, there is no UI (User interface), it was thought about it at beginning, but there are more important things, like life itself :) But do not worry, MonitorUI does great job, it has really good notifications via mail and very nice logs. Who wants another dashboard when you can integrate through logs with such great tool like Grafana, Kibana, Splunk (this is not the advertisement) etc. Also it does pretty nice color outputs on terminal, so your eyes will not be lost in shadows.

Console output
![MonitorUI](/img/monitorui.png)

## **Ok, what Monitor~~UI~~ can do for me ?**

### _Generally_

* Agents / probes free monitoring - No installation required on monitored hosts / clients, Monitor~~UI~~ use wide general TCP/UDP protocols and Services (HTTP / HTTPS, WMI, DB connectors) to monitor the hosts.

* Supported OSses: Windows, Linux, Freebsd, Unix etc. Also you can run it from the cloud or anywhere where Python 3 works, like [https://www.pythonanywhere.com](https://www.pythonanywhere.com) (again, this is not an advertisement, just hints).

* Advance notification - email recipients configurable per monitored site (monitored host)

* Log format is prepared for machine processing

#### _Network monitoring_

* Ping
* Port (unlimited ports per host)
* SSL Certificate expiration check (configurable notification period before certificates expiration)

#### _Web functions monitoring_

* URL Response Code (useful to check if site is reachable or monitor health-checks)
* Web changes (check if web pages has changed between check, useful to monitor if website, health check is same or changed. You can define to ignore HTML elements if they are generated dynamically)

#### _Oracle DB_

* SQL Query to compare against expected result, need to uncoment cx-Oracle in /install/requirements_win.txt, requirements_linux_freebsd.txt

#### _SQLite DB_

* SQL Query to compare against expected result

#### _WMI - MS Windows_

* Windows processes, check if Windows process(es) runs or not. (This functionality is available only if Monitor~~UI~~ is installed on Windows)

Other type of check needed? Write us feedback, we are open to all of ideas ;).

## **Performance and where I can use it ?**

### **Performance**

Currently the biggest deployment about which we know is monitoring of 150+ servers and on each it performs 3 - 4 checks, which means 600 checks each few minutes. The MonitorUI can performs this in cca. 15 seconds (quite good).

### **Where I Can use it ?**

There are no limitations from us, it fits everywhere where you need monitor internal or external services and infrastructure. Monitor~~UI~~ does not use any probes, so it literary works Out of Box.

## **I want it, how can I install ? (Full installation steps, including Python)**

### **Windows**

1. Download and install Python version 3.8x - 3.10.x from [https://www.python.org](https://www.python.org) which fits to your Windows version. During the installation do not forget to **"check"** on first screen **"Add python.exe to PATH"**. If you missed it, do not worry, just uninstall and install Python 3 again and check the "add path". By end of installation process select **Disable path length limit**.

    * Why Python 3.8.x - 3.10.x? it is because compatibility of Oracle (cx_oracle). If you want newest python, there is no issue, just remove "cx_oracle" from "\install\requirements_win.txt"
    * If you do not want to use OracleDB monitoring script, use any new python

2. Restart machine (PC, Server etc ..), to activate the PATH Variable

3. Download Monitor~~UI~~ from Github [https://github.com/lmoravek83/monitorui/](https://github.com/lmoravek83/monitorui/)

4. Unzip from "monitorui-[version].zip" content in to folder where you want to have Monitor~~UI~~ placed

5. In the folder "monitorui-master\install" is **"install_windows.bat"**. Running this script It will be installed necessary python packages from pypi.org (store for python libraries)

        install_windows.bat

6. That is all :) Now proceed to Configuration part

    * Also you can use git clone, make Python venv, but this is out of scope of this manual (we want keep it simple)

### **Linux / FreeBSD**

1. Install Python 3.8.x - 3.10.x (source code, packages, whatever suits to you) and python pip package manager. If you already have these requirements, you can skip this point

    * Example for Debian (type) distribution:

            sudo apt install python3

            sudo apt install python3-pip

    * Example for FreeBSD (privileged account to install right is required)

            pkg pkg install python39

            pkg pkg install py39-pip

    * Example for FreeBSD (sudo users)

            sudo pkg install python39

            sudo pkg apt install py39-pip

    * Why Python 3.8.x - 3.10.x? it is because compatibility of Oracle (cx_oracle). If you want newest python, there is no issue, just remove "cx_oracle" from "\install\requirements_win.txt".
    * With similar way is possible to install on all unix(like) systems

2. Download Monitor~~UI~~ from Github [https://github.com/lmoravek83/monitorui/releases](https://github.com/lmoravek83/monitorui/releases)

3. Unzip from "monitorui-[version].zip" content in to folder where you want to have Monitor~~UI~~ placed

4. In the folder "monitorui-master/install" is "**install__linux_freebsd.sh**". Running this script It will be installed necessary python packages from pypi.org (store for python libraries)

    Run from from ./install directory:

        sh install_linux_freebsd.sh

5. That is all :) Now proceed to Configuration part

    * Also you can use git clone, make Python venv, but this is out of scope of this manual (we want keep it simple)

## **Configuration**

After the installation there are two directories in Monitor~~UI~~ folder: **"config"** and **"Sites"**. Both folder contains example values of general Monitor~~UI~~ and sites (monitored hosts) configuration.

### **General Configuration**

**"config.json"** under **"config"** folder contains general configuration for Monitor~~UI~~. All values are optional. Is recommended to fullfil SMTP / email configuration parameters as minimum. Create new one or adjust one which is already there.

```json
{
  "sitesfolder": ".//sites", // Folder where are stored sites to be monitored (Optional, default value: .//sites)
  "smtpserver": "smtp.gmail.com", // SMTP server for email notification (Optional, default value: '')
  "smtpport": 587, // SMTP port of email server (Optional, default value: 25)
  "smtpssl": true, // SSL over SMTP (Optional, default value: False)
  "smtpauthentication": true, // Switch to enable SMTP authentication (Optional, default value: False)
  "smtpuser": "", // SMTP User (Optional, default value: "")
  "smtppassfilelocation": ".//config//5fbTeZ9GUsYeaHxF", //SMTP Password taken from file (optional)
  "smtppass": "", // If password file does not exist, use this value (Optional, default value: '')
  "from_email": "xyz@gmail.com", // Email from which notification being send (Optional, default value: '')
  "workinloop": false, // In case that you want to run monitoring as service (Optional, default value: False)
  "loopintervallmin": 5, // If workinloop = True, set minimal time in sec. to re-run monitoring (Optional, default value: 300)
  "loopintervallmax": 10, // If workinloop = True, set maximal time in sec. to re-run monitoring (Optional, default value: 300)
  "logsretention": 60, // Logs Retention period, if not used or None, no logs retention (Optional, default value: None)
  "log_daily_feed": true, // Copy last daily log of each site under ./logs/log_daily_feed/ for logs processing (Optional, default value: False)
  "parallel_checks": true, // Monitoring can run the checks of sites (monitored hosts) in parallel (Optional: default value: False) 
  "max_workers": 5, // Maximum parallel threads (Optional, default value: 5)  "timeout_email": 10 // Set time out for email services (Optional, default value: None)
}
```

Use the example config from folder **./config/config.json**, as this commented documentation is not valid JSON.

### **Site Configuration**

#### **How to add new site (host) to be monitored**

    * Note, bellow directory structure use the UNIX convection, For Windows users, just change in your mind during reading "/" with "\" :)

1. Under folder **"./sites/"** create system name folder _(Example: MY_Application_PROD etc.)_ If you extracted package properly, there is already sample folder "git_servers"

2. Under **"./sites/MY_Application_PROD/"** create new site folder _(Example: Server01.mydomain.com)_

    * The final path for example will be **"./sites/MY_Application_PROD/Server01.mydomain.com"**

3. Create new or copy **"configsite.json"** from example **./sites/git_servers/github/** in to your site folder

4. With this approach you can create unlimited sites grouped in to the related folders (based on system, environments etc.)

#### **How to configure site**

For each site is required to create "configsite.json", you can use example which is delivered along with the package.

```json
{
  "sitename": "Github", // Name of the site (monitored host), if not configured, is used direcotry name
  "hostname": "www.github.com", // Hostname for ping, port checks
  "siteurl": "https://github.com/pallets/click", // URL Site for SSL Certificate check, WEB check, HTTPs response check
  "siteenviroment": "PROD", // Type of environment (Production, tests, etc)
  "systemname": "github", // Name of the system, or different grouping and logs identification (Optional), if not configured, is used directory of system
  "monitoringstart": "000000", // From which time is monitoring of site enabled (Optional)
  "monitoringend": "235959", // Until which time is monitoring of site enabled (Optional)
  "tags": [""],
  "monitoringdays": [0, 1, 2, 3, 4, 5, 6], // On which days is monitoring enabled on the host, 0 = sunday (Optional)
  "emailrecipients": [ "someemail@gmail.com" ], // List of recipients example: [ "aa@aa.com"] or [ "aa@aa.com", "bb@bb.com" ] (Optional)
  "checkhostping": true, // Switch to enable or disable Ping check (Optional, default value: False)
  "checkhostport": true, // Switch to enable or disable Port check (Optional, default value: False)
  "hostports": [ "443", "80" ], // Ports to be checked. Example:  [ "80" ]  or [ "443", "80" ] (Mandatory if checkhostport = true , default value: "")
  "checkcertificateexpiration": true, // Switch to enable or disable Certificate Expiration check (Optional, default value: False)
  "certificateexpirationtrigger1": 30, // How many days before certificate expiration notification is triggered (Optional, default value: 30)
  "certificateexpirationtrigger2": 20, // How many days before certificate expiration notification is triggered (Optional, default value: 20)
  "certificateexpirationtrigger3": 10, // How many days before certificate expiration notification is triggered (Optional, default value: 10)
  "certificateexpirationtrigger4": 5, // How many days before certificate expiration notification is triggered (Optional, default value: 5)
  "certificateport": 443, //Certificate Expiration Port check (Optional, default value: 443)
  "checksiteresponsecode": true, // Switch to enable or disable Port check (Optional, default value: False) 
  "siteresponsecode": "200", // Expected response code
  "checksitecontent": false, // Check site for the content, if changed during the checks (Optional, default value: False) 
  "htmlignoreelements": [ "" ], // List of elements which need to be ignored, useful if part of the page is dynamically changed, to avoid false positive results.
  "sslcertificatevalidation": true, // Switch to enable or disable certificate validation, useful is you are using self generated certificate or is between proxy server etc ... (Optional, default value: True)
  "checkwmiprocesses": false, // Switch to enable or disable WMI Process check check, only for Windows (Optional, default value: False)
  "wmiprocesses": [""],
  "checksqllitescript": false, // Switch to enable or disable SQLITE DB sql check check
  "sqlitdbepath": "", // path to SQL Lite DB relatively to the MonitorUI folder
  "sqlitedbname": "", // Filename of SQLITE DB
  "sqlliteevaluateoperator": "", // Evaluate operator < > = !=
  "sqlitesqlcommand": "", // SQL Command to be performed
  "sqliteexpectedvalue": "", // Expected value
  "checksqloraclescript": false, // Switch to enable or disable OracleDB  sql check check
  "oracleu": "", // Oracle user
  "oraclep": "", // Oracle password for defined user
  "oracledsn": "", // Oracle DSN
  "oracleevaluateoperator": "", // Evaluate operator < > = !=
  "oraclesqlcommand": "", // SQL Command to be performed
  "oracleexpectedvalue": "" // Expected value
}
```

### **Oracle DB drivers**

For Oracle DB check needs to be installed oracle Driver.

[Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html)

1. Download **"Basic Light Package"** which suits to your system

2. Unpack in folder where you want to have the Oracle DB drivers

3. Adjust path in **"./modules/functions/oracledb.py"** Line: **"cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_3")"**

## **How to run Monitor~~UI~~**

### **Windows**

run in Windows Command line / Power shell "monitor_ui.bat" or you can add it in scheduled tasks:

    monitorui_run.bat

or

    python monitorui.py

### **Linux**

run in Shell or you can add it in to the **crontab** (do not forget for full path):

    sh monitorui_run.sh

or

    python ./monitorui.py
or

    python3 ./monitorui.py

## **Logs**

Info: Logs keeps same structure, so they can be easily processed (OK, Warning, Error) in to logs machine processing platform (Grafana, Kibana, Splunk etc...)

### **General Logs**

/logs/monitor_DDMMYYYYY.log - store daily logs which contains information from each run, failures and other issues. Also contains when each run starts and ends, including duration

### **Logs for machine data processing** (Splunk, Grafana, Kibana etc ..)

/logs/log_daily_feed/sitename.log - store daily log of each moniterd site / host. in this folder are stored last logs from all minitored sites / hosts.

### **Site logs**

/sites/system/site/logs/sitename_DDMMYYYYY.log contains details of each check and result
