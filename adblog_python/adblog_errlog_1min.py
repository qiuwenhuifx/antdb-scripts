#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
import sys
import re
import os
import time
import datetime
import psycopg2
from psycopg2.extensions import AsIs

csv.field_size_limit(sys.maxsize)
# pg_log csv log fields
readlogfields = ['log_time', 'user_name', 'database_name', 'process_id', 'connection_from', 'session_id', 'session_line_num', 'command_tag', 'session_start_time', 'virtual_transaction_id', 'transaction_id', 'error_severity', 'sql_state_code', 'message', 'detail', 'hint', 'internal_query', 'internal_query_pos', 'context', 'query', 'query_pos', 'location', 'application_name']
writelogfields = ['nodename', 'log_time', 'user_name', 'database_name', 'connection_from', 'session_id', 'command_tag', 'error_severity', 'message', 'detail','query']

# command_tag from CreateCommandTag()@src/backend/tcop/utility.c  
cmd_list = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'EXECUTE', 'EXECUTE DIRECT', 'CREATE TABLE', 'TRUNCATE TABLE', 'COPY', 'CREATE INDEX', 'CREATE TABLE AS', 'BARRIER', 'REINDEX']

# write file delimiter
out_delimiter = "^"

nodename = ''
logdir = ''
begintime = ''
endtime = ''
outcsvfilename = ''

# error_severity from src/backend/utils/error/elog.c
log_level=['WARNING', 'ERROR', 'FATAL', 'PANIC'] 

# adb connection info
adb_conn="dbname=shhis user=adbadmin password=123 host=localhost port=5432"
target_table='adblog_errlog_'+datetime.datetime.now().strftime('%Y%m%d')

