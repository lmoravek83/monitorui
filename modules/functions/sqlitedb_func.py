"""
SQLite functions for MonitorUI
"""
from colorama import Fore, Style, init
from modules.functions import common_func as cf
init()
try:
    import sqlite3
except Exception as e:
    message = f'ERROR: SQLITE DB driver load failed.. {e}'
    print(Fore.RED + message + Style.RESET_ALL)


def check_sqllite_script(sitename, env, logpath, hostname, sqlitdbepath, sqlitedbname,
                         sqlitesqlcommand, sqlliteevaluateoperator, sqliteexpectedvalue,
                         sqlitedb_state_file, smtpuseremail, smtppass, emails, from_email,
                         smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email, sitestarttime, site: str, systemname: str):
    """
    Function to execute SQL query and compare results agins expected values (int)

    param: sitename - name of the site
    param: env - enviroment
    param: hostnanem - hostname  monitored machine (Windows)
    param: logpath - path and filename of the log where will be result writen

    param: sqlitdbepath
    param: sqlitedbname


    param: oracledb_state_file - file to compare woth previous check to
    trigger or not trigger email notfication
    param: sqlitesqlcommand - sql command to be executed ont the db
    param: sqlliteevaluateoperator - oprator for evalueate <,>, !=, etc ..
    param: sqliteexpectedvalue - value gor which is compared result of sql scrit

    param: smtpuseremail - user email for SMTP autentification, email notification
    param: smtppass - password for SMTP autentification
    param: email - email list of recepitents
    param: from_email - sender email
    param: smtpserver - smtp server
    param: smtpport - smtp port
    param: smtpsll - use SSL for smtp connection
    param: smtpauthentication - use autentification for smtp connection
    """
    sql_connection_failed = f'Subject: {sitename} {env} ERROR: SQL - Failed - Connection' + '\n' + f'ERROR: - Hi, monitoring identified that SQL DB Conenction to {hostname} Failed'
    sql_connection_failed_cursor = f'Subject: {sitename} {env} ERROR: SQL - Failed - Create Coursor' + '\n' + f'ERROR: - Hi, monitoring identified that SQL DB Conenction to {hostname} Failed - create cursor'
    sql_connection_failed_sql_command = f'Subject: {sitename} {env} ERROR: SQL - Failed - Execute SQL' + '\n' + f'ERROR: - Hi, monitoring identified that SQL DB Conenction to {hostname} Failed - Execute SQL Command'
    sql_evaluation_failed = f'Subject: {sitename} {env} ERROR: SQL - Failed - SQL Evaluation' + '\n' + f'ERROR: - Hi, monitoring identified that SQL evaluation on {hostname} Failed'

    conn = None
    try:
        conn = sqlite3.connect(sqlitdbepath + sqlitedbname)
    except Exception as excep_conn_db:
        message_conn_db = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|Failed to connect SQLITE DB on Exception = {excep_conn_db}\r\n'
        print(Fore.RED + message_conn_db + Style.RESET_ALL)
        cf.write_file_append(logpath, f'{message_conn_db}')
        try:
            cf.send_emails(smtpuseremail, smtppass, emails, from_email, sql_connection_failed,
                           smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
        except Exception as excep_email:
            message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
            print(Fore.RED + message_email_error + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message_email_error}')

    conn_c = None
    if conn is not None:
        try:
            conn_c = conn.cursor()
        except sqlite3.Error as excep_create_cursor:
            message_create_cursor = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|Failed to connect SQLITE DB - Create Cursor on Exception = {excep_create_cursor}\r\n'
            print(Fore.RED + message_create_cursor + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message_create_cursor}')
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                               sql_connection_failed_cursor, smtpserver, smtpport,
                               smtpssl, smtpauthentication, timeout_email)
            except Exception as excep_email:
                message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
                print(Fore.RED + message_email_error + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_email_error}')

    sqlresult = None
    if conn_c is not None:
        try:
            conn_c.execute(str(sqlitesqlcommand))
            sqlresult = conn_c.fetchone()[0]

        except Exception as excep_sql_cmd:
            message_sql_cmd = f'{sitestarttime}|{site}|{systemname}|{env}(SQLITE_DB|ERROR|ERROR: Failed to connect SQLITE DB - Execute SQL Command: {excep_sql_cmd}\r\n'
            print(Fore.RED + message_sql_cmd + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message_sql_cmd}')
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                               sql_connection_failed_sql_command, smtpserver, smtpport,
                               smtpssl, smtpauthentication, timeout_email)
            except Exception as excep_email:
                message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
                print(Fore.RED + message_email_error + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_email_error}')

    sqlcomparision = None
    if sqlresult is not None:
        if sqliteexpectedvalue and sqlliteevaluateoperator is not None:
            try:
                # print(sqlliteevaluateoperator)
                if sqlliteevaluateoperator == '<':
                    if sqlresult < int(sqliteexpectedvalue):
                        sqlcomparision = 'OK'
                    else:
                        sqlcomparision = 'NOK'

                elif sqlliteevaluateoperator == '>':
                    if sqlresult > int(sqliteexpectedvalue):
                        sqlcomparision = 'OK'
                    else:
                        sqlcomparision = 'NOK'

                elif sqlliteevaluateoperator == '=':
                    if sqlresult == int(sqliteexpectedvalue):
                        sqlcomparision = 'OK'
                    else:
                        sqlcomparision = 'NOK'

                elif sqlliteevaluateoperator == '!=':
                    if sqlresult != int(sqliteexpectedvalue):
                        sqlcomparision = 'OK'
                    else:
                        sqlcomparision = 'NOK'

            except Exception as excep_sql_eval:
                message_sql_eval = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|Failed to evalute SQL Result: {excep_sql_eval}\r\n'
                print(Fore.RED + message_sql_eval + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_sql_eval}')
                try:
                    cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                                   sql_evaluation_failed, smtpserver, smtpport, smtpssl,
                                   smtpauthentication, timeout_email)
                except Exception as excep_email:
                    message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
                    print(Fore.RED + message_email_error + Style.RESET_ALL)
                    cf.write_file_append(logpath, f'{message_email_error}')
        else:
            message_compare_failed = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|Result comparision failed due missing expected values or operator in config file'
            print(Fore.YELLOW + message_compare_failed + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message_compare_failed}')
            email_message = f'Subject: {sitename} {env} ERROR: evaluation logic failed' + '\n' + f'Hi, monitoring identified that on {hostname} {message_compare_failed}'
            try:
                cf.send_emails(smtpuseremail, smtppass, emails, from_email, email_message,
                               smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
            except Exception as excep_email:
                message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
                print(Fore.RED + message_email_error + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_email_error}')
    else:
        message_comp_failed_no_res = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|SQL result comparision failed due to not obained SQL Result '
        print(Fore.YELLOW + message_comp_failed_no_res + Style.RESET_ALL)
        cf.write_file_append(logpath, f'{message_comp_failed_no_res}')
        email_message = f'Subject: {sitename} {env} SQL evaluation failed' + '\n' + f'Hi, monitoring identified that on {hostname} {message_comp_failed_no_res}'
        try:
            cf.send_emails(smtpuseremail, smtppass, emails, from_email, email_message,
                           smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
        except Exception as excep_email:
            message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
            print(Fore.RED + message_email_error + Style.RESET_ALL)
            cf.write_file_append(logpath, f'{message_email_error}')

    if sqlcomparision is not None:
        print(sqlcomparision)

    cf.check_state_file_exist(sqlitedb_state_file, 'OK')

    if sqlcomparision == 'OK':
        message_validation_ok = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|OK|Condition validation OK - SQL scripts results are in defined conditon: records {sqlresult}\r\n'
        print(message_validation_ok)
        cf.write_file_append(logpath, message_validation_ok)
        if not cf.check_previous_state(sqlcomparision, sqlitedb_state_file):
            try:
                sql_script_condition_ok = f'Subject: {sitename} {env} SQL - condition evaluation OK' + '\n' + f'Hi, monitoring identified that SQL condition evaluation on {hostname} is OK, results {sqlresult}- SQL scripts results are in defined conditon'
                cf.send_emails(smtpuseremail, smtppass, emails, from_email, sql_script_condition_ok,
                               smtpserver, smtpport, smtpssl, smtpauthentication, timeout_email)
            except Exception as excep_email:
                message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
                print(Fore.RED + message_email_error + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_email_error}')
            cf.write_current_state(sqlcomparision, sqlitedb_state_file)
        # cf.write_current_state(sqlcomparision, sqlitedb_state_file)
        return True
    else:
        message_cond_val_failed = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|SQLITE condition validation failed - SQL scripts results are out of defined conditon: records {sqlresult}\r\n'
        print(Fore.YELLOW + message_cond_val_failed + Style.RESET_ALL)
        cf.write_file_append(logpath, message_cond_val_failed)
        if not cf.check_previous_state(sqlcomparision, sqlitedb_state_file):
            try:
                sql_script_condition_failed = f'Subject: {sitename} {env} SQLLITE - condition evaluation failed' + '\n' + f'Hi, monitoring identified that SQL condition evaluation on {hostname} Failed, results {sqlresult} - SQL scripts results are out of defined conditon'
                cf.send_emails(smtpuseremail, smtppass, emails, from_email,
                               sql_script_condition_failed, smtpserver, smtpport,
                               smtpssl, smtpauthentication, timeout_email)
            except Exception as excep_email:
                message_email_error = f'{sitestarttime}|{site}|{systemname}|{env}|MAIL_NOTIFICATION|ERROR|Email notification failed on Exception = {excep_email}\r\n'
                print(Fore.RED + message_email_error + Style.RESET_ALL)
                cf.write_file_append(logpath, f'{message_email_error}')
            cf.write_current_state(sqlcomparision, sqlitedb_state_file)
        # cf.write_current_state(sqlcomparision, sqlitedb_state_file)
        return True

    try:
        conn.close()
    except Exception as excep_db_close_conn:
        message_close_conn_failed = f'{sitestarttime}|{site}|{systemname}|{env}|SQLITE_DB|ERROR|Failed to close connection: {excep_db_close_conn}\r\n'
        print(Fore.RED + message_close_conn_failed + Style.RESET_ALL)
        cf.write_file_append(logpath, f'{message_close_conn_failed}')
