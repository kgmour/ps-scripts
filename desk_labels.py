#desk.com api script

import requests
import json
import csv
from pprint import pprint as pp
import datetime
from datetime import date, timedelta
import calendar
import time

labels_list = []
column_headers_labels = ['case_id', 'label']

labels_list.append(column_headers_labels)

page_counter = 1
loops = 499

with open('/home/kevin/data/desk/labels/labels.csv') as j:
	reader = csv.reader(j, delimiter='\t')
	old_data = list(reader)

d = date.today() - timedelta(days=7)

d_str = str(d)

epoch = datetime.datetime(int(d_str[:4]), int(d_str[5:7]), int(d_str[8:10]), 0, 0).strftime('%s')

while loops > 0:
	page_counter_string = str(page_counter)
	desk = 'https://trainsignal.desk.com/api/v2/cases?sort_field=updated_at&fields=id, label,type,status,created_at,updated_at,received_at,first_resolved_at,resolved_at&since_updated_at=' + epoch + '&sort_direction=asc&per_page=100&page=' + page_counter_string
	header = {'Authorization': 'Basic a2V2aW4tbW91cml0c2VuQHBsdXJhbHNpZ2h0LmNvbTo8M05hdGFsaWU=', 'Accept': 'application/json'}
	case_response = requests.get(desk, headers=header)
	case_response_dict = json.loads(case_response.text)
	if '_embedded' in case_response_dict:
		for entry in case_response_dict['_embedded']['entries']:
			case_id = entry['id']
			case_id_string = str(case_id)
			updated_at = entry['updated_at']
			label = 'https://trainsignal.desk.com/api/v2/cases/' + case_id_string + '/labels'
			label_response = requests.get(label, headers=header)
			label_response_dict = json.loads(label_response.text) 
			for name in label_response_dict['_embedded']['entries']:
				labels = []
				labels.append(case_id)
				labels.append(name['name'])
				labels_list.append(labels)
		loops = loops - 1
		page_counter = page_counter + 1
		time.sleep(.3)
		if loops == 1:
			loops = 499
			epoch = datetime.datetime(int(updated_at[:4]), int(updated_at[5:7]), int(updated_at[8:10]), int(updated_at[11:13]), int(updated_at[14:16])).strftime('%s')
		else:
			continue
	else:
		for i in old_data:
			c = len(old_data)
			while c > 0:
				if i[0] != labels_list[c][0] || i[1] != labels_list[c][1]:
					old_data.append(labels_list[c])
					c = c - 1
				else:
					c = c - 1
		with open('/home/kevin/data/desk/labels/labels_new.csv', 'wb') as f:
			writer = csv.writer(f, delimiter='	')
			writer.writerows(old_data)



