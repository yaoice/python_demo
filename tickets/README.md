# python3查询12306火车票

由于12306的接口经常变化，有可能需要根据最新的接口对代码进行适当修改才能正常运行。

1. 环境安装（python3，用virtualenv更好）

        pip install -r requirements.txt

2. 如何运行

        python tickets.py -gd 深圳 杭州 2017-10-14

        python tickets.py（查看使用方法）

3. 原理

      - 使用chrome的开发者工具，发送网页查询请求，在开发者工具Network拦过滤出类型为xhr的请求，形如https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date=2017-10-25&leftTicketDTO.from_station=IOQ&leftTicketDTO.to_station=FZS&purpose_codes=ADULT

      - 输入进去的是中文地名，需要转换为对应的英文地名；地名对应关系，在这个js中指定https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9027
      （可查询当前网页，看最新import进去的js路径），可通过tickets.py中的transferStation函数生成stations.py

      - r.json()['data']['result']返回的是一个列表，每个车
      次是一个长字符串，中间用‘|’分隔。

4. 参考链接

      - https://www.shiyanlou.com/courses/623
      - http://www.jianshu.com/p/1b755b0bbebf
