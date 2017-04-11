#!/usr/bin/env python

import csv
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


def read_ibm_csv():
    with open('/home/kevin/Downloads/IBM_Data.csv', 'rb') as f:
        reader = csv.reader(f)
        ibm_data = list(reader)
        return ibm_data


def pull_domains_and_remove_duplicates(ibm_data):
    emails = list(set([i[4] for i in ibm_data]))
    domains = []
    for i in emails:
        if '@' in i:
            index = i.index('@')
            domains.append(i[index:])
        else:
            continue
    return domains


def create_dict_of_domains_and_convert_to_list(domains):
    location_data = {domain: domains.count(domain) for domain in domains}
    new_data = map(list, location_data.items())
    return new_data


def create_csv_with_domain_and_number_of_users_on_that_domain(new_data):
    with open('/home/kevin/Desktop/ibm.csv', 'w') as fout:
        csv_out = csv.writer(fout)
        csv_out.writerows(['Domains', 'Amount'])
        for row in new_data:
            csv_out.writerow(row)


if __name__ == '__main__':
    ibm_report = read_ibm_csv()
    ibm_domains = pull_domains_and_remove_duplicates(ibm_report)
    ibm_list = create_dict_of_domains_and_convert_to_list(ibm_domains)
    create_csv_with_domain_and_number_of_users_on_that_domain(ibm_list)
