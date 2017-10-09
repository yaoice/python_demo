# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""

from colorama import init, Fore
from docopt import docopt
from itertools import zip_longest as izip
from prettytable import PrettyTable
from pprint import pprint
from stations import stations
import requests

init()

class TrainsCollection:

    header='车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座 备注'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options

    @property
    def trains(self):
        for raw_train in self.available_trains:
            raw_train_split = raw_train.split('|')
            train_no = raw_train_split[3]
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.BLUE + stations_to_name[raw_train_split[6]] + Fore.RESET,
                               Fore.RED + stations_to_name[raw_train_split[7]] + Fore.RESET]),
                    '\n'.join([Fore.BLUE + raw_train_split[8] + Fore.RESET,
                               Fore.RED + raw_train_split[9] + Fore.RESET]),
                    raw_train_split[10],
                    raw_train_split[-5],
                    raw_train_split[-6],
                    raw_train_split[-13],
                    raw_train_split[-8],
                    raw_train_split[-7],
                    raw_train_split[-10],
                    raw_train_split[1],
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


def search():
    """command line interface"""
    arguments = docopt(__doc__)
#    print(arguments)
    global stations_to_name
    stations_to_name = invert_dict_fast(stations)
    from_station=stations.get(arguments['<from>'])
    to_station=stations.get(arguments['<to>'])
    date=arguments['<date>']
    url='https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date,from_station,to_station
    )

    r = requests.get(url, verify=False)
#    pprint(r.json()['data']['result'])
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    available_trains = r.json()['data']['result']
    TrainsCollection(available_trains, options).pretty_print()


def invert_dict_fast(d):
    return dict(izip(d.values( ), d.keys( )))


def transferStation():
    import re
    import requests
    from pprint import pprint

    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
    response = requests.get(url, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    pprint(dict(stations), indent=4)


if __name__ == '__main__':
    search()
