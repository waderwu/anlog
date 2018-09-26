from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Log
import requests as rq
import json
from datetime import datetime

# Create your views here.


def index(requests):
    log_list = Log.objects.all()
    paginator = Paginator(log_list, 1)

    page = requests.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    page_info = {}
    page_info['has_previous'] = logs.has_previous
    page_info['previous_page_number'] = logs.previous_page_number
    page_info['number'] = logs.number
    page_info['num_pages'] = logs.paginator.num_pages
    page_info['has_next'] = logs.has_next
    page_info['next_page_number'] = logs.next_page_number

    dicts = []
    for i, log in enumerate(logs):
        item = {}
        item['index'] = i+1
        item['attackip'] = log.attackip
        item['attacktime'] = log.attacktime
        item['method'] = log.method
        item['path'] = log.path
        item['headers'] = log.headers
        item['post'] = log.post
        item['get'] = log.get
        item['response'] = log.response
        dicts.append(item)

    return render(requests, "index.html", {'contents': dicts, 'page_info': page_info})


def login(requests):
    return HttpResponse("hello man")


def update(requests):
    url = "http://192.168.197.132/logser.php"
    r = rq.get(url)
    jsonr = json.loads(r.text)
    print(jsonr)
    for key in jsonr:
        jlog = json.loads(jsonr[key])
        ip = jlog['ip']
        time = datetime.strptime(jlog['time'], "%Y-%m-%d %H:%M:%S")
        method = jlog['method'].lower()
        response = jlog['response']
        log = Log(attackip=ip, attacktime=time, method=method, path=jlog['path'], headers=jlog['headers'], post=jlog['post'], get=jlog['get'], response=response)
        log.save()
    return HttpResponse("ok")


def replay(requests):
    logid = requests.GET['id']
    log = Log.objects.get(pk=logid)
    return HttpResponse(log.replay())


def show(requests):
    logs = Log.objects.all()

    jslogs = serializers.serialize("json", logs)
    return HttpResponse(jslogs, content_type="application/json")


def search(requests):
    keyword = requests.GET['keyword']

    retjs = {}

    datalogs = Log.objects.filter(data__iregex=keyword)
    retjs['data'] = serializers.serialize("json", datalogs)

    headerslogs = Log.objects.filter(headers__iregex=keyword)
    retjs['headers'] = serializers.serialize("json", headerslogs)

    urilogs = Log.objects.filter(headers__iregex=keyword)
    retjs['uri'] = serializers.serialize("json", urilogs)

    urilogs = Log.objects.filter(uri__iregex=keyword)
    retjs['uri'] = serializers.serialize("json", urilogs)

    reslogs = Log.objects.filter(response__iregex=keyword)
    retjs['response'] = serializers.serialize("json", reslogs)

    return JsonResponse(retjs)


def filter(requests):
    logs = None
    if 'ip' in requests.GET:
        ip = requests.GET['ip']
        logs = Log.objects.filter(attackip=ip)
    elif "uri" in requests.GET:
        uri = requests.GET['uri']
        logs = Log.objects.filter(uri__iregex=uri)

    retlogs = serializers.serialize("json", logs)
    return HttpResponse(retlogs, content_type="application/json")


def statistics(requests):
    pass