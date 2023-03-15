"""
Network monitoring functions
"""
from subprocess import check_output
from os import system
from socket import socket, AF_INET, SOCK_STREAM
from sys import platform
from datetime import datetime, timedelta
import ssl
from colorama import Fore, Style, init
from modules.functions import common_func as cf
init()


def get_ping_status(hostname):
    """
    Function check if the hostname / ip is reachable
    param: hostname - hostname or ip for destinatiot
    """

    try:
        # print(platform.)
        if "win32" in platform.lower():
            if check_output(f'ping -n 1 {hostname}'):
                return '0'
            elif check_output(f'ping -n 3 {hostname}'):
                return '0'
            else:
                return 'Ping Failed'
        # elif "linux" in platform.lower():
        #     if check_output(f'ping -c 1 {hostname}'):
        #         return '0'
        #     else:
        #         return 'Ping Failed'
        # elif "freebsd" in platform.lower():
        #     if system(f'ping -c 1 {hostname} > /dev/null') == 0:
        #         return '0'
        #     else:
        #         return 'Ping Failed'
        else:
            if system(f'ping -c 1 {hostname} > /dev/null') == 0:
                return '0'
            elif system(f'ping -c 3 {hostname} > /dev/null') == 0:
                return '0'
            else:
                return 'Ping Failed'

    except Exception as exep:
        return f'Ping Failed on Exception: {exep}'


def check_ping(sitename: str, env: str, logpath: str, hostname: str, url: str,
               ping_state_file: str, smtpuseremail: str, smtppass: str, emails: list,
               from_email: str, smtpserver: str, smtpport: int, smtpssl: bool,
               smtpauthentication: bool, timeout_email, sitestarttime, site: str, systemname: str):
    """
    Function check the repose code 'get_response_code' on the site and compared\
            with given code, based on the evaluation is send email notification and logged

    param: sitename - name of the site
    param: env - enviroment

    param: url - url of the site
    param: hostname / ip - hostname which will be checked for ping
    param: logpath - path and filename of the log whre will be result writen
    param: ping_state_fil - name of the file where is stored response code

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for sMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """

    cf.check_state_file_exist(ping_state_file, '0')

    responsecode = get_ping_status(hostname)

    ping_msg_down = f'Subject: {sitename} {env} Ping - DOWN' + '\n' + f'Hi, monitoring identified that {hostname} / PING is DOWN \n{url}'
    ping_msg_up = f'Subject: {sitename} {env} Ping - UP' + '\n' + f'Hi, monitoring identified that {hostname} / PING is UP \n{url}'

    if responsecode != '0':
        message = f'{sitestarttime}|{site}|{systemname}|{env}|PING|ERROR|Response code = {responsecode}\r\n'
        print(Fore.YELLOW + message + Style.RESET_ALL)
        cf.write_file_append(logpath, message)
        # Check previos state of response code, to do not spam and send email / write same data in status file
        if not cf.check_previous_state(responsecode, ping_state_file):
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email, ping_msg_down,
                               smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
            except Exception as exep_email:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message}')
            cf.write_current_state(responsecode, ping_state_file)
        # cf.write_current_state(responsecode, ping_state_file)
        # return False

    else:
        message = f'{sitestarttime}|{site}|{systemname}|{env}|PING|OK|Response code = {responsecode}\r\n'
        print(message)
        cf.write_file_append(logpath, message)
        # Check previos state of response code, to do not spam and send email / write same data in status file
        if not cf.check_previous_state(responsecode, ping_state_file):
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email, ping_msg_up,
                               smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
            except Exception as exep_email:
                message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message}')
            cf.write_current_state(responsecode, ping_state_file)
        # cf.write_current_state(responsecode, ping_state_file)
        # return True


def get_port_status(hostname, port, timeout_check):
    """
    Function get port status
    param: hostname
    param: port
    """
    resp = ''
    try:
        a_socket = socket(AF_INET, SOCK_STREAM)
        a_socket.settimeout(timeout_check)
        resp = str(a_socket.connect_ex((hostname, int(port))))
        a_socket.close()
        return resp
    except Exception as exep:
        return f'Port Connection failed one Exception: {exep}'


