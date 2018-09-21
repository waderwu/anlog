import json


j = '{"uri":"\/debug.php","method":"POST","headers":{"Host":"192.168.197.129","User-Agent":"curl\/7.47.0","Accept":"*\/*"},"data":"system=xx&xindong=ls","ip":"127.0.0.1","time":"18-09-15 18:30:20"}'

j = '{"uri":"\/debug.php","method":"POST","headers":{"Host":"192.168.197.129","Accept-Encoding":"gzip, deflate","Accept":"*\/*","User-Agent":"python-requests\/2.9.1","Connection":"keep-alive"},"data":"system=xxx&xindong=ls","ip":"127.0.0.1","time":"18-09-15 23:40:01"}'

d = json.loads(j)

uri = d['uri']
headers = d['headers']
data = d['data']
host = headers['Host']
headers = str(headers)
method = d['method'].lower()

with open("replay", "r") as f:
    script = f.read()

script = script.replace("{uri}", uri)

script = script.replace("{headers}", headers)

script = script.replace("{data}", data)

script = script.replace("{host}", host)

script = script.replace("{method}", method)

print(script)
