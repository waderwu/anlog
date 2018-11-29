# 功能
- [x] php通过加载我们提供的log.php进行记录日志，包括request 和 response
- [x] 通过访问server.php获取日志，将日志存到数据库里面
- [x] 能够根据关键字进行搜索，可指定搜索请求头或者想要
- [x] 能够根据ip，uri，等进行过滤
- [x] 根据正则进行概率计算进而匹配攻击类型
- [ ] 运用机器学习检测异常流量
- [x] 根据日志获取重放脚本

## 目前存在的问题
- [ ] 如何收集更准确的规则
- [ ] 如何确定每个规则对应的概率

- server.php

获取最新的日志文件并且，以json的格式返回

- log.php

存储日志的

- log/show

显示日志内容

```
[{"model": "log.log", "pk": 1, "fields": {"attackip": "127.0.0.1", "attacktime": "2018-09-16T14:20:02Z", "method": "post", "uri": "/debug.php", "headers": "{'Host': '127.0.0.1', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'User-Agent': 'python-requests/2.9.1', 'Accept': '*/*'}", "data": "system=xxx&xindong=ls", "response": "2018-09-21 07:12:51.727974+00:00"}}, {"model": "log.log", "pk": 2, "fields": {"attackip": "127.0.0.1", "attacktime": "2018-09-16T14:19:58Z", "method": "post", "uri": "/debug.php", "headers": "{'Host': '127.0.0.1', 'User-Agent': 'python-requests/2.9.1', 'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*'}", "data": "system=xxx&xindong=ls", "response": "2018-09-21 07:12:51.727974+00:00"}}]
```

- log/update

从日志服务器上更新日志

- log/replay?id=1

获取重放脚本

```python
import requests

def replay():
    url = "http://127.0.0.1/debug.php"
    headers = {}
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    tmp = {'Host': '127.0.0.1', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive', 'User-Agent': 'python-requests/2.9.1', 'Accept': '*/*'}
    for key in tmp:
        headers[key] = tmp[key]

    data = """system=xxx&xindong=ls"""
    r = requests.post(url, data=data, headers=headers, timeout=5)

    return r.text


if __name__ == "__main__":
    print(replay())
```