from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# from django.utils.safestring import mark_safe
from .models import Log
import requests as rq
import json
from datetime import datetime

# Create your views here.


def index(requests):
    log_list = Log.objects.all()
    paginator = Paginator(log_list, 3)

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
        # item['pageHtml'] = mark_safe(log.response)
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

    log_list = None

    if "keyword" in requests.GET:
        keyword = requests.GET['keyword']
        log_list = Log.objects.filter(Q(headers__iregex=keyword)|Q(post__iregex=keyword)|Q(get__iregex=keyword)|Q(response__iregex=keyword))

    if "ip" in requests.GET:
        ip = requests.GET['ip']
        if log_list:
            log_list = log_list.objects.filter(attackip=ip)
        else:
            log_list = Log.objects.filter(attackip=ip)

    if "method" in requests.GET:
        method = requests.GET['method']
        if log_list:
            log_list = log_list.filter(method=method)
        else:
            log_list = Log.objects.filter(method=method)

    if "post" in requests.GET:
        post = requests.GET['post']
        if log_list:
            log_list = log_list.filter(post__iregex=post)
        else:
            log_list = Log.objects.filter(post__iregex=post)

    if "get" in requests.GET:
        get = requests.GET['get']
        if log_list:
            log_list = log_list.filter(get__iregex=get)
        else:
            log_list = Log.objects.filter(get__iregex=get)

    # retjs = {}
    # retjs['attackip'] = serializers.serialize("json", attackiplogs)
    #
    # headerslogs = Log.objects.filter(headers__iregex=keyword)
    # retjs['headers'] = serializers.serialize("json", headerslogs)
    #
    # postlogs = Log.objects.filter(post__iregex=keyword)
    # retjs['post'] = serializers.serialize("json", postlogs)
    #
    # getlogs = Log.objects.filter(get__iregex=keyword)
    # retjs['get'] = serializers.serialize("json", getlogs)
    #
    # reslogs = Log.objects.filter(response__iregex=keyword)
    # retjs['response'] = serializers.serialize("json", reslogs)

    # print(JsonResponse(retjs))
    # return JsonResponse(retjs)
    paginator = Paginator(log_list, 3)

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
        # item['pageHtml'] = mark_safe(log.response)
        dicts.append(item)

    return render(requests, "index.html", {'contents': dicts, 'page_info': page_info})


def filter(requests):
    logs = None
    if 'ip' in requests.GET:
        ip = requests.GET['ip']
        logs = Log.objects.filter(attackip=ip)
    elif "path" in requests.GET:
        path = requests.GET['path']
        logs = Log.objects.filter(path__iregex=path)

    retlogs = serializers.serialize("json", logs)
    return HttpResponse(retlogs, content_type="application/json")


def statistics(requests):
    pass