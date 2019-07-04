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

    {
        'data':
            {
                'sum':{
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


#### 性能自动化部分

接口：
>http://152.136.202.79:9092/server/pt/push

请求方式：
> POST

参数：
>body 按照以下JSON 格式组织自动化测试结果

JSON:
    
    
    { 
        'data':
            {
              'sum':{
                  'Jenkinsid':1,
                  'app':'百度',测试App名称，统一即可，也可以写app Package 或 Boundid
                  'model':'HuaweiP9',设备型号
                  'runt':'2019-07-01 12:10:01', 脚本触发的时间标示
                  'codev':'123 代码code版本',
                  'platform':'android or iOS'
                  },
              'data':{
                  'fps':
                          [
                              {'activity':'页面标识，最好为英文，会在结果页面展示',
                               'info':'页面简单信息介绍',
                               'data':[45,46,47,56,43,45,45]
                               },
                           ],
                  'mem':
                          [
                              {'activity':'页面标识，最好为英文，会在结果页面展示',
                               'info':'页面简单信息介绍',
                               'data':[45,46,47,56,43,45,45]
                               },
                          ],
                  'cpu':
                          [
                              {'activity':'',
                              'info':'',
                              'data':[23,12,41,32,12]
                              },
                          ],
                  'pt':
                          [
                              {'activity':'',
                               'info':'',
                               'data':460
                               },
                           ],
                  'st':
                          {
                              'sumer':123,
                              'data':[12,123,1234,12345]
                          }
                  }
            }
    }
    
### 结果展示

#### 功能自动化部分
接口：
>http://152.136.202.79:9092/web/result/detail

请求方式：
>GET

参数：
>jenkinsId=25 #结果上传时JenkinsID值，此值尽量保持唯一

>platform=android #结果上传时platform值

举例：
>http://152.136.202.79:9092/web/result/detail?jenkinsId=25&platform=android

#### 性能自动化部分
接口：
>http://152.136.202.79:9092/web/performance/detail

请求方式：
>GET

参数：
>?jenkinsId=32 #结果上传时JenkinsID值，此值尽量保持唯一

>platform=android #结果上传时platform值

举例：
>http://152.136.202.79:9092/web/performance/detail?jenkinsId=32&platform=iOS