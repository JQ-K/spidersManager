#快手爬虫说明文档



## 一、spiders

### 1.spider:kuaishou_register_did

（1）作用：注册快手did

（2）管道：KuaishouRedisPipeline

- KuaishouRedisPipeline

  在redis中动态加入注册的did到did池中，其中did池是由一个有序的set，其中key值为kuaishou_did，成员及其分数分别为注册的含有did的cookie值和过期时间

  ```MySQL
  # 手动添加命令
  ZADD kuaishou_did "kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1;clientid=3;did=web_2f207c637e9a28073fcf40986503b7c6;client_key=65890b29;" 15700000000
  ```

（3）处理流程：

- [ ] step1：通过访问指定接口，产生did
- [ ] step2：通过docker容器模拟页面加载对did注册激活



### 2.spider:kuaishou_search_overview

（1）作用：监听种子topic，实时更新用户的动态数据等

（2）管道：KuaishouKafkaPipeline，KuaishouScrapyLogsMySQLPipeline，KuaishouUserSeedsMySQLPipeline

- KuaishouKafkaPipeline

  获取KOL的动态数据，比如粉丝数等，并将最新的数据发送到topic[kuaishou_online_daily]，供数据整合端对数据进一步处理

- KuaishouScrapyLogsMySQLPipeline

  记录KOL种子动态数据更新任务的最终结果，并记录下来

- KuaishouUserSeedsMySQLPipeline

  对查询到的KOL静态数据，主要是kwaiId和principalId，进行跟新，同时更新下一次任务调度时间

### 3.Scrapy-Splash的安装

Scrapy-Splash的安装分为两部分，一个是Splash服务的安装，具体通过Docker来安装服务，运行服务会启动一个Splash服务，通过它的接口来实现JavaScript页面的加载；另外一个是Scrapy-Splash的Python库的安装，安装后就可在Scrapy中使用Splash服务了，下面我们分三部份来安装：

#### (1)安装Docker

```powershell
#安装所需要的包：
yum install -y yum-utils device-mapper-persistent-data lvm2
#设置稳定存储库：
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#开始安装DOCKER CE：
yum install docker-ce
#启动dockers：
systemctl start docker
#测试安装是否正确：
docker run hello-world
```

#### (2)安装splash服务

通过Docker安装Scrapinghub/splash镜像，然后启动容器，创建splash服务

```shell
docker pull scrapinghub/splash
docker run -d -p 8050:8050 scrapinghub/splash
#通过浏览器访问8050端口验证安装是否成功
```

#### (3)Python包Scrapy-Splash安装

```shell
pip3 install scrapy-splash
```