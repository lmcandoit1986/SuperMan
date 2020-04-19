# SuperMan

## 主体内容

+ 展示各个平台最近自动化执行情况,以及列表展示
+ 结果页面展示   
1）功能自动化结果页面   
2）性能自动化（App）结果页面

### 实例

+ [主页面](http://152.136.202.79:9092/web/index)

+ [自动化测试结果页面](http://152.136.202.79:9092/web/result/detail?jenkinsId=25&platform=android&test)

+ [性能测试结果页面](http://152.136.202.79:9092/web/performance/detail?jenkinsId=32&platform=iOS)

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
    
    
    { 'data':{
	'sum':{
        'Jenkinsid':7,
        'app':'平安健康险',
        'model':'iPhone8P',
        'runt':'2019-07-01 12:10:06',
        'codev':'0001',
        'platform':'iOS'
        },
    'data':{'fps':
            [
                          {'activity': 'ac1', 'data': [{'fpslist': [45, 56, 45, 65, 75, 56, 23, 43, 53, 43, 23]}, {'fpslist': [41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87]}, {'fpslist': [23, 34, 53, 41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34]}], 'info': '页面info'}, 
                          {'activity': 'ac2', 'data': [{'fpslist': [45, 56, 45, 65, 75, 56, 23, 43, 53, 43, 23]}, {'fpslist': [41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87]}, {'fpslist': [23, 34, 53, 41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34]}], 'info': '页面info'}, 
                          {'activity': 'ac3', 'data': [{'fpslist': [45, 56, 45, 65, 75, 56, 23, 43, 53, 43, 23]}, {'fpslist': [41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87]}, {'fpslist': [23, 34, 53, 41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34]}], 'info': '页面info'}
                          ],
                      'mem':
                          [
                          {'activity': '主页面', 'data': [45, 56, 45, 65, 75, 56, 23, 43, 53, 43, 23], 'info': '页面info'}, 
                          {'activity': '副页面', 'data': [41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87], 'info': '页面info'}, 
                          {'activity': '第三页面', 'data': [23, 34, 53, 41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87], 'info': '页面info'}
                          ],
                      'cpu':
                          [
                          {'activity': '主页面', 'data': [45, 56, 45, 65, 75, 56, 23, 43, 53, 43, 23], 'info': '页面info'}, 
                          {'activity': '副页面', 'data': [41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87], 'info': '页面info'}, 
                          {'activity': '第三页面', 'data': [23, 34, 53, 41, 52, 35, 65, 75, 56, 23, 43, 53, 43, 23, 34, 34, 54, 22, 45, 66, 76, 76, 87], 'info': '页面info'}],
                      'pt':
                          [
                          {'activity': '主页面', 'data': 540, 'info': '页面info'}, 
                          {'activity': '副页面', 'data': 645, 'info': '页面info'}, 
                          {'activity': '第三页面', 'data': 877, 'info': '页面info'}
                          ],
                      'st':
                          {'data': [56, 34, 436, 234, 456, 456], 'sumer': 456}
              }
          }
    }
    
    
#### 接口自动化部分
##### 接口监控结果上传

接口：

>http://152.136.202.79:9092/server/monitor/push

请求方式:
>POST

参数：
>body 按照以下JSON 格式组织自动化测试结果

JSON:

    {
        'data':{
            'rt':'2019-7-4 12:00:00', # 触发时间
            'allCaseNum':100,#总用例数
            'FailCaseName':10,# 失败用例数
            'only':1,# 唯一标识，用于结果展示定位
            'result':
                [
                    {
                        'model':'医疗', # 所属模块
                        'api':'preAuthorizationApply.json',# 接口名称
                        'charger':'负责人',
                        'caseName':'用例名称',
                        'res':0 or -1,# -1 为失败，0 pass，有其他状态可以再定义
                        'useTime':1000,#耗时
                        'comment':'日志信息',
                    },
                    {
                        'model':'医疗',
                        'api':'',
                        'charger':'',
                        'caseName':'',
                        'res':'',
                        'useTime':1000,
                        'comment':'',
                    }
                ]
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
>jenkinsId=32 #结果上传时JenkinsID值，此值尽量保持唯一

>platform=android #结果上传时platform值

举例：
>http://152.136.202.79:9092/web/performance/detail?jenkinsId=32&platform=iOS

#### 接口监控部分

接口：
>http://152.136.202.79:9092/web/watcher

请求方式：
>GET

参数：
>only=1 #结果上传时only值，此值需要保持唯一

举例：
>http://152.136.202.79:9092/web/watcher?only=1



