# SuperMan

## 主体内容

1. 展示各个平台最近自动化执行结果走势，以及列表展示
2. 结果也没展示，目前主要是分功能自动化 和 性能自动化（App）结果

### 实例

[主页面](http://152.136.202.79:9092/web/index)

[自动化测试结果页面](http://152.136.202.79:9092/web/result/detail?jenkinsId=25&platform=android&test)

[性能测试结果页面](http://152.136.202.79:9092/web/performance/detail?jenkinsId=32&platform=iOS)

## 使用相关

### 结果上传

#### 功能自动化部分

接口：
>http://152.136.202.79:9092/server/result/push

请求方式：
> POST

参数：
>body 按照以下JSON 格式组织自动化测试结果

JSON:

(''')
    {
    'data':{'sum':{
                'platform':'iOS',
                'runt':'2019-07-04 12:10:01',
                'model':'iPhone 6s',
                'uset':'5m',
                'Jenkinsid':'25',
                'app':'平安健康险',
                'all':5,
                'fail':1,
            },
            'detail':[
                {
                    'caseName':'Login',
                    'result':0,
                    'comment':'',
                    'pic':''
                },
                {
                    'caseName':'Buy',
                    'result':-1,
                    'comment':'失败日志',
                    'pic':'1230148182.png'	
                }
                ]
        }
    }
(''')


#### 性能自动化部分