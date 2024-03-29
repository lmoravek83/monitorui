"""
Module which is covering Webfunctions functions related MONITORUI
"""

from datetime import datetime
from os import path, remove
from shutil import copyfile
from requests import get
from colorama import Fore, Style, init
from modules.functions import common_func as cf
init()


def get_response_code(url: str, sslcertificatevalidation: bool, timeout_check: int) -> str:
    """
    param: url
    Return: obtained response code
    """
    try:
        return str(get(url, verify=sslcertificatevalidation, timeout=timeout_check).status_code)

    except Exception as excep:
        return f"Response Code failed on Exception: {excep}"


def check_response_code(sitename: str, env: str, responsecode_state_file: str, url: str, timeout_check,
                        defined_responsecode: str, sslcertificatevalidation: bool, logpath: str, smtpuseremail: str, smtppass: str,
                        emails: list, from_email: str, smtpserver: str, smtpport: int,
                        smtpssl: bool, smtpauthentication: bool, timeout_email, sitestarttime, site: str, systemname: str) -> bool:
    """
    Function check the respose code 'get_response_code' on the site and compared with given code,
    based on the evaluation is send email notification and logged

    param: sitename - name of the site
    param: env - enviroment

    param: responsecode_state_file - name of the file where is stored response code
    param: url - irl of the page where will be response code obtained
    param: expected - response code for which will be the result compared
    param: logpath - path and filename of the log whre will be result writen

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for SMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """
    # Check if last web service status file exist, if not create with defined code
    cf.check_state_file_exist(responsecode_state_file, defined_responsecode)

    # Receive response code from function
    obtained_responsecode = get_response_code(url, sslcertificatevalidation, timeout_check)

    msg_responsecode_failed = f'Subject: {sitename} {env} Response Code - NOK' + '\n' + \
        f'Hi,\nmonitoring identified that site {sitename} responsecode does not correspond to the definition.\n\n{url}\nExpected response code: {defined_responsecode}, obtained responsecode {obtained_responsecode}'
    msg_responsecode_ok = f'Subject: {sitename} {env} Response Code - OK' + '\n' + \
        f'Hi,\nmonitoring identified that site {sitename} responsecode correspond to the definition.\n\n{url}\nExpected response code: {defined_responsecode}, obtained responsecode {obtained_responsecode}'

    if obtained_responsecode != defined_responsecode:
        message = f'{sitestarttime}|{site}|{systemname}|{env}|HTTP_RESPONSE_CODE|ERROR|Status = Down|Response code: {obtained_responsecode}\r\n'
        print(Fore.YELLOW + message + Style.RESET_ALL)
        cf.write_file_append(logpath, message)
        # Check previos state of response code, to do not spam and send email
        if not cf.check_previous_state(obtained_responsecode, responsecode_state_file):
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                               msg_responsecode_failed, smtpserver, smtpport,
                               smtpssl, smtpauthentication, timeout_email)
            except Exception as exep_email:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message}')
            cf.write_current_state(obtained_responsecode, responsecode_state_file)
        return False
    else:
        message = f'{sitestarttime}|{site}|{systemname}|{env}|HTTP_RESPONSE_CODE|OK|Status = UP|Response code: {obtained_responsecode}\r\n'
        print(message)
        cf.write_file_append(logpath, message)
        # Check previos state of response code, to do not spam and send email
        if not cf.check_previous_state(obtained_responsecode, responsecode_state_file):
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                               msg_responsecode_ok, smtpserver, smtpport,
                               smtpssl, smtpauthentication, timeout_email)
            except Exception as exep_email:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message}')
            cf.write_current_state(obtained_responsecode, responsecode_state_file)
        return True


# Web page Footprint functions
def create_web_current_foot_print(url: str, webactualtmpfootprint_file: str,
                                  htmlignoreelements: list, sslcertificatevalidation: bool, timeout_check: int):
    """
    Function which dowload poage in to the txt file from given url.\
            Functiona can ignore some of the page elements.
    param: url - defined url of web page / page which will be downloaded
    param: webactualtmpfootprint_file - file name where wil be page stored
    param: htmlignoreelement - html element hwihc will be ignored during page safe
    param: sslcertificatevalidation - use / disable SSL certificate validation
    """
    content = []
    # Remove old Actual Foot print file - if exist
    cf.remove_file_func(webactualtmpfootprint_file)

    content = list(get(url, verify=sslcertificatevalidation, timeout=timeout_check).text.split('\n'))

    filestring = ''
    for element in content:
        for htmlignore in htmlignoreelements:
            if htmlignore in element and htmlignore != "":
                element = "\n"

        filestring = filestring + element

    cf.write_file(webactualtmpfootprint_file, filestring)


def check_web_saved_footprint_file_exist(websavedfootprint_file: str,
                                         webactualtmpfootprint_file: str):
    """
    Function check if Footprint for storing original web page, exists, if not create it.
    param: websavedfootprint_file - file where will be stored web page, if file do not exist(copy)
    param: webactualtmpfootprint_file - file from which will be created (copy)
    websavedfootprint_file
    """
    if not path.isfile(websavedfootprint_file):
        copyfile(webactualtmpfootprint_file, websavedfootprint_file)


