"""
Monitored site class which provides all possbile fnctions / type of check
"""

from datetime import datetime
from os import path, remove, mkdir
from pathlib import Path
from time import time
from shutil import copyfile
from colorama import Fore, Style, init
from modules.functions.web_func import check_response_code, check_site_content
from modules.functions.network_func import check_ping, check_port, certificate_expiration_check
from modules.functions.wmi_func import check_wmi_process
from modules.functions.sqlitedb_func import check_sqllite_script
from modules.functions.oracledb_func import check_sql_oracle_script
from modules.functions import common_func as cf
init()


class MonitoredSite():
    """
    Monitored site class which provides all possbile fnctions / type of check
    """
    def __init__(self, config, siteconfig, site, sitefolder, logdailyfeedfolder):
        # Monitoring Config configuration
        self.sitestarttime = datetime.now()
        self.sitefolder = sitefolder
        self.site = site
        self.logdailyfeedfolder = logdailyfeedfolder

        if 'smtpuser' in config:
            self.smtpuseremail = config['smtpuser']
        else:
            self.smtpuseremail = ''

        if 'from_email' in config:
            self.from_email = config['from_email']
        else:
            self.from_email = ''

        if 'smtpserver' in config:
            self.smtpserver = config['smtpserver']
        else:
            self.smtpserver = 'localhost'

        if 'smtpport' in config:
            self.smtpport = config['smtpport']
        else:
            self.smtpport = 25

        if 'smtpssl' in config:
            self.smtpssl = config['smtpssl']
        else:
            self.smtpssl = False

        if 'smtpauthentication' in config:
            self.smtpauthentication = config['smtpauthentication']
        else:
            self.smtpauthentication = False

        if 'smtppass' in config:
            self.smtppass = config['smtppass']
        else:
            self.smtppass = ''

        if 'log_daily_feed' in config:
            self.logdailyfeed = config['log_daily_feed']
        else:
            self.logdailyfeed = False

        if 'logsretention' in config:
            self.logsretention = config['logsretention']
        else:
            self.logsretention = None

        # Write monitoring Time stame un to the Site Log
        if not path.exists(self.sitefolder + '//logs'):
            mkdir(self.sitefolder + '//logs')
        self.logpath =\
            f'{self.sitefolder}//logs//{self.site}_{datetime.now().strftime("%d%m%Y")}.log'
        # message = f'-Site "{self.site}" monitoring at: {sitestarttime}-\r\n'
        # print(message)
        # cf.write_file_append(self.logpath, message)

        # Configuration for site
        # Site and Enviroment Identification
        if 'siteenviroment' in siteconfig:
            self.env = siteconfig['siteenviroment']
        else:
            self.env = 'ENV_TBD'

        if 'sitename' in siteconfig:
            self.sitename = siteconfig['sitename']
        else:
            self.sitename = "SiteName_TBD"

        if 'systemname' in siteconfig:
            self.systemname = siteconfig['systemname']
        else:
            self.systemname = "SystemName_TBD"

        if 'hostname' in siteconfig:
            self.hostname = siteconfig['hostname']
        else:
            self.hostname = 'localhost'

        # Netwrok func
        if 'hostports' in siteconfig:
            self.hostports = siteconfig['hostports']
        else:
            self.hostports = ['']

        if 'certificateexpirationtrigger1' in siteconfig:
            self.certificateexpirationtrigger1 = siteconfig['certificateexpirationtrigger1']
        else:
            self.certificateexpirationtrigger1 = 30

        if 'certificateexpirationtrigger2' in siteconfig:
            self.certificateexpirationtrigger2 = siteconfig['certificateexpirationtrigger2']
        else:
            self.certificateexpirationtrigger2 = 20

        if 'certificateexpirationtrigger3' in siteconfig:
            self.certificateexpirationtrigger3 = siteconfig['certificateexpirationtrigger3']
        else:
            self.certificateexpirationtrigger3 = 10

        if 'certificateexpirationtrigger4' in siteconfig:
            self.certificateexpirationtrigger4 = siteconfig['certificateexpirationtrigger4']
        else:
            self.certificateexpirationtrigger4 = 5

        if "certificateport" in siteconfig:
            self.certificateport = siteconfig['certificateport']
        else:
            self.certificateport = 443

        # WMI processes
        if 'wmiprocesses' in siteconfig:
            self.wmiprocesses = siteconfig['wmiprocesses']
            # self.wmiprocesses.sort()
        else:
            self.wmiprocesses = ''

        # Monitoring URL and Response Code, HTML Ignore Elements
        if 'siteresponsecode' in siteconfig:
            self.siteresponsecode = siteconfig['siteresponsecode']
        else:
            self.siteresponsecode = '200'

        if 'siteurl' in siteconfig:
            self.url = siteconfig['siteurl']
        else:
            self.url = 'localhost'

        if 'htmlignoreelements' in siteconfig:
            self.htmlignoreelements = siteconfig['htmlignoreelements']
        else:
            self.htmlignoreelements = ['']

        if 'sslcertificatevalidation' in siteconfig:
            self.sslcertificatevalidation = siteconfig['sslcertificatevalidation']
        else:
            self.sslcertificatevalidation = True

        # ORACLE DB monitoring Configuration
        if "oracleuser" in siteconfig:
            self.oracleuser = siteconfig['oracleuser']
        else:
            self.oracleuser = ''

        if "oraclepassword" in siteconfig:
            self.oraclepassword = siteconfig['oraclepassword']
        else:
            self.oraclepassword = ''

        if "oracledsn" in siteconfig:
            self.oracledsn = siteconfig['oracledsn']
        else:
            self.oracledsn = ''

        if "oracleevaluateoperator" in siteconfig:
            self.oracleevaluateoperator = siteconfig['oracleevaluateoperator']
        else:
            self.oracleevaluateoperator = None

        if "oraclesqlcommand" in siteconfig:
            self.oraclesqlcommand = siteconfig['oraclesqlcommand']
        else:
            self.oraclesqlcommand = ''

        if "oracleexpectedvalue" in siteconfig:
            self.oracleexpectedvalue = siteconfig['oracleexpectedvalue']
        else:
            self.oracleexpectedvalue = None

        # SQLITE DB monitoring Configuration
        if "sqlitdbepath" in siteconfig:
            self.sqlitdbepath = siteconfig['sqlitdbepath']
        else:
            self.sqlitdbepath = ''

        if "sqlitedbname" in siteconfig:
            self.sqlitedbname = siteconfig['sqlitedbname']
        else:
            self.sqlitedbname = ''

        if "sqlliteevaluateoperator" in siteconfig:
            self.sqlliteevaluateoperator = siteconfig['sqlliteevaluateoperator']
        else:
            self.sqlliteevaluateoperator = None

        if "sqlitesqlcommand" in siteconfig:
            self.sqlitesqlcommand = siteconfig['sqlitesqlcommand']
        else:
            self.sqlitesqlcommand = ''

        if "sqliteexpectedvalue" in siteconfig:
            self.sqliteexpectedvalue = siteconfig['sqliteexpectedvalue']
        else:
            self.sqliteexpectedvalue = None

        # Files configuration
        self.responsecode_state_file = f'{self.sitefolder}//responsecode_state.txt'
        self.ping_state_file = f'{self.sitefolder}//ping_state.txt'
        # self.port_state_file = f'{self.sitefolder}//port_state.txt'
        self.port_state_file_nosuffix = f'{self.sitefolder}//port_state_'
        self.sqlitedb_state_file = f'{self.sitefolder}//sqlitedb_state.txt'
        self.oracledb_state_file = f'{self.sitefolder}//oracledb_state.txt'
        self.webactualtmpfootprint_file\
            = f'{self.sitefolder}//webactualtmpfootprint.txt'
        self.websavedfootprint_file = f'{self.sitefolder}//websavedfootprint.txt'
        self.weblaststatefootprint_file_nosuffix\
            = f'{self.sitefolder}//weblaststatefootprint'
        self.weblaststatefootprint_file = f'{self.weblaststatefootprint_file_nosuffix}.txt'
        self.wmiprocesses_file = f'{self.sitefolder}//wmiprocesses.txt'
        self.wmiprocessestmp_file = f'{self.sitefolder}//wmiprocessestmp.txt'
        self.wmiprocessestmp_file_nosuffix = f'{self.sitefolder}//wmiprocesses'
        self.certificate_expiration_check_file\
            = f'{self.sitefolder}//certificate_exp_last_check.txt'

        if 'emailrecipients' in siteconfig:
            self.emails = siteconfig['emailrecipients']
        else:
            self.emails = ['']

    def site_check_response_code(self):
        """
        Response code check on website
        """
        check_response_code(self.sitename, self.env, self.responsecode_state_file,
                            self.url, self.siteresponsecode, self.sslcertificatevalidation, self.logpath, self.smtpuseremail,
                            self.smtppass, self.emails, self.from_email, self.smtpserver,
                            self.smtpport, self.smtpssl, self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def site_check_site_content(self):
        """
        Check if website is not changed agoinst first run
        """
        check_site_content(self.sitename, self.env, self.logpath, self.url,
                           self.sslcertificatevalidation, self.htmlignoreelements,
                           self.webactualtmpfootprint_file, self.websavedfootprint_file,
                           self.weblaststatefootprint_file,
                           self.weblaststatefootprint_file_nosuffix, self.smtpuseremail,
                           self.smtppass, self.emails, self.from_email, self.smtpserver,
                           self.smtpport, self.smtpssl, self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def site_check_ping(self):
        """
        Check if is possible to Ping the host
        """
        check_ping(self.sitename, self.env, self.logpath, self.hostname, self.url,
                   self.ping_state_file, self.smtpuseremail, self.smtppass, self.emails,
                   self.from_email, self.smtpserver, self.smtpport, self.smtpssl,
                   self.smtpauthentication, self.sitestarttime, self.site, self.sitename)

    def site_check_port(self):
        """
        Check if is Port is enabled on the host
        """
        check_port(self.sitename, self.env, self.logpath, self.hostname, self.url,
                   self.port_state_file_nosuffix, self.hostports, self.smtpuseremail,
                   self.smtppass, self.emails, self.from_email, self.smtpserver,
                   self.smtpport, self.smtpssl, self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def site_certificate_expiration_check(self):
        """
        check if ssl certificate expire
        """
        certificate_expiration_check(self.sitename, self.env, self.logpath, self.hostname,
                                     self.url, self.certificate_expiration_check_file,
                                     self.certificateport,
                                     self.certificateexpirationtrigger1,
                                     self.certificateexpirationtrigger2,
                                     self.certificateexpirationtrigger3,
                                     self.certificateexpirationtrigger4, self.smtpuseremail,
                                     self.smtppass, self.emails, self.from_email,
                                     self.smtpserver, self.smtpport, self.smtpssl,
                                     self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def site_check_wmni_process(self):
        """
        Check if defined proccesse runs on host
        """
        check_wmi_process(self.sitename, self.env, self.logpath, self.hostname,
                          self.wmiprocesses_file, self.wmiprocessestmp_file,
                          self.wmiprocessestmp_file_nosuffix, self.wmiprocesses,
                          self.smtpuseremail, self.smtppass, self.emails, self.from_email,
                          self.smtpserver, self.smtpport, self.smtpssl, self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def site_check_sqlite_script(self):
        """
        Connect on SQL DB, excetue SQL sritp and compare agoind Int value
        """
        check_sqllite_script(self.sitename, self.env, self.logpath, self.hostname,
                             self.sqlitdbepath, self.sqlitedbname, self.sqlitesqlcommand,
                             self.sqlliteevaluateoperator, self.sqliteexpectedvalue,
                             self.sqlitedb_state_file, self.smtpuseremail, self.smtppass,
                             self.emails, self.from_email, self.smtpserver, self.smtpport,
                             self.smtpssl, self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def site_check_oracle_script(self):
        """
        Connect on Oracle DB, excetue SQL sritp and compare agoind Int value
        """
        check_sql_oracle_script(self.sitename, self.env, self.hostname, self.logpath,
                                self.oracleuser, self.oraclepassword, self.oracledsn,
                                self.oracledb_state_file, self.oraclesqlcommand,
                                self.oracleevaluateoperator,
                                self.oracleexpectedvalue, self.smtpuseremail, self.smtppass,
                                self.emails, self.from_email, self.smtpserver, self.smtpport,
                                self.smtpssl, self.smtpauthentication, self.sitestarttime, self.site, self.systemname)

    def copy_log_for_agregation(self):
        """
        copy the log 
        """
        copyfile(self.logpath, self.logdailyfeedfolder + '//' + f'{self.site}.log')

    def removesite_logs(self):
        """
        Remove site logs - data retention
        """
        if self.logsretention is not None:
            try:
                logssitepath = f'{self.sitefolder}//logs//'

                for item in Path(logssitepath).glob('*.log'):
                    if item.is_file():
                        try:
                            if (Path.stat(item).st_mtime) < time() - self.logsretention * 86400:
                                remove(item)
                        except Exception as exep:
                            message = f'|ERROR|Failed to remove log file: {exep}\r\n'
                            print(Fore.RED + message + Style.RESET_ALL)
                            cf.write_file_append(self.logpath, f'{message}')
            except Exception as exep:
                message = f'|ERROR|Failed to oparate with log folder during celaning log files: {exep}\r\n'
                print(Fore.RED + message + Style.RESET_ALL)
                cf.write_file_append(self.logpath, f'{message}')
