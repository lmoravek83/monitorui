# <span style="color:#37ABC8">Monitor</span><span style="color:#FF6600">~~UI~~</span>

First, there is no UI (User interface), it was thought about it at begining, but there are more important thinks, like life itself :) But do not wory, MonitorUI does great job, it has realy good notifications via mail and very nice logs. Who wants another dashboard when you can integrate with such great tool like Grafana, Kibana, Splunk (this is not the advertisment) etc ... Also it does prety nice color outputs on terminal (so your eyes will not be lost in shadows).

## Ok, stop talking, now what Monitor~~UI~~ can do for you ?

### General

* Agents / probes free monitoring - No installation required on monitored hosts / clients, Monitor~~UI~~ use wide general TCP/UDP protocols and Services (HTTP / HTTPS, WMI, DB connectors).

* Supported OSses: Windows, Linux, Freebsd, Unix etc. Also you can run it from the cloud or anywhere where Python 3 Works, like [https://www.pythonanywhere.com](https://www.pythonanywhere.com) (again, this is not an advertisment)

### Network monitoring

* Ping
* Port (unlimited ports per host)
* SSL Certificate expiration check (configurable notification dates before certificates expiration)

### Web functions monitoring

* URL Response Code (usefull to check if site works, or monitor healthchecks)
* Web changes (check if web pages has changed, usefull to monitor if website, health check is same or changed, yes you can define to ignore some elemets if they are generated dynamicly)

### Oracle DB

* Query compare against expected result

### SQLite DB

* Query compare against expected result

### WMI - MS Windows

* Windows processes (check if Windows proces(es) runs or not) *this works only if Monitor~~UI~~ is installed on Windows, Windows like windows :)

### Other type of check needed? Write us feedback, we are open to all of ideas ;)

## Performace and where I can use it ?

### Performance

Currently the bigest deployment about which we know is monitoring of 150+ servers and on eacch it perfroms 3 - 4 checks, which means 600 checks each few minuts. The MonitorUI can performs this in cca. 15 seconds, which isquite good. And we are working on more optimalitazion. Enoug of self-praise!

### Where I Can use it ?

There are no limitations from us, but it fits everywhere where you need monitor internal or external serverces and ifrastructure and you do not see that worth for it or can't be deployed large hard to configure solution or due to licneses. Monitor~~UI~~ does not use any probes, so it lieterraly works Out of Box.

## I want it, how can I install ?

### Windows

1. Download and install Python version 3.8x - 3.10.x from [https://www.python.org](https://www.python.org) which fits to your Windows version. During the instlation do not forget to **"check"** on first instalator screen **"Add python.exe to PATH"**. If you missed it, do not wory, just uninstall and install Python 3.10.x again and check the "add path". By end of instllation process selecet **Disable path lenght limit**.

    * Why Python 3.8.x - 3.10.x? it is becasue compatibility of Oracle (cx_oracle). If you want newest python, there is no issue, just remove "cx_oracle" from "\install\requirements_win.txt".

2. Restart machine (PC, Server etc ..), to activate the PATH Variable

3. Download Monitor~~UI~~ from Github [https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip](https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip)

4. Unzip "monitorui-master.zip" in to folder where you want to have Monitor~~UI~~ placed.

5. In the folder "monitorui-master\install" is "install_windows.bat". Run this sript. It will install necessary python packages from pypi.org (store for python libraries)

        install_windows.bat

6. That is all :) Now proceed to Configration part

    * Also you can use git clone, make Python Venv, but this is out of scope of this manual (we want keep it simple)

### Linux / FreeBSD (We realy like Freebsd and Yes this is ad :)) / etc

1. Install Python 3.8.x - 3.10.x (source code, packages, whatever suits to you) and python pip package manager. If you already have these rquirements, you can skip this point

    * Example for Debian (type) distribudiotns:

            sudo apt istall python3

            sudo apt install python3-pip

    * Example for FreeBSD (priviledged to install right is rquired)

            pkg istall python3

            pkg apt install python3-pip

    * Why Python 3.8.x - 3.10.x? it is becasue compatibility of Oracle (cx_oracle). If you want newest python, there is no issue, just remove "cx_oracle" from "\install\requirements_win.txt".

2. Download Monitor~~UI~~ from Github [https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip](https://github.com/lmoravek83/monitorui/archive/refs/heads/master.zip)

3. Unzip "monitorui-master.zip" in to folder where you want to have Monitor~~UI~~ placed.

4. In the folder "monitorui-master\install" is "install_linux.sh". Run this sript. It will install necessary python packages from pypi.org (store for python libraries)

        sh install_linux_freebsd.sh

5. That is all :) Now proceed to Configration part

    * Also you can use git clone, make Python Venv, but this is out of scope of this manual (we want keep it simple)

### Freebsd (We realy like Freebsd and Yes this is ad :))

## Configuration

### General Configuration

### Site Configuration

#### Oracle DB drivers
