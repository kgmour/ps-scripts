#desk.com api script

import requests
import json
import csv
from pprint import pprint as pp
import datetime
from datetime import date, timedelta
import calendar
import time
import ConfigParser

config = ConfigParser.ConfigParser()
config_read = config.read('/home/kevin/Documents/python_scripts/desk_config.ini')

url_1 = config.get('DeskCredentials', 'DeskURL1')
url_2 = config.get('DeskCredentials', 'DeskURL2')
auth = config.get('DeskCredentials', 'Authorization')
username = config.get('KermitCredentials', 'Username')
password = config.get('KermitCredentials', 'Password')
ip_address = config.get('KermitCredentials', 'IPAddress')

cases_list = []
column_headers_cases = ['case_id', 'created_at', 'type', 'status', 'updated_at', 'received_at', 'first_resolved_at', 'resolved_at']
cases_list.append(column_headers_cases)

page_counter = 1
loops = 499

epoch = '1420092000'

while loops > 0:
	page_counter_string = str(page_counter)
	desk = url_1 + epoch + url_2 + page_counter_string
	header = {'Authorization': 'Basic ' + auth, 'Accept': 'application/json'}
	case_response = requests.get(desk, headers=header)
	case_response_dict = json.loads(case_response.text)
	if '_embedded' in case_response_dict:
		for entry in case_response_dict['_embedded']['entries']:
			cases = []
			case_id = entry['id']
			case_id_string = str(case_id)
			cases.append(entry['id'])
			created_at = entry['created_at']
			if created_at is None:
				cases.append('')
			else:
				created_at_string = str(created_at)
				cases.append(created_at_string[:10] + ' ' + created_at_string[11:19])
			cases.append(entry['type'])
			cases.append(entry['status'])
			updated_at = entry['updated_at']
			if updated_at is None:
				cases.append('')
			else:
				updated_at_string = str(updated_at)
				cases.append(updated_at_string[:10] + ' ' + updated_at_string[11:19])
			received_at = entry['received_at']
			if received_at is None:
				cases.append('')
			else:
				received_at_string = str(received_at)
				cases.append(received_at_string[:10] + ' ' + received_at_string[11:19])
			first_resolved_at = entry['first_resolved_at']
			if first_resolved_at is None:
				cases.append('')
			else:
				first_resolved_at_string = str(first_resolved_at)
				cases.append(first_resolved_at_string[:10] + ' ' + first_resolved_at_string[11:19])
			resolved_at = entry['resolved_at']
			if resolved_at is None:
				cases.append('')
			else:
				resolved_at_string = str(resolved_at)
				cases.append(resolved_at_string[:10] + ' ' + resolved_at_string[11:19])
				cases_list.append(cases)
		loops = loops - 1
		page_counter = page_counter + 1
		time.sleep(1)
		if loops == 1:
			loops = 499
			page_counter = 1
			epoch = datetime.datetime(int(updated_at[:4]), int(updated_at[5:7]), int(updated_at[8:10]), int(updated_at[11:13]), int(updated_at[14:16])).strftime('%s')
			continue	
		else:
			print loops
	else:
		with open('/home/kevin/data/desk/cases/cases_new.csv', 'wb') as f:
			writer = csv.writer(f, delimiter='	')
			writer.writerows(cases_list)
		loops = 0

time.sleep(15)

creds = (username, password)
headers = {'Accept': 'application/octet-stream'}

infile = open('@/home/kevin/data/desk/labels/labels.csv')

r = requests.put(ip_address + '/kermit/api/files/user/kevin-mouritsen/desk_labels_stage/labels.csv?overwrite=true', data=infile, auth=creds, headers=headers, verify=False)