def check_port(sitename: str, env: str, logpath: str, hostname: str, url: str, timeout_check,
               port_state_file_nosuffix: str, hostports: list, smtpuseremail: str, smtppass: str,
               emails: list, from_email: str, smtpserver: str, smtpport: int, smtpssl: bool,
               smtpauthentication: bool, timeout_email, sitestarttime, site: str, systemname: str):
    """
    Function check the repose code 'get_response_code' on the site and compared with given code,\
            based on the evaluation is send email notification and logged

    param: sitename - name of the site
    param: env - enviroment
    param: logpath - path and filename of the log whre will be result writen
    param: hostname / ip - hostname which will be checked for ping
    param: url - url of the site

    param: hostports - ports ID which need to be checked
    param: port_state_file_nosuffix - name of the file where is stored response code

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for sMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """
    for port in hostports:
        # Check if last web service status file exist
        port_state_file = port_state_file_nosuffix + port + ".txt"
        cf.check_state_file_exist(port_state_file, '0')
        # Receive response code from function
        responsecode = get_port_status(hostname, port, timeout_check)

        port_msg_down = f'Subject: {sitename} {env} Port - DOWN' + '\n' + f'Hi, monitoring identified that {hostname} Port {port} is DOWN \n{url}'
        port_msg_up = f'Subject: {sitename} {env} Port - UP' + '\n' + f'Hi, monitoring identified that {hostname} Port {port} is UP \n{url}'

        if responsecode != '0':
            message = f'{sitestarttime}|{site}|{systemname}|{env}|PORT|ERROR|Port={port}|Response code = {responsecode}\r\n'
            print(Fore.YELLOW + message + Style.RESET_ALL)
            cf.write_file_append(logpath, message)
            # Check previos state of response code, to do not spam and send email / write same data in status file
            if not cf.check_previous_state(responsecode, port_state_file):
                try:
                    cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                                   port_msg_down, smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
                except Exception as exep_email:
                    message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                    print(Fore.RED + message + Style.RESET_ALL)
                    cf.write_file_append(logpath, f'{message}')
                cf.write_current_state(responsecode, port_state_file)
            # cf.write_current_state(responsecode, port_state_file)
            # If discomment, whole loop will not continue to next item - port
            # return False
        else:
            message = f'{sitestarttime}|{site}|{systemname}|{env}|PORT|OK|Port = {port}|Response code = {responsecode}\r\n'
            print(message)
            cf.write_file_append(logpath, message)
            # Check previos state of response code, to do not spam and send email / write same data in status file
            if not cf.check_previous_state(responsecode, port_state_file):
                try:
                    cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                                   port_msg_up, smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
                except Exception as exep_email:
                    message = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                    print(Fore.RED + message + Style.RESET_ALL)
                    cf.write_file_append(logpath, f'{message}')
                cf.write_current_state(responsecode, port_state_file)
            # cf.write_current_state(responsecode, port_state_file)
            # If discomment, whole loop will not continue to next item - port
            # return True


def ssl_expiry_datetime(host, port, timeout_check):
    """
    get expiration date on SSL certificate from hostname
    pram: host
    param: port
    """
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket(AF_INET),
        server_hostname=host,
    )
    # 3 second timeout because Lambda has runtime limitations
    # try:
    conn.settimeout(timeout_check)
    conn.connect((host, port))
    ssl_info = conn.getpeercert()
    return datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    # except Exception as exep:
    #     return exep


