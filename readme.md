# <span style="color://37ABC8">Monitor</span><span style="color://FF6600">~~UI~~</span> - Infrastructure and Services monitoring

Monitor~~UI~~ is infrastructure, network and services monitoring, with using of basic protocols (no agents installation on hosts required ).

First, there is no UI (User interface), it was thought about it at beginning, but there are more important thinks, like life itself :) But do not worry, MonitorUI does great job, it has really good notifications via mail and very nice logs. Who wants another dashboard when you can integrate with such great tool like Grafana, Kibana, Splunk (this is not the advertisement) etc ... Also it does pretty nice color outputs on terminal (so your eyes will not be lost in shadows).

![MonitorUI](/img/monitorui.png)

## Ok, stop talking, now what Monitor~~UI~~ can do for you ?

### General

* Agents / probes free monitoring - No installation required on monitored hosts / clients, Monitor~~UI~~ use wide general TCP/UDP protocols and Services (HTTP / HTTPS, WMI, DB connectors).

* Supported OSses: Windows, Linux, Freebsd, Unix etc. Also you can run it from the cloud or anywhere where Python 3 Works, like [https://www.pythonanywhere.com](https://www.pythonanywhere.com) (again, this is not an advertisement)

#### Network monitoring

* Ping
* Port (unlimited ports per host)
* SSL Certificate expiration check (configurable notification dates before certificates expiration)

#### Web functions monitoring

* URL Response Code (useful to check if site works, or monitor health-checks)
* Web changes (check if web pages has changed, useful to monitor if website, health check is same or changed, yes you can define to ignore some elements if they are generated dynamically)

#### Oracle DB

* Query compare against expected result

#### SQLite DB

* Query compare against expected result

#### WMI - MS Windows

* Windows processes (check if Windows process(es) runs or not) *this works only if Monitor~~UI~~ is installed on Windows, Windows like windows :)

#### Other type of check needed? Write us feedback, we are open to all of ideas ;)

## Performance and where I can use it ?

### Performance

Currently the biggest deployment about which we know is monitoring of 150+ servers and on each it performs 3 - 4 checks, which means 600 checks each few minutes. The MonitorUI can performs this in cca. 15 seconds, which is quite good. And we are working on more optimization. Enough of self-praise!

### Where I Can use it ?

There are no limitations from us, but it fits everywhere where you need monitor internal or external serveries and infrastructure and you do not see that worth for it or can't be deployed large hard to configure solution or due to licenses. Monitor~~UI~~ does not use any probes, so it literary works Out of Box.

## I want it, how can I install ?

### Windows

1. Download and install Python version 3.8x - 3.10.x from [https://www.python.org](https://www.python.org) which fits to your Windows version. During the installation do not forget to **"check"** on first screen **"Add python.exe to PATH"**. If you missed it, do not wory, just uninstall and install Python 3.10.x again and check the "add path". By end of installation process select **Disable path length limit**.

    * Why Python 3.8.x - 3.10.x? it is becasue compatibility of Oracle (cx_oracle). If you want newest python, there is no issue, just remove "cx_oracle" from "\install\requirements_win.txt".

2. Restart machine (PC, Server etc ..), to activate the PATH Variable

3. Download Monitor~~UI~~ from Github [https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip](https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip)

4. Unzip "monitorui-master.zip" in to folder where you want to have Monitor~~UI~~ placed.

5. In the folder "monitorui-master\install" is "install_windows.bat". Run this script. It will install necessary python packages from pypi.org (store for python libraries)

        install_windows.bat

6. That is all :) Now proceed to Configuration part

    * Also you can use git clone, make Python venv, but this is out of scope of this manual (we want keep it simple)

### Linux / FreeBSD (We really like Freebsd and Yes this is ad :))

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

2. Download Monitor~~UI~~ from Github [https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip](https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip)

3. Unzip "monitorui-master.zip" in to folder where you want to have Monitor~~UI~~ placed.

4. In the folder "monitorui-master/install" is "install_freebsd.sh". Run this script. It will install necessary python packages from pypi.org (store for python libraries)

    Run from from ./install directory:

        sh install_linux_freebsd.sh

5. That is all :) Now proceed to Configuration part

    * Also you can use git clone, make Python venv, but this is out of scope of this manual (we want keep it simple)

## Configuration

After the installation in there will be tow directories in Monitor~~UI~~ folder: "config" and "Sites". Both folder contains example values of general Monitor~~UI~~ configuration and sites to be monitored

### General Configuration

config.json under config folder contains general configuration for Monitor~~UI~~. All values are optional, is recommended to fullfil SMTP - email configuration parameters as minimum.

