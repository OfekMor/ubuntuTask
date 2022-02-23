import json
from os import listdir
from os.path import isfile, join
from socket import socket, error
from datetime import datetime

FOLDER_PATH = r'/var/log/audit'
host, port = "localhost", 514

onlyfiles = [f for f in listdir(FOLDER_PATH) if isfile(join(FOLDER_PATH, f))]

server_name = ''
date = datetime.now()
dt = date.strftime("%d/%m/%y %H:%M:%S")
audit_log_json = {}

audit_log_json.update({'date': dt})
audit_log_json.update({'name': server_name})

def check_duplicated_rows(auditlog):
    seen = []
    for x in auditlog:
        if x not in seen:
            yield x
            seen.append(x)

def get_and_parse_log():
    for file in onlyfiles:
        if file.startswith("audit.log"):
            audit_log = open(f'/var/log/audit/{file}', 'r')

            for line in audit_log.readlines():
                check_duplicated_rows(audit_log)
                small = {
                }
                for objects in line.split(" "):
                    part = objects.split('=')
                    if len(part) > 1:
                        small.update({part[0]: part[1].replace('\n', "")})

                audit_log_json.update(small)
            print(audit_log_json)
            audit_log.close()

data = json.dumps(audit_log_json)
get_and_parse_log()

def send_parsed_data_to_localhost(parsedData):
    try:
        s = socket()
        s.connect((host, int(port)))
        server_name(s.getsockname())
        print('server name - ' + server_name)
        s.settimeout(4)
        s.send(parsedData)
        s.recv(800)
        s.close()
    except error:
        audit_log_json.update(f'an exception is occured:\n{error}')
        s.close()

send_parsed_data_to_localhost(data)
