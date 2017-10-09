# python查询stackalytics.com代码贡献数量

stackalytics.com是一个代码贡献统计网站，统计项目包括OpenStack、docker、kubernetes、ceph、ansible等众多开源明星项目。

1. 环境安装（python2，用virtualenv更好）

        pip install -r requirements.txt

2. 配置config.py

        field = {
          'release': 'queens',     # openstack版本
          'project_type': ['openstack', 'all'],   # openstack项目
          'metric': ['marks', 'commits', 'bpc',   'filed-bugs', 'resolved-bugs', 'loc'],   # openstack度量指标
          'company': ['tencent', 'huawei', 'zte%20corporation','h3c', 'fiberhome', 'china%20unionpay',
                    'china%20mobile', 'inspur', '99cloud', 'easystack', 'awcloud', 'kylin%20cloud'],    # 要查询的公司
          'engineers': {'owercompany': 'Tencent',
                      'ids': ['yao3690093-o', 'krunerge']
                     },     # 要查询的个人
         }

3. 运行

        python get_metric.py
