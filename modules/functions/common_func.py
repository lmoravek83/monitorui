"""
Commmon function used in MonitorUI
"""

from smtplib import SMTP
from json import load
from os import path, listdir, remove
from filecmp import cmp, clear_cache
from pathlib import Path
from colorama import Fore, Style, init
init()


def check_wmi_proccesses_file_exist(wmi_proc_state_file) -> None:
    """
    If file for WMI processes list does not exist, create one
    param: wmi_proc_state_file - file name of the WMI proccess files
    """
    if not path.isfile(wmi_proc_state_file):
        write_file(wmi_proc_state_file, "")


# Logic related to read config files and define paths
def read_json(filename):
    """
    Read JSON File
    param: filename - filename of JSON file to be read
    """
    file = open(filename, "r", encoding='utf-8')
    content = load(file)
    file.close()
    return content


def read_file(filename):
    """
    Read file
    param: filename - filename of file to be read
    """
    file = open(filename, 'r', encoding='utf-8')
    content = (file.readlines())
    file.close()
    return content


def write_file(filename, content):
    """
    Write file
    param: filename - filename of file to be writeten
    param: content
    """
    file = open(filename, 'w', encoding='utf-8')
    file.write(content)
    file.close()


def write_file_append(filename, content):
    """
    Append file
    param: filename - filename of file to be append
    param: content
    """
    file = open(filename, 'a', encoding='utf-8')
    file.write(content)
    file.close()


def write_file_list(filename, content):
    """
    Write list in the file
    param: filename - filename of file to be append
    param: content - elelements / list
    """
    file = open(filename, 'w', encoding='utf-8')
    for element in content:
        file.write(element + '\r\n')
    file.close()


def list_directories(directory):
    """
    Retrun list of directories in given path - dir
    param: filename - filename of file to be append
    param: content - elelements / list
    """
    listsofdirs = []
    for item in listdir(directory):
        if path.isdir(directory + item):
            listsofdirs.append(item)
    return listsofdirs


def remove_file_func(file):
    """
    Remove file if exists
    param: filename - filename of file to be removed
    """
    if path.isfile(file):
        remove(file)


def send_emails(smtpuseremail, password, email_list, from_adress, msg, smtpserver, smtpport,
                smtpssl, smtpauthencitation):
    """
    param: smtpuseremail - user email for SMTP autentification, email notification
    param: password - password for SMTP autentification
    param: email_list - email list of recepitents
    param: from_adress - sender email
    param: msg - email meesage
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection   try:
    """
    print(Fore.CYAN + f'Sending email to {email_list}\r\n' + Style.RESET_ALL)
    smtp_object = SMTP(smtpserver, port=smtpport, timeout=10)
    smtp_object.ehlo()
    if smtpssl:
        smtp_object.starttls()
    if smtpauthencitation:
        smtp_object.login(smtpuseremail, password)
    for to_adress in email_list:
        smtp_object.sendmail(from_adress, to_adress, msg)
    smtp_object.quit()
    del smtp_object


def compare_files(file1, file2):
    """
    Compare of two files
    :param: file1 - fisrt file
    :param: file2 - second file
    """
    ret = cmp(file1, file2)
    clear_cache()
    return ret


def check_state_file_exist(mon_state_file, responsecode) -> None:
    """
    If State file do not exist, crate one with defined response code
    :param: state file txt
    :param: Expected response code (response code, ping, port, sql output)
    """
    if not path.isfile(mon_state_file):
        write_file(mon_state_file, responsecode)


def write_current_state(responsecode, mon_state_file):
    """
    Write given state in to the file
    param: responsecode - response code friten in file
    param: fmon_state_file - ile with content
    """
    write_file(mon_state_file, responsecode)


def check_previous_state(response, mon_state_file) -> bool:
    """
    Open file and check if the contant is same as given value
    param: response
    param: file with content
    """
    content = Path(mon_state_file).read_text(encoding='utf-8')
    if response == content:
        return True
    else:
        return False