def check_web_last_state_footprint_file_exist(websavedfootprint_file: str,
                                              weblaststatefootprint_file: str):
    """
    Function check if last saved Footprint file exists, if not create it.
    param: websavedfootprint_file - file where will be stored web page, during first run. (copy)
    param: ebactualtmpfootprint_file - file from which will be created (copy) websavedfootprint_file
    """
    if not path.isfile(weblaststatefootprint_file):
        copyfile(websavedfootprint_file, weblaststatefootprint_file)


def check_site_content(sitename: str, env: str, logpath: str, url: str, timeout_check,
                       sslcertificatevalidation: bool, htmlignoreelements: list,
                       webactualtmpfootprint_file: str, websavedfootprint_file: str,
                       weblaststatefootprint_file: str, weblaststatefootprint_file_nosuffix: str,
                       smtpuseremail: str, smtppass: str, emails: list, from_email: str,
                       smtpserver: str, smtpport: int, smtpssl: bool, smtpauthentication: bool, timeout_email, sitestarttime, site: str, systemname: str):
    """
    Function
    - Create new web footprint of given url
    - Check if exist last footprint and saved foot print, if not create ones
    - compares obtained footprint with last footprint and saved footprint,\
            if there is differenc notify on given email adress.

    param: sitename - name of the site
    param: env - enviroment

    param: logpath - path and filename of the log where will be result writen

    param: url - defined url of web page / page which will be downloaded / compared
    param: htmlignoreelements - ignore elements on the page
    param: sslcertificatevalidation - validate SSL certificate on page

    param: webactualtmpfootprint_file - file where is stoed tmeporrary current footprint of the page
    param: websavedfootprint_file - file where is stored original footprint of the page\
            - created during firt run
    param: weblaststatefootprint_file - file where is stored last foot print
    param: weblaststatefootprint_file_nosuffix - file where is recorded last foot print\
            if comparision failed

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for SMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """

    # Create Actul web foot print
    try:
        create_web_current_foot_print(url, webactualtmpfootprint_file, htmlignoreelements,
                                      sslcertificatevalidation, timeout_check)
    except Exception as excep:
        message = f'{sitestarttime}|{site}|{systemname}|{env}|create_web_current_foot_print Failed on Exception: {excep}\r\n'
        print(message)
        cf.write_file_append(logpath, f'{message}')
        cf.remove_file_func(webactualtmpfootprint_file)

    # If FootPrint file does not exist, create new foot print file
    check_web_saved_footprint_file_exist(websavedfootprint_file, webactualtmpfootprint_file)
    # If last state file does not exist, initializing lats state of webpage, from original footprint
    check_web_last_state_footprint_file_exist(websavedfootprint_file, weblaststatefootprint_file)

    msg_comparefailed = f'Subject: {sitename} {env} Page Changed' + '\n' + \
        f'Hi, monitoring identified that {sitename} has changed from footprint / last state \n {url}'
    msg_pageoriginal = f'Subject: {sitename} {env} Page Changed back to original' + '\n' + \
        f'Hi, monitoring identified that {sitename} has changed back to original \n {url}'

    # Logic to compare footprint of webpage with actual webpagefotpritn
    if cf.compare_files(websavedfootprint_file, webactualtmpfootprint_file):
        message = f'{sitestarttime}|{site}|{systemname}|{env}|WEB_CHANGE|OK|Page compare: OK\r\n'
        print(message)
        cf.write_file_append(logpath, message)
        # Snapshoting to the previous state
        # Send email, if only chanes from previos state, to do not spam
        if not cf.compare_files(weblaststatefootprint_file, webactualtmpfootprint_file):
            # make snapshot of changed page
            copyfile(webactualtmpfootprint_file, f'{weblaststatefootprint_file_nosuffix}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.txt')
            message = f'{sitestarttime}|{site}|{systemname}|{env}|WEB_CHANGE|OK|Page Change: Page changed to the original\r\n'
            print(message)
            cf.write_file_append(logpath, message)
            # remove last state footprint and make it from actual web state
            remove(weblaststatefootprint_file)
            copyfile(webactualtmpfootprint_file, weblaststatefootprint_file)
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email, msg_pageoriginal,
                               smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
            except Exception as exep_email:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message}')
        cf.remove_file_func(webactualtmpfootprint_file)
        return True

    else:
        message = f'{sitestarttime}|{site}|{systemname}|{env}|WEB_CHANGE|ERROR|Page compare: Failed\r\n'
        print(Fore.YELLOW + message + Style.RESET_ALL)
        cf.write_file_append(logpath, message)
        # Snapshoting to the previous state
        # Send email, if only chanes from previos state, to do not spam
        if not cf.compare_files(weblaststatefootprint_file, webactualtmpfootprint_file):
            # make snapshot of changed page
            copyfile(webactualtmpfootprint_file, f'{weblaststatefootprint_file_nosuffix}_{datetime.now().strftime("%d%m%Y_%H%M%S")}.txt')
            message = f'{sitestarttime}|{site}|{systemname}|{env}|WEB_CHANGE|WARNING|Page Change: Page changed to the last state\r\n'
            print(Fore.YELLOW + message + Style.RESET_ALL)
            cf.write_file_append(logpath, message)
            # remove last state footprint and make it from actual web state
            remove(weblaststatefootprint_file)
            copyfile(webactualtmpfootprint_file, weblaststatefootprint_file)
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email, msg_comparefailed,
                               smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
            except Exception as exep_email:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message}')

        cf.remove_file_func(webactualtmpfootprint_file)
        return False
