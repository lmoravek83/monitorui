"""
monitorui.py is the main script which runs the MONITORUI
"""
from sys import platform
from time import sleep, time
from random import randint
from pathlib import Path
from datetime import datetime
from os import chdir, path, mkdir, remove
import concurrent.futures
from colorama import Fore, Style, init
from modules.monitored_site import MonitoredSite
from modules.functions import common_func as cf
init()


def go_monitor(site):
    try:
        # set site config path for current minotred site
        siteconfig = cf.read_json(sitesfolder + "//" + system + "//" + site + '//configsite.json')
        # set site folder for current minotred site
        sitefolder = sitesfolder + "//" + system + "//" + site
        # set log daily feed folder
        logdailyfeedfolder = './/logs/log_daily_feed'
        if 'monitoringstart' not in siteconfig:
            siteconfig['monitoringstart'] = '000000'

        if 'monitoringend' not in siteconfig:
            siteconfig['monitoringend'] = '235959'

        if 'monitoringdays' not in siteconfig:
            siteconfig['monitoringdays'] = [0, 1, 2, 3, 4, 5, 6]

        if 'checkhostping' not in siteconfig:
            siteconfig['checkhostping'] = False

        if 'checksiteresponsecode' not in siteconfig:
            siteconfig['checksiteresponsecode'] = False

        if 'checksitecontent' not in siteconfig:
            siteconfig['checksitecontent'] = False

        if 'checkcertificateexpiration' not in siteconfig:
            siteconfig['checkcertificateexpiration'] = False

        if 'checkwmiprocesses' not in siteconfig:
            siteconfig['checkwmiprocesses'] = False
        # WMI need support of Win32, if monitoring runs on non Win32 compatible system,
        # WMI is set to disabled
        if platform != "win32":
            siteconfig['checkwmiprocesses'] = False
        if 'checksqllitescript' not in siteconfig:
            siteconfig['checksqllitescript'] = False
        if 'checksqloraclescript' not in siteconfig:
            siteconfig['checksqloraclescript'] = False
        # Check if monitored site is alowed for current dayd
        if datetime.today().weekday() in siteconfig['monitoringdays']:
            if datetime.now().strftime("%H%M%S") >= siteconfig['monitoringstart']\
                    and datetime.now().strftime("%H%M%S") <= siteconfig['monitoringend']:
                # Crete instance of class Monitored Site
                workingsite = MonitoredSite(config, siteconfig, site, sitefolder, logdailyfeedfolder)
                if siteconfig['checkhostping']:
                    workingsite.site_check_ping()
                if siteconfig['checkhostport']:
                    workingsite.site_check_port()
                if siteconfig['checksiteresponsecode']:
                    workingsite.site_check_response_code()
                if siteconfig['checkcertificateexpiration']:
                    workingsite.site_certificate_expiration_check()
                if siteconfig['checksitecontent']:
                    workingsite.site_check_site_content()
                if siteconfig['checkwmiprocesses']:
                    workingsite.site_check_wmni_process()
                if siteconfig['checksqllitescript']:
                    workingsite.site_check_sqlite_script()
                if siteconfig['checksqloraclescript']:
                    workingsite.site_check_oracle_script()
                workingsite.copy_log_for_agregation()
                # Remove logs in Monitored Site - Log Retention
                workingsite.removesite_logs()
                # Remove instance of MonitoredSite Class
                try:
                    del workingsite
                except Exception as exep:
                    message = f'{site} Failed removing object: \r\n {exep}'
                    print(Fore.RED + message + Style.RESET_ALL)
                    cf.write_file_append(logpath, f'{message}')
            else:
                print(f"-Site {site} skipped, out of working hours- \r\n")
        else:
            print(f"-Site {site} skipped, not sheduled for today \r\n")
    except Exception as exep:
        message = f'{datetime.now()}|MONITORING_EXECUTION|ERROR|Skipped on Exception, issues found: {exep} \r\n'
        print(Fore.RED + message + Style.RESET_ALL)
        cf.write_file_append(logpath, f'{message}')