```json
{
  "sitesfolder": ".//sites", // Where are stored sites to be monitored (Optional, default value: .//sites)
  "smtpserver": "smtp.gmail.com", // SMTP server for notification (Optional, default value: '')
  "smtpport": 587, // SMTP server for notification (Optional, default value: 25)
  "smtpssl": true, // SSL over SMTP (Optional, default value: False)
  "smtpauthentication": true, //User / password authentication (Optional, default value: False)
  "smtpuser": "", // SMTP User (Optional, default value: "")
  "smtppassfilelocation": ".//config//5fbTeZ9GUsYeaHxF", //SMTP Password taken from file (optional)
  "smtppass": "", // If password file does not exist, use this value (Optional, default value: '')
  "from_email": "xyz@gmail.com", // Email from which notification being send (Optional, default value: '')
  "workinloop": false, // In case that you want to run monitoring as service (Optional, default value: False)
  "loopintervallmin": 5, // If workinloop = True, set minimal time in sec. to re-run monitoring (Optional, default value: 300)
  "loopintervallmax": 10, // If workinloop = True, set maximal time in sec. to re-run monitoring (Optional, default value: 300)
  "logsretention": 60, // Logs Retention period, if not used or None, no logs retention (Optional, default value: None)
  "log_daily_feed": true, // Copy last daily log of each site under ./logs/log_daily_feed/ for logs processing (Optional, default value: False)
  "parallel_checks": true, // Monitoring can run the checks of sites parallel (Optional: default value: False) 
  "max_workers": 5, // Maximum parallel threads (Optional, default value: 5)  "timeout_email": 10 // Set time out for email services (Optional, default value: None)
}
```

Please use the example config from folder ./config/config.json, as this commented documentation is not valid JSON.

### Site Configuration

```json
{
  "sitename": "Github", // Name of the site 
  "hostname": "www.github.com", // Hostname for ping, port checks
  "siteurl": "https://github.com/pallets/click", // URL Site for SSL Certificate check, WEB check, HTTPs response check
  "siteenviroment": "PROD", // Type of environment (Production, tests, etc)
  "systemname": "github", // Name of the system, or different grouping (Optional, Placeholder, not currently used)
  "monitoringstart": "000000", // When monitor of host start (Optional)
  "monitoringend": "235959", // When monitor of host stops (Optional)
  "tags": [""],
  "monitoringdays": [0, 1, 2, 3, 4, 5, 6], // Which days is monitoring enabled on the host, 0 = sunday (Optional)
  "emailrecipients": [ "someemail@gmail.com" ], // List of recipients example: [ "aa@aa.com"] or [ "aa@aa.com", "bb@bb.com" ] (Optional)
  "checkhostping": true, // Switch to enable or disable Ping check (Optional, default value: False)
  "checkhostport": true, // Switch to enable or disable Port check (Optional, default value: False)
  "hostports": [ "443", "80" ], // Ports to be checked. Example:  [ "80" ]  or [ "443", "80" ] (Mandatory if checkhostport = true , default value: "")
  "checkcertificateexpiration": true, // Switch to enable or disable Certificate Expiration check (Optional, default value: False)
  "certificateexpirationtrigger1": 30, // How many days before certificate expiration notification will trigger (Optional, default value: 30)
  "certificateexpirationtrigger2": 20, // How many days before certificate expiration notification will trigger (Optional, default value: 20)
  "certificateexpirationtrigger3": 10, // How many days before certificate expiration notification will trigger (Optional, default value: 10)
  "certificateexpirationtrigger4": 5, // How many days before certificate expiration notification will trigger (Optional, default value: 5)
  "certificateport": 443, //Certificate Expiration Port check (Optional, default value: 443)
  "checksiteresponsecode": true, // Switch to enable or disable Port check (Optional, default value: False) 
  "siteresponsecode": "200", // Expected response code
  "checksitecontent": false, // Check site for the content, if changed during the checks (Optional, default value: False) 
  "htmlignoreelements": [ "" ], // List of elements which need to be ignored, useful if some of the page is dynamically changing.
  "sslcertificatevalidation": true, // Switch to enable or disable certificate validation, useful is you are using self generated certificate or is on the way proxy server etc ... (Optional, default value: True)
  "checkwmiprocesses": false, // Switch to enable or disable WMI Process check check, only for Windows (Optional, default value: False)
  "wmiprocesses": [""],
  "checksqllitescript": false, // List of processes to be check if they are running [ "Process_name1","Process_name1" ]
  "sqlitdbepath": "", // path to SQL Lite DB relatively to the MonitorUI folder
  "sqlitedbname": "",
  "sqlliteevaluateoperator": "",
  "sqlitesqlcommand": "",
  "sqliteexpectedvalue": "",
  "checksqloraclescript": false,
  "oracleuser": "",
  "oraclepassword": "",
  "oracledsn": "",
  "oracleevaluateoperator": "",
  "oraclesqlcommand": "",
  "oracleexpectedvalue": ""
}

## How to run 

### Logs

## Oracle DB drivers
