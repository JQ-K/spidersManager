# 集群规划
本次共创建了3个节点（包括一个主节点和两个工作节点），节点规划如下：
| ip地址        | 主机名 | 节点类型      | 内网ip        |
|---------------|--------|---------------|---------------|
| 118.31.58.116 | zqhd5  | redis         | 172.16.62.228 |
| 47.98.235.102 | zqhd6	 | 工作节点      | 172.16.62.234 |
| 47.110.255.29 | zqhd7	 | 工作节点      | 172.16.62.233 |
| 118.31.9.94   | zqhd8  | 主节点、mongo | 172.16.62.235 |

# 账号信息
1. hadoop账号信息
用户名：hadoop 密码：5KHlWSSd
2. root账号信息
使用堡垒机登录即为root账号

# 安装

## 要求
[源码下载：crawlab-team/crawlab](https://github.com/crawlab-team/crawlab)
* Go 1.12+
* Node 8.12+
* Redis
* MongoDB 3.6+

## master节点安装
* 源码位置：/data/server/crawlab-master

### 安装前后端所需的库

#### 安装前端所需的库
npm install -g yarn
cd /data/server/crawlab-master/frontend
yarn install

#### 安装后端所需的库
cd /data/server/crawlab-master/backend
go install ./...

### 修改前后端配置文件

#### 修改前端配置文件
文件位置：./frontend/.env.production
```
NODE_ENV='production'
VUE_APP_BASE_URL='http://118.31.9.94:8000'
```

#### 修改后端配置文件
文件位置：./backend/conf/config.yml
```
api:
  address: "172.16.62.235:8000"
mongo:
  host: 172.16.62.235
  port: 27017
  db: crawl
  username: ""
  password: ""
  authSource: "admin"
redis:
  address: 172.16.62.228
  password: ""
  database: 2
  port: 6379
log:
  level: info
  path: "/data/code/crawlab-master/logs/crawlab"
  isDeletePeriodically: "N"
  deleteFrequency: "@hourly"
server:
  host: 0.0.0.0
  port: 8000
  master: "Y"
  secret: "crawlab"
  register:
	# mac地址 或者 ip地址，如果是ip，则需要手动指定IP
    type: "mac"
    ip: ""
spider:
  path: "/data/code/crawlab-master/spiders"
task:
  workers: 4
other:
  tmppath: "/data/code/crawlab-master/tmp"
```

### 构建前后端

#### 构建前端
cd /data/server/crawlab-master/frontend
npm run build:prod
构建完成后，会在./frontend目录下创建一个dist文件夹，里面是打包好后的静态文件。
安装nginx，yum install nginx
添加/etc/nginx/conf.d/crawlab.conf文件，输入以下内容：
```
server {
    listen    8080;
    server_name    dev.crawlab.com;
    root    /data/server/crawlab-master/frontend/dist;
    index    index.html;
}
```
运行命令：nginx -s reload

#### 构建后端
cd /data/server/crawlab-master/backend
go build
构建完成后，会在./backend目录下创建crawlab可执行文件

### 启动服务
cd /data/server/crawlab-master/backend
nohup crawlab &
启动成功，打开浏览器：http://118.31.9.94:8080


## worker节点安装
* 源码位置：/data/server/crawlab-master

### 安装后端所需的库
同master节点

### 修改后端配置文件
文件位置：./backend/conf/config.yml
```
api:
  address: "172.16.62.235:8000"
mongo:
  host: 172.16.62.235
  port: 27017
  db: crawl
  username: ""
  password: ""
  authSource: "admin"
redis:
  address: 172.16.62.228
  password: ""
  database: 2
  port: 6379
log:
  level: info
  path: "/data/code/crawlab-master/logs/crawlab"
  isDeletePeriodically: "N"
  deleteFrequency: "@hourly"
server:
  host: 0.0.0.0
  port: 18000
  master: "N"
  secret: "crawlab"
  register:
    # mac地址 或者 ip地址，如果是ip，则需要手动指定IP
    type: "mac"
    ip: ""
spider:
  path: "/data/code/crawlab-master/spiders"
task:
  workers: 4
other:
  tmppath: "/data/code/crawlab-master/tmp"
```

### 构建后端
同master节点

### 启动服务
cd /data/server/crawlab-master/backend
nohup crawlab &

# 附
[官方部署文档](https://tikazyq.github.io/crawlab-docs/Installation/Direct.html)