def get_sqlinfo(filename):
    """
    get logtime/username/dbname/sqltext/parameter/duration from pglog
    """
    with open(filename) as readlogfile:
        csvfile = csv.DictReader(readlogfile, fieldnames=readlogfields)
        tables = []
        try:
            for row in csvfile:
                logtimestr = datetime.datetime.strftime(datetime.datetime.strptime(row['log_time'][:19], '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d_%H%M%S')
                if logtimestr <= begintime:
                    continue
                if logtimestr > endtime:
                    break 
                if (row['error_severity'] in log_level):
                    logtime = row['log_time']
                    username = row['user_name']
                    dbname = row['database_name']
                    connection_from  = row['connection_from']
                    command_tag  = row['command_tag']
                    session_id = row['session_id']
                    message = row['message']
                    error_severity = row['error_severity']
                    detail = row['detail']
                    query = row['query']
                    outline = {'nodename':nodename, 'log_time':logtime, 'user_name':username, 'database_name': dbname, 'connection_from':connection_from, 'session_id':session_id,'command_tag':command_tag, 'message':message, 'detail':detail, 'query':query,'error_severity':error_severity}
                    tables.append(outline)
                else:
                    #next(csvfile)
                    #csvfile.next() 
                    continue
        except StopIteration:
            print "StopIteration"
        finally:
            # start to write rows  to csv file
            print datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')+" start to write rows  to csv file: "+outcsvfilename
            with open(outcsvfilename,'a+') as outfile:
               outfile_csv = csv.DictWriter(outfile, fieldnames=writelogfields,delimiter=out_delimiter)
               outfile_csv.writerows(tables)       


def end_process():
    #helpinfo = ' end process. now  copy data to adb '
    
    try:
       conn = psycopg2.connect(adb_conn)
    except psycopg2.Error as e:
        print"Unable to connect!"
        print e.pgerror
        print e.diag.message_detail
        sys.exit(1)   
        
    #该程序创建一个光标将用于整个数据库使用Python编程。
    try:
        print datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')+' start to copy csv file to adb'
        cur = conn.cursor()
        cur.execute("copy %s from %s delimiter %s csv;",(AsIs(target_table),outcsvfilename,out_delimiter))
        #copy_line = 'then execute "copy adblog_sqlinfo from \''+outcsvfilename+'\'  delimiter \''+out_delimiter+'\' csv;" to load csv data '

    except psycopg2.Error as e:
        print"copy execute error:"
        print e.pgerror
        print e.diag.message_detail
        sys.exit(1)
    else:
        lines = len(open(outcsvfilename).readlines())
        print datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')+' end copy csv file to adb ,file lines is:'+str(lines)
        os.remove(outcsvfilename)
    conn.commit()
    conn.close() 

def validateTimeFormat(input):
    try:
        datetime.datetime.strptime(input, '%Y-%m-%d_%H%M%S')
        return True
    except ValueError:
        return False

def get_logrange_input():
    while 1:
       global nodename
       nodename = raw_input("please input nodename: ").strip()
       print 'nodename is: '+nodename
       if nodename:
           break
       else:
           print 'nodename must should be valid'

    while 1:
       global logdir
       logdir = raw_input("please input logdir: ").strip()
       print 'logdir is: '+logdir

       if os.path.exists(logdir):
           break
       else:
           print 'input log dir does not exists!'

    while 1:
        sysbegintime = datetime.date.today().strftime("%Y-%m-%d_%H%M%S")
        inputbegintime = raw_input("please input begin time:(default "+sysbegintime+") ").strip()
        global begintime
        begintime = inputbegintime if inputbegintime else sysbegintime
        if validateTimeFormat(begintime):
            if begintime > datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"):  
                print "begintime should be less than now():"+datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            else:    
                print  'begintime is: '+begintime
                break
        else:
           print begintime+' time format is not correct, should be like %Y-%m-%d_%H%M%S (2017-12-31_080000)'

    while 1:
        sysendtime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        inputendtime = raw_input("please input end time:(default "+sysendtime+") ").strip()
        global endtime
        endtime = inputendtime if inputendtime else sysendtime
        if validateTimeFormat(endtime):
            if endtime > datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"):
                print "endtime should be less than now():"+datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
            elif endtime <= begintime:
                print "endtime should be greater than begintime:"+begintime
            else:
                print  'endtime is: '+endtime
                break
        else:
            print endtime+' time format is not correct, should be like %Y-%m-%d_%H%M%S (2017-12-31_080000)'
    global outcsvfilename
    outcsvfilename = os.getcwd()+'/adblog_sqlinfo_'+nodename+'_'+begintime+'_'+endtime+'.csv'
    print 'outcsvfilename is: '+outcsvfilename

def get_logfile():
    postfix = 'csv'
    files = [os.path.join(logdir,fn) for fn in os.listdir(logdir)]
    files.sort(key=os.path.getmtime,reverse=True)
    file_list = []
    for f in files:
     if f.endswith(postfix):
        filenametime = f[-21:-5]
        if filenametime <= begintime:
            file_list.append(f)
            break
        elif filenametime > endtime:
            continue
        else:
          file_list.append(f)

    print begintime,endtime
    for f in file_list:
        print datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')+' start to parse file: '+f 
        get_sqlinfo(f)

def get_opt():
    global nodename
    nodename = sys.argv[1]
    global logdir
    logdir = sys.argv[2]
    if os.path.exists(logdir):
           print 'logdir is: '+logdir 
    else:
           print 'input log dir does not exists!'
           sys.exit(1)
    global begintime
    global endtime
    # get begintime from tmp file
    lastendtimefile = '/tmp/adblog_errlog_endtime'
    try:
        f = open(lastendtimefile,'r')
    except Exception:
        begintime = (datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y-%m-%d_%H%M%S")
    else:
        lastendtime = f.read()
        if lastendtime:
            begintime = lastendtime
            f.close();
        else:   
            begintime = (datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y-%m-%d_%H%M%S")
    endtime =  datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    with open(lastendtimefile, 'w') as f:
        f.write(endtime)
    global outcsvfilename
    outcsvfilename = '/tmp/adblog_errlog_'+nodename+'_'+begintime+'_'+endtime+'.csv'
    print 'outcsvfilename is: '+outcsvfilename          

if __name__ == "__main__":
    # init global var
    print sys.argv[:]
    if (len(sys.argv)) > 1:
       get_opt()
    else:
       get_logrange_input()
    # read logfile and write sqlinfo to csv file
    get_logfile()
    end_process()