# Change dir to actual script location (useful on Windows), global settings
chdir(path.dirname(path.abspath(__file__)))
# get actual time and write script start date in to script log
scriptstarttime = datetime.now()
if not path.exists('.//logs'):
    mkdir('.//logs')
logpath = f'.//logs//monitoring_{datetime.now().strftime("%d%m%Y")}.log'
if not path.exists('.//logs/log_daily_feed'):
    mkdir('.//logs/log_daily_feed')
LOG_DIR_PATH = './/logs//'
message = f'{datetime.now()}|MONITORING_EXECUTION|INFO|Monitoring Start\r\n'
print(message)
cf.write_file_append(logpath, message)

# Read config file and set password in to config list
config = cf.read_json('.//config//config.json')
# sitesfolder = config['sitesfolder']
if 'sitesfolder' in config:
    sitesfolder = config['sitesfolder']
else:
    sitesfolder = './/sites'

# Look somewhere else, there is nothing to do
smptpassfilelocation = config['smtppassfilelocation']
if path.isfile(smptpassfilelocation):
    config['smtppass'] = str(cf.read_file(smptpassfilelocation)[0])

if 'workinloop' not in config:
    config['workinloop'] = False

if 'loopintervallmin' not in config:
    config['loopintervallmin'] = 300

if 'loopintervallmax' not in config:
    config['loopintervallmax'] = 500

if 'logsretention' not in config:
    config['logsretention'] = None
    
if 'paralel_checks' not in config:
    config['paralel_checks'] = True

SCRIPT_LOOP = True

while SCRIPT_LOOP:
    listofsystems = cf.list_directories(sitesfolder + "//")
    # print(listofsystems)
    for system in listofsystems:
        # Read sites in to list
        listofsites = cf.list_directories(sitesfolder + "//" + system + "//")
        if config['paralel_checks']:
            if __name__ == '__main__':
                # with multiprocessing.Pool() as pool:
                #     pool.map(go, listofsites)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(go_monitor, site) for site in listofsites]
                    concurrent.futures.wait(futures)
        else:
            # for cycle for each site from list, invoke class end perfom monitoring actions
            for site in listofsites:
                go_monitor(site)

    # Clean up log files
    # Log retetion for MonitoringUI
    if config['logsretention'] is not None:

        try:
            for item in Path(LOG_DIR_PATH).glob('*.log'):
                if item.is_file():
                    try:
                        if (Path.stat(item).st_mtime) < time() - config['logsretention'] * 86400:
                            remove(item)
                    except Exception as remove_e:
                        message = f'{datetime.now()}|MONITORING_EXECUTION|ERROR|Failed to remove log file: {remove_e}\r\n'
                        print(Fore.RED + message + Style.RESET_ALL)
                        cf.write_file_append(logpath, f'{message}')
        except Exception as e:
            message = f'{datetime.now()}|MONITORING_EXECUTION|ERROR|Failed to oparate with log folder during celaning log files: {e}\r\n'
            print(Fore.RED + message + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message}')

        try:
            for item in Path(LOG_DIR_PATH + 'log_daily_feed//').glob('*.log'):
                if item.is_file():
                    try:
                        if (Path.stat(item).st_mtime) < time() - config['logsretention'] * 86400:
                            remove(item)
                    except Exception as remove_e:
                        message = f'{datetime.now()}|MONITORING_EXECUTION|ERROR|Failed to remove log file: {remove_e}\r\n'
                        print(Fore.RED + message + Style.RESET_ALL)
                        cf.write_file_append(logpath, f'{message}')
        except Exception as e:
            message = f'{datetime.now()}|MONITORING_EXECUTION|ERROR|Failed to oparate with log folder during celaning log files: {e}\r\n'
            print(Fore.RED + message + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message}')

    if config['workinloop'] is False:
        SCRIPT_LOOP = False

    if config['workinloop'] is True:
        # Work in loop condition
        sleep(randint(config['loopintervallmin'], config['loopintervallmax']))


# Calculte running time of script
message = f'{datetime.now()}|MONITORING_EXECUTION|INFO|Monitoring End|Monitoring execution time = {str(datetime.now() - scriptstarttime)}\r\n'
print(message)
cf.write_file_append(logpath, message)
# Work in loop condition
