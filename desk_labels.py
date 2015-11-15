#desk.com api script

import requests
import json
import csv
from pprint import pprint as pp
import datetime
import calendar
import time
import ConfigParser

# Read in private data from config file
config = ConfigParser.ConfigParser()
config.read('/home/kevin/Documents/python_scripts/Desk.com/config/desk_config.ini')
url_1 = config.get('DeskCredentials', 'DeskURL1')
url_2 = config.get('DeskCredentials', 'DeskURL2')
url_3 = config.get('DeskCredentials', 'DeskURL3')
auth = config.get('DeskCredentials', 'Authorization')
username = config.get('KermitCredentials', 'Username')
password = config.get('KermitCredentials', 'Password')
ip_address = config.get('KermitCredentials', 'IPAddress')


# Set up list to receive records
labels_list = []
column_headers_labels = ['case_id', 'label']
labels_list.append(column_headers_labels)

# Set up initial variables for main loop
page_counter = 1
loops = 499

# Epoch is the utc time code where the script will start pulling data from
epoch = '1388556000'

# Use custom adapters to force script to keep trying if Internet connection is temporarily lost
session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))

# Execution of main loop, which pulls data from Desk.com
while loops > 0:
	page_counter_string = str(page_counter)
	desk = url_1 + epoch + url_2 + page_counter_string
	header = {'Authorization': 'Basic ' + auth, 'Accept': 'application/json'}
	case_response = session.get(url=desk, headers=header)
	try:
		case_response_dict = json.loads(case_response.text)
	except ValueError as e:
		print case_response.text
		print e
	if '_embedded' in case_response_dict:
		for entry in case_response_dict['_embedded']['entries']:
			case_id = entry['id']
			case_id_string = str(case_id)
			updated_at = entry['updated_at']
			label = url_3 + case_id_string + '/labels'
			label_response = session.get(url=label, headers=header)
			try:
				label_response_dict = json.loads(label_response.text)
			except ValueError as e:
				print e
				print label_response.text 
			for name in label_response_dict['_embedded']['entries']:
				labels = []
				labels.append(case_id)
				labels.append(name['name'])
				labels_list.append(labels)
		loops = loops - 1
		page_counter = page_counter + 1
		time.sleep(.7)
		if loops == 1:
			loops = 499
			page_counter = 1
			epoch = datetime.datetime(int(updated_at[:4]), int(updated_at[5:7]), int(updated_at[8:10]), int(updated_at[11:13]), int(updated_at[14:16])).strftime('%s')
			continue
		else:
			print loops
			continue
	else:
		# Creates .csv file of tab-delimited list of lists
		with open('/home/kevin/data/desk/labels/labels_new.csv', 'wb') as f:
			writer = csv.writer(f, delimiter='	')
			writer.writerows(labels_list)
		time.sleep(15)
		# Sends newly created .csv file to DataHub
		creds = (username, password)
		headers = {'Accept': 'application/octet-stream'}
		infile = open('/home/kevin/data/desk/labels/labels_new.csv')
		r = requests.put(ip_address + '/kermit/api/files/user/kevin-mouritsen/desk_labels_stage/labels.csv?overwrite=true', data=infile, auth=creds, headers=headers, verify=False)
		loops = 0
		print 'Process Complete'