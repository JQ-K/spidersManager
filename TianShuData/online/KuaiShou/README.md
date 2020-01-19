#快手爬虫说明文档



## 一、spiders

### 1.spider:kuaishou_register_did

（1）作用：注册快手did

（2）管道：KuaishouRedisPipeline

- KuaishouRedisPipeline

  主要是对Redis库中key为kuaishou_did的数据，建立一个did池，供快手爬虫使用，主要字段为：如下说明

  ```MySQL
  # value结构为：
  {'did': 'web_6f1b84f77f3d498ea1f8684517d9283f', 'didv': '1577082503000'}
  ```

（3）处理流程：

- [ ] step1：通过访问指定接口，产生did
- [ ] step2：通过访问特定接口，注册did



### 2.releasetask.py

（1）作用：分发任务，现在只做了简单的数据查询并分发，后期考虑如何将任务合理的分布在一天的各个时段

（2）类型：不缺失principalId任务 和  缺失principalId任务

（3）消息目的：kakfa消息列队

（4）消息结构：

- 不缺失principalId任务

  ```json
  {'name': 'kuanshou_kol_seeds', 'userId': 268937622, 'kwaiId': 'YangGe666', 'principalId': 'YangGe666'}
  ```

- 缺失principalId任务

  ```json
  {'name': 'kuanshou_seeds_search', 'userId': 570567973, 'kwaiId': '570567973'}
  ```

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