#/usr/bin/env python

import httplib2
import json
import sys
from prettytable import PrettyTable
from config import field


class BaseStackalytics(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseStackalytics, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class Stackalytics(BaseStackalytics):
    def __init__(self, prefix):
        super(Stackalytics, self).__init__()
        self._prefix = prefix
        self._http_instance = self.get_http_instance()

    def get_http_instance(self):
        return httplib2.Http(".cache")

    def get_metrics(self, url):
        try:
            return self._http_instance.request(self._prefix + url,
                                               "GET",
                                               headers={'Accept': 'application/json'})
        except httplib2.ServerNotFoundError:
            print "Url {} not found".format(url)
            sys.exit(1)



def main():

    company_statistics = {}
    engineer_statistics = {}

    stackalytics = Stackalytics("http://stackalytics.com")
    
    for project_type in field['project_type']:
        company_statistics[project_type] = {}
        for company in field['company']:
            company_statistics[project_type][company] = {}

            for metric in field['metric']:
                company_statistics[project_type][company][metric] = {}
                url = "/api/1.0/stats/companies?release={}&metric={}&project_type={}&company={}".format(field['release'],
                                                                                                        metric,
                                                                                                        project_type,
                                                                                                        company)
                resp, content = stackalytics.get_metrics(url)
                stats = json.loads(content)['stats']
                try:
                    metric_dict = stats[0]
                except IndexError:
                    metric_dict = {'id': company, 'metric': 0}
                company_statistics[project_type][company][metric] = metric_dict


    for project_type in field['project_type']:
        engineer_statistics[project_type] = {}
        for engineer in field['engineers']['ids']:
            engineer_statistics[project_type][engineer] = {}
            for metric in field['metric']:
                engineer_statistics[project_type][engineer][metric] = {}
                engineers_url = "/api/1.0/stats/engineers?&release={}&metric={}"\
                                "&project_type={}&company={}&user_id={}".format(field['release'],
                                                                                metric,
                                                                                project_type,
                                                                                field['engineers']['owercompany'],
                                                                                engineer)
                engineers_resp, engineers_content = stackalytics.get_metrics(engineers_url)
                engineers_stats = json.loads(engineers_content)['stats']
                try:
                    engineers_metric_dict = engineers_stats[0]
                except IndexError:
                    engineers_metric_dict = {'id': engineer, 'metric': 0}
                engineer_statistics[project_type][engineer][metric] = engineers_metric_dict

    engineer_table_field = ['metric'] + [engineer for engineer in field['engineers']['ids']]
    for project_type in field['project_type']:
        print "{} {} project by tencent individual:".format(field['release'], project_type)
        table = PrettyTable(engineer_table_field)
        for metric in field['metric']:
            table.add_row([metric] + [engineer_statistics[project_type][engineer][metric]['metric'] for engineer in field['engineers']['ids']])
        print table

    table_field = ['metric'] + [company.replace('%20', ' ') for company in field['company']]
    for project_type in field['project_type']:
        print "{} {} project by company:".format(field['release'], project_type)
        table = PrettyTable(table_field)
        for metric in field['metric']:
            table.add_row([metric] + [company_statistics[project_type][company][metric]['metric'] for company in field['company']])
        print table

#    print company_statistics



if __name__ == '__main__':
    sys.exit(main())
