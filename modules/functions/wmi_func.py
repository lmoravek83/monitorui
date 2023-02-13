"""
Module which is covering WMI functions related MONITORUI
"""

from sys import platform
from shutil import copyfile
from datetime import datetime
from os import path
from modules.functions import common_func as cf
try:
    if platform == "win32":
        import wmi
# Do not load WMI library on non Windows system
except Exception as exep:
    print(f'WMI library load failed. {exep}')


def check_wmi_proccesses_file_exist(wmiprocesses_file) -> None:
    """
    If file do not exist, crate emty one
    :param: wmi state file txt
    :param: Expected response code (response code, ping, port, sql output)
    """
    if not path.isfile(wmiprocesses_file):
        cf.write_file(wmiprocesses_file, "")


def check_wmi_process(sitename, env, logpath, hostname, wmiprocesses_file, wmiprocessestmp_file,
                      wmiprocessestmp_file_nosuffix, wmiprocesses, smtpuseremail, smtppass, emails,
                      from_email, smtpserver, smtpport, smtpssl, smtpauthentication, sitestarttime, site: str, systemname: str):
    """
    Function
    - Get and compare if processes are running on monitored machine

    param: sitename - name of the site
    param: env - enviroment

    param: logpath - path and filename of the log where will be result writen

    param: hostnanem - hostname  monitored machine (Windows)
    param: hwmiprocesses_file - files which prupose is to compare last check
    with current check to trigger or not trgigger email
    param: swmiprocessestmp_file - files which prupose is to compare last check
    with current check to trigger or not trgigger email
    param: swmiprocessestmp_file_nosuffix - files which prupose is to compare last check
    with current check to trigger or not trgigger email

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for SMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """
    wmi_connection_failed = f'Subject: {sitename} {env} WMI - Failed' + '\n' + \
        f'Hi, monitoring identified that WMI Conenction to {hostname} Failed'

    # Conenction to the WMI API on Windows Server
    print(f'Connecting to the WMI for host {hostname}')
    try:
        # Intitiate Emypt list
        list_of_processes = []
        list_of_processes_status = []
        process_failed_flag = False
        message = ''
        email_message = ''

        chwmi = wmi.WMI(hostname)

        # Add processt to the lit

        for process in chwmi.Win32_Process():
            list_of_processes.append(process.Name)
        # print(list_of_processes)

        # Remove duplicities from List
        list_of_processes = list(set(list_of_processes))

        # Check for defined (configured)  processes, if they exist in obtained process list
        for eachproces in wmiprocesses:
            if eachproces in list_of_processes:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|WINDOWS_PROCESS|OK|{eachproces} - OK\r\n'
                print(message)
                list_of_processes_status.append(f'{eachproces} - OK')
                cf.write_file_append(logpath, message)

            else:
                message = f'{sitestarttime}|WINDOWS_PROCESS|{site}|ERROR|{eachproces} - NOK\r\n'
                print(message)
                list_of_processes_status.append(f'{eachproces} - NOK')
                cf.write_file_append(logpath, message)
                # Semafor for identification, if some process failed
                process_failed_flag = True

        check_wmi_proccesses_file_exist(wmiprocesses_file)
        cf.write_file_list(wmiprocessestmp_file, list_of_processes_status)

        if process_failed_flag is False:
            if cf.compare_files(wmiprocesses_file, wmiprocessestmp_file):
                message = f'{sitestarttime}|{site}|{systemname}|{env}|WINDOWS_PROCESS|OK|All processes are running\r\n'
                print(message)
                cf.write_file_list(logpath, message)
                copyfile(wmiprocessestmp_file, wmiprocesses_file)
            else:
                copyfile(wmiprocessestmp_file, f'{wmiprocessestmp_file_nosuffix}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.txt')
                message = f'{sitestarttime}|{site}|{systemname}|{env}|WINDOWS_PROCESS|OK|All procsses are running\r\n'
                print(message)
                cf.write_file_append(logpath, message)
                copyfile(wmiprocessestmp_file, wmiprocesses_file)

                try:
                    # Email preparation
                    email_message_list_of_processes_status = ""
                    for item in list_of_processes_status:
                        email_message_list_of_processes_status += f'{str(item)}\n'
                    email_message = f'Subject: {sitename} {env} Monitored proces(es) OK' + '\n' + f'Hi, monitoring identified that on {hostname} all processes are ok\n{email_message_list_of_processes_status}'
                    cf.send_emails(smtpuseremail, smtppass, emails, from_email, email_message,
                                   smtpserver, smtpport, smtpssl, smtpauthentication)
                except Exception as exep_email:
                    message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                    print(message)
                    cf.write_file_append(logpath, f'{message}')

        if process_failed_flag is True:
            if cf.compare_files(wmiprocesses_file, wmiprocessestmp_file):
                message = f'{sitestarttime}|{site}|{systemname}|{env}|WINDOWS_PROCESS|ERROR|Monitored proces(es) failed\r\n'
                print(message)
                cf.write_file_list(logpath, message)
                copyfile(wmiprocessestmp_file, wmiprocesses_file)
            # if compare_files(wmiprocesses_file, wmiprocesses_file)
            # is False and process_failed_flag is True:
            else:
                copyfile(wmiprocessestmp_file, f'{wmiprocessestmp_file_nosuffix}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.txt')
                message = f'{sitestarttime}|{site}|{systemname}|{env}|WINDOWS_PROCESS|ERROR|Monitored proces(es) failed\r\n'
                print(message)
                cf.write_file_append(logpath, message)
                copyfile(wmiprocessestmp_file, wmiprocesses_file)

                try:
                    # Email preparation
                    email_message_list_of_processes_status = ""
                    for item in list_of_processes_status:
                        email_message_list_of_processes_status += f'\n{str(item)}'
                    email_message = f'Subject: {sitename} {env} Monitored proces(es) FAILED' + '\n' + f'Hi, monitoring identified that on {hostname} NOT all processes are OK\n{email_message_list_of_processes_status}'
                    cf.send_emails(smtpuseremail, smtppass, emails, from_email, email_message,
                                   smtpserver, smtpport, smtpssl, smtpauthentication)
                except Exception as exep_email:
                    message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                    print(message)
                    cf.write_file_append(logpath, f'{message}')

        # cf.remove(wmiprocessestmp_file)
        # print(list_of_processes_status)

    except Exception as wmi_e:
        message = f'{sitestarttime}|{site}|{systemname}|{env}|WINDOWS_PROCESS|Failed to conenct to WMI API: {wmi_e}\r\n'
        print(message)
        cf.write_file_append(logpath, f'{message}')
        try:
            cf.send_emails(smtpuseremail, smtppass, emails, from_email, wmi_connection_failed,
                           smtpserver, smtpport, smtpssl, smtpauthentication)
        except Exception as exep_email:
            message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
            print(message)
            cf.write_file_append(logpath, f'{message}')

    # finally:
    #     del chwmi
