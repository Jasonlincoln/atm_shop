### 1、需求

```
1、额度 15000或自定义
2、实现购物商城，买东西加入 购物车，调用信用卡接口结账
3、可以提现，手续费5%
4、支持多账户登录
5、支持账户间转账
6、记录每月日常消费流水
7、提供还款接口
8、ATM记录操作日志
9、提供管理接口，包括添加账户、用户额度，冻结账户等。。。
10、用户认证用装饰器

示例代码 https://github.com/triaquae/py3_training/tree/master/atm

简易流程图：https://www.processon.com/view/link/589eb841e4b0999184934329
```

### 2、流程图见附件

### 3、程序结构

```
atm
├── bank # atm程序
│   ├── bin
│   │   ├
│   │   └── start.py # atm启动文件
│   ├── conf
│   │   ├
│   │   └── settings.py # atm 配置文件
│   ├── core  # atm 核心模块
│   │   ├── auth.py  # 用户登陆模块
│   │   ├─
│   │   ├── log.py  # 日志模块
│   │   ├── manager.py # 后台管理模块
│   │   ├── my_bank.py # 主程序
│   │   ├
│   │   └── trans.py # 交易模块
│   ├── db
│   │   ├─
│   │   └── user  # atm用户数据
│   ├── 
│   ├── log
│   │   ├── access.log  # 登陆日志
│   │   └── transactions.log # 交易日志
│   └── 
├── 
└── shop
    ├── 
    ├── core
    │   ├── 
    │   ├── main.py # 商城启动文件
    │   └── 
    │       
    ├── db
    │   ├──
    │   ├── shopping_dic # 购物车数据
    │   └── user # 商城用户数据
    └── __init__.py

```

### 4、测试步骤

```
1、商城
 先注册用户，然后登陆，按提示操作
 
2、atm
atm可以单独启动
atm后台管理：登陆管理员账号:admin 密码：9527

后台管理首页可以选择添加用户或者更新用户信息，特别：输入"q"返回atm登陆界面

运行atm/bin/start.py，单独启动atm程序


```