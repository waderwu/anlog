from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
import requests as rq
import json
from datetime import datetime

# Create your views here.


def index(requests):
    return render(requests, "index.html")


def login(requests):
    return HttpResponse("hello man")


def update(requests):
    url = "http://192.168.197.131/logser.php"
    r = rq.get(url)
    jsonr = json.loads(r.text)
    print(jsonr)
    for key in jsonr:
        jlog = json.loads(jsonr[key])
        ip = jlog['ip']
        time = datetime.strptime(jlog['time'], "%Y-%m-%d %H:%M:%S")
        method = jlog['method'].lower()
        log = Log(attackip=ip, attacktime=time, method=method, uri=jlog['uri'], headers=jlog['headers'], data=jlog['data'])
        log.save()
    return HttpResponse("ok")