def certificate_expiration_check(sitename: str, env: str, logpath: str, hostname: str, url: str, timeout_check,
                                 certificate_expiration_check_file: str, certificateport: int,
                                 certificateexpirationtrigger1: int,
                                 certificateexpirationtrigger2: int,
                                 certificateexpirationtrigger3: int,
                                 certificateexpirationtrigger4: int,
                                 smtpuseremail: str, smtppass: str, emails: list, from_email: str,
                                 smtpserver: str, smtpport: int, smtpssl: bool,
                                 smtpauthentication: bool, timeout_email, sitestarttime, site: str, systemname: str):
    """
    Function to check if certificate expires

    param: sitename - name of the site
    param: env - enviroment
    param: logpath - path and filename of the log whre will be result writen
    param: hostname / ip - hostname which will be checked for ping
    param: url - url of the site

    param: certificate_expiration_check_file - name of the file where is stored
    information on date check
    param: certificateexpirationtrigger - how mnay days before the expiration,
    email notification will be triggered

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for sMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """

    # Check if last certificate status file exist
    cf.check_state_file_exist(certificate_expiration_check_file, '0')
    if cf.read_file(certificate_expiration_check_file)[0] != datetime.now().strftime("%d%m%Y"):

        try:
            # Get expiration time on hostname certificate
            cert_exp_date = ssl_expiry_datetime(hostname, certificateport, timeout_check)
            if (((datetime.now() + timedelta(days=certificateexpirationtrigger1 - 1)).date() ==
                cert_exp_date.date()) or
                ((datetime.now() + timedelta(days=certificateexpirationtrigger2 - 1)).date() ==
                cert_exp_date.date()) or
                ((datetime.now() + timedelta(days=certificateexpirationtrigger3 - 1)).date() ==
                cert_exp_date.date()) or
                ((datetime.now() + timedelta(days=certificateexpirationtrigger4 - 1)).date() ==
                    cert_exp_date.date())):

                message_cert_exp = f'{sitestarttime}|{site}|{systemname}|{env}|SSL_CERTIFICATE_EXPIRATION|WARNING|Certificate for {hostname} will expire on {cert_exp_date.strftime("%d.%m.%Y %H:%M:%S")}\r\n'
                print(Fore.YELLOW + message_cert_exp + Style.RESET_ALL)
                cf.write_file_append(logpath, message_cert_exp)

                cf.write_file(certificate_expiration_check_file,
                              datetime.now().strftime("%d%m%Y"))
                # Set email message
                cert_msg_exp = f'Subject: {sitename} {env} Certificate Expire on {cert_exp_date.strftime("%d.%m.%Y %H:%M:%S")}' + '\n' + f'Hi, monitoring identified that for {hostname} expire on {cert_exp_date.strftime("%d.%m.%Y %H:%M:%S")} \n{url}'

                try:
                    cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                                   cert_msg_exp, smtpserver, smtpport, smtpssl,
                                   smtpauthentication, timeout_email)
                except Exception as exep_email:
                    message_email_error =\
                        f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                    print(Fore.RED + message_email_error + Style.RESET_ALL)
                    cf.write_file_append(logpath, f'{message_email_error}')
                    cf.remove_file_func(certificate_expiration_check_file)

            else:
                if (datetime.now() + timedelta(days=certificateexpirationtrigger1 - 1)).date() > cert_exp_date.date():
                    message_cert_exp = f'{sitestarttime}|{site}|{systemname}|{env}|SSL_CERTIFICATE_EXPIRATION|WARNING|Certificate for {hostname} will expire on {cert_exp_date.strftime("%d.%m.%Y %H:%M:%S")}\r\n'
                    print(Fore.YELLOW + message_cert_exp + Style.RESET_ALL)
                    cf.write_file_append(logpath, message_cert_exp)
                    cf.write_file(certificate_expiration_check_file, datetime.now().strftime("%d%m%Y"))

                else:
                    message_cert_no_exp = f'{sitestarttime}|{site}|{systemname}|{env}|SSL_CERTIFICATE_EXPIRATION|INFO|Certificate for {hostname} will expire on {cert_exp_date.strftime("%d.%m.%Y %H:%M:%S")}\r\n'
                    print(message_cert_no_exp)
                    cf.write_file_append(logpath, message_cert_no_exp)
                    cf.write_file(certificate_expiration_check_file, datetime.now().strftime("%d%m%Y"))

        except Exception as exep:
            exep_crt = f'{sitestarttime}|{site}|{systemname}|{env}|SSL_CERTIFICATE_EXPIRATION|ERROR|failed to obtain SSL certificate expiration info on {hostname} with Error = {exep}\r\n'
            print(Fore.RED + exep_crt + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{exep_crt}')
            cf.write_file(certificate_expiration_check_file,
                          datetime.now().strftime("%d%m%Y"))

            cert_msg_exp = f'Subject: Failed to obtain SSL certificate expiration info on {hostname}' + '\n' +\
                f'Hi, monitoring identified that was not able to obtain certificate expiration info for {hostname} with Error = {exep}'
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                               cert_msg_exp, smtpserver, smtpport, smtpssl,
                               smtpauthentication, timeout_email)
            except Exception as exep_email:
                message_email_error =\
                    f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {exep_email}\r\n'
                print(Fore.RED + message_email_error + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_email_error}')
