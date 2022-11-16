"""
monitorui.py is the main script which runs the MONITORUI
"""
from sys import platform
from time import sleep, time
from random import randint
from pathlib import Path
from datetime import datetime
from os import chdir, path, mkdir, remove
from colorama import Fore, Style, init
from modules.monitored_site import MonitoredSite
from modules.functions import common_func as cf
init()

SCRIPT_LOOP = True

while SCRIPT_LOOP:

    # Change dir to actual script location (useful on Windows), global settings
    chdir(path.dirname(path.abspath(__file__)))
    # get actual time and write script start date in to script log
    scriptstarttime = datetime.now()
    if not path.exists('.//logs'):
        mkdir('.//logs')
    logpath = f'.//logs//monitoring_{datetime.now().strftime("%d%m%Y")}.log'
    LOG_DIR_PATH = './/logs//'
    message = f'--Starting monitoring at {scriptstarttime}-- \r\n'
    print(message)
    cf.write_file_append(logpath, message)

    # Read config file and set password in to config list
    config = cf.read_json('.//config//config.json')
    sitesfolder = config['sitesfolder']

    # Look somewhere else, there is nothing to do
    smptpassfilelocation = config['smtppassfilelocation']
    if path.isfile(smptpassfilelocation):
        config['smtppass'] = str(cf.read_file(smptpassfilelocation)[0])

    if 'workinloop' not in config:
        config['workinloop'] = False

    if 'loopintervallmin' not in config:
        config['loopintervallmin'] = 500

    if 'loopintervallmax' not in config:
        config['loopintervallmax'] = 500

    if 'logsretention' not in config:
        config['logsretention'] = None

    # Read sites in to list
    listofsites = cf.list_directories(sitesfolder)

    # for cycle for each site from list, invoke class end perfom monitoring actions
    for site in listofsites:
        # siteconfig = cf.read_json(sitesfolder +clear site + '//configsite.json')
        # workingsite = monitoredSite(config, siteconfig, site)
        # workingsite.get_response_code()
        try:
            siteconfig = cf.read_json(sitesfolder + site + '//configsite.json')
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
            if datetime.today().weekday() in siteconfig['monitoringdays']:
                if datetime.now().strftime("%H%M%S") >= siteconfig['monitoringstart']\
                        and datetime.now().strftime("%H%M%S") <= siteconfig['monitoringend']:
                    workingsite = MonitoredSite(config, siteconfig, site)
                    if siteconfig['checkhostping']:
                        workingsite.site_check_ping()
                    if siteconfig['checkhostport']:
                        workingsite.site_check_port()
                    if siteconfig['checksiteresponsecode']:
                        workingsite.site_check_response_code()
                    if siteconfig['checkcertificateexpiration']:
                        workingsite.site_certificate_expiration_check()
                    if siteconfig['checksitecontent']:
                        workingsite.sitei_check_site_content()
                    if siteconfig['checkwmiprocesses']:
                        workingsite.site_check_wmni_process()
                    if siteconfig['checksqllitescript']:
                        workingsite.site_check_sqlite_script()
                    if siteconfig['checksqloraclescript']:
                        workingsite.site_check_oracle_script()

                    workingsite.removesite_logs()
                    try:
                        del workingsite
                    except Exception as e:
                        message = f'{site} Failed removing object: \r\n {e}'
                        print(Fore.RED + message + Style.RESET_ALL)
                        cf.write_file_append(logpath, f'{message}')
                else:
                    print(f"-Site {site} skipped, out of working hours- \r\n")
            else:
                print(f"-Site {site} skipped, not sheduled for today \r\n")
        except Exception as e:
            message = f'{site} skipped on Exception, issues found: \r\n {e}'
            print(Fore.RED + message + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message}')

    # Clean up log files

    if config['logsretention'] is not None:

        try:
            for item in Path(LOG_DIR_PATH).glob('*.log'):
                if item.is_file():
                    try:
                        if (Path.stat(item).st_mtime) < time() - config['logsretention'] * 86400:
                            remove(item)
                    except Exception as remove_e:
                        message = f'Failed to remove log file: {remove_e}\r\n'
                        print(Fore.RED + message + Style.RESET_ALL)
                        cf.write_file_append(logpath, f'{message}')
        except Exception as e:
            message = f'Failed to oparate with log folder during celaning log files: {e}\r\n'
            print(Fore.RED + message + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message}')

    # Calculte running time of script
    message = f'--Monitoring execution time: {str(datetime.now() - scriptstarttime)}--\r\n'
    print(message)
    cf.write_file_append(logpath, message)
    # Work in loop condition
    if config['workinloop'] is False:
        SCRIPT_LOOP = False

    if config['workinloop'] is True:
        sleep(randint(config['loopintervallmin'], config['loopintervallmax']))
