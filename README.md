# 监视我的手机：数据都去哪儿了？

> _**警告**: 请勿用于非法目的，非法获取他人隐私属于犯罪!_

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716170641.png" width="80%" /></div>

**日常使用的手机可能比想象的更加活跃**，当微信聊天、淘宝购物、抖音看视频甚至是喵的手机待机啥也不干，某些 App 都会悄悄地与服务器交换着数据。这些数据包括微信聊天记录、地理位置、通讯录、通话记录、QQ消息，甚至短信
内容...

我一直想知道**我的数据都去了哪里**？**哪些 App 在源源不断上传数据**？**数据被哪些公司搜集了**？

前一段时间，浏览过一篇国外的博客《[Tracking my phone's silent connections](https://kushaldas.in/posts/tracking-my-phone-s-silent-connections.html)》，文中作者 Kushal 使用 WireGuard 代理的方式，监控自己的手机 1 个星期，截获手机与服务器之间的所有请求，最后统计了手机到底悄悄地在和哪些公司的服务器进行连接。

受到 Kushal 的启发，我决定使用部署 ss 的方式截获我个人的手机数据。

## 监控方案

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190715193635.png" width="80%" /></div>

### 实验设备

- 日常使用的安卓手机 `x1`
- 国内某云服务器 `x1`

### 代理方案

手机的数据都是与不同的服务器进行着连接，如何获取所有的连接？首先我想到的是手机要通过 Wi-Fi 路由器上网，那么如果在路由器端截取数据包，会比较容易。但是无法获取手机的移动基站流量。

于是在 1 台云服务器上搭建了个代理服务，手机客户端设置为全局代理连接 VPN 服务器，就可以在服务器端获取所有的数据请求。

### 部署服务

为了保证上网访问速度，提升网络体验，推荐选择国内的服务器，代理服务器首先安装 Docker

```shell
$ sudo apt-get -y install docker.io
```

**启动 ss Docker 容器**

通过阅读 ss 的文档，可知在启动 ss 时只需要加上 `-v` 参数(Verbose mode)即可输出详细 Log。同时使用 `tmux` 让服务在后台运行，将输出以追加的方式(`>>`)重定向到 `logs.txt` 文件。

```shell
$ tmux
$ sudo docker run -t --name ss -p 9000:9000 mritd/shadowsocks -s "-s 0.0.0.0 -p 9000 -m aes-256-cfb -k yourpassword --fast-open -v" >> logs.txt
```

**手机客户端**

在手机端安装 ss 或者酸酸乳客户端，配置代理服务器地址、端口、密码与加密方式，代理模式设置为全局代理。

然后在服务器端，使用 `tail` 命令从指定点开始将从文件写到标准输出，显示实时 Log，服务搭建成功

```shell
$ tail -f logs.txt
```

当手机使用微信时，记录的 Log 日志如下

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716105753.png" width="80%" /></div>


### 数据处理

**DNS 域名解析**

DNS(Domain Name System)，翻译过来就是域名系统，是互联网上作为域名和 IP 地址相互映射的一个分布式数据库。获取到的记录大多数是域名，

```python
import socket
def domain_to_ip(domain):
    return socket.gethostbyname(domain)
```
例如，解析 `www.baidu.com` 的 IP 地址
```Python
domain_to_ip('www.baidu.com')
'14.215.177.38'
```

**IP 地理数据库**

推荐使用 [ip2region](https://github.com/lionsoul2014/ip2region)，一个开源的 IP 到地区的映射库，具有 99.9% 准确率，提供 Binary,B 树和纯内存三种查询快速搜索算法。

```python
>> result = ipgeo.find('www.baidu.com')
>> print(result)
{'ip': '14.215.177.38', 'city_id': 2140, 'country': '中国', 'province': '广东省', 'city': '广州市', 'operator': '电信'}
```

**保存数据**

```python
df.to_csv(out_csv, index=False)
print('saved to {}'.format(out_csv))
```

### 数据可视化

经过十多天的记录，俺一共记录了 `280059` 条记录

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716182131.png" width="50%" /></div>

接下来使用 Pyecharts 对数据进行可视化。Echarts 是百度开源的一个数据可视化 JS 库，而 Pyecharts 是一个用于生成 Echarts 图表 Python 库。

#### 主要的互联网公司

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716091323.png" width="80%" /></div>

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716163609.png" width="80%" /></div>

从上图可以看出，俺的安卓手机(安装了谷歌服务)，在国内的网络环境，请求次数最多还是 Google。

然后就是日常使用的微信和 QQ 了。由于平时会看 B 站视频，所以 Bilibili 排名第三 orz...

我手机安装的是 QQ 输入法，但是去往 `sougou.com` 的请求居然有 `1952` 条，查看了用户协议才发现 `“QQ输入法”是经腾讯公司认可，由搜狗公司发布的客户端软件。`

还有像美团、高德地图这样的软件，平时并不怎么频繁使用，网络请求却异常地活跃，不知道偷偷摸摸干着啥。

#### 夜间活动排行

过滤出凌晨 00:00 ~ 06:00 时间段的活动，可以发现去往 `*.qq.com` 的连接始终是最多的。

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716164538.png" width="80%" /></div>

#### 全球分布

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716091052.png" width="80%" /></div>

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716091018.png" width="80%" /></div>

#### 国内各省份分布

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716091206.png" width="80%" /></div>

可以看到俺的流量大多去往了广东、上海和北京这样的地方，台湾这么高的原因是谷歌的服务器在那边，DNS 解析谷歌的域名都指向了台湾。

#### 电信运营商

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716095130.png" width="80%" /></div>

#### 服务器端口统计

<div style="text-align:center"><img src ="https://raw.githubusercontent.com/wangshub/image-hosting/master/img/20190716091544.png" width="80%" /></div>

#### 其他

在一加手机的网络请求中，发现了一些发往 oppo 服务器的请求，看来不光硬件由 oppo 代工，连软件也是。

```python
[('epoch.cdo.oppomobile.com', 208),
 ('gslb.cdo.oppomobile.com', 38),
 ('istore.oppomobile.com', 38),
 ('opsapi.store.oppomobile.com', 34),
 ('api.cdo.oppomobile.com', 22),
 ('message.pull.oppomobile.com', 21),
 ('st.pull.oppomobile.com', 13),
 ('cdopic0.oppomobile.com', 9),
 ('newds01.myoppo.com', 9),
 ('httpdns.push.oppomobile.com', 4),
 ('conn1.oppomobile.com', 1),
 ('iopen.cdo.oppomobile.com', 1)
```

### 最后

> _吉利控股集团创始人、董事长李书福曾说 “现在的人几乎是全部透明的。我心里就想，马化腾肯定天天在看我们的微信，因为他都可以看的，随便看，这些问题非常大。”_

### 完整代码

[https://github.com/wangshub/tracking-my-phone](https://github.com/wangshub/tracking-my-phone)

- 如果需要更为详细的数据，可以考虑使用 [mitmproxy](https://mitmproxy.org/) 代理，能够抓取 HTTPS 数据，并提供 Python API。

### 参考链接

- [Tracking my phone's silent connections](https://kushaldas.in/posts/tracking-my-phone-s-silent-connections.html)
- [ip2region: Ip2region is a offline IP location library](https://github.com/lionsoul2014/ip2region)
- [Python Data Analysis Library](https://pandas.pydata.org/)
- [Pyecharts: A Python Echarts Plotting Library.](https://pyecharts.org)
