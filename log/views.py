from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Log
from django.db.models import Count
from datetime import timedelta
from datetime import datetime
import pytz
from datetime import time
import numpy as np


# Create your views here.

def index(requests):
    log_list = Log.objects.all()
    ip_addrs = set(log_list.values_list("attackip"))
    ip_info = {}
    for ip in ip_addrs:
        ip_info[ip[0]] = {}
        visited_log = log_list.filter(attackip=ip[0])
        ip_info[ip[0]]['visit_num'] = len(visited_log)
        ip_info[ip[0]]['attack_num'] = len(visited_log.exclude(attacktype="[]"))

    log_sorted_by_time = log_list.order_by("-attacktime")
    latest_min = log_sorted_by_time[0].attacktime.timestamp() - (log_sorted_by_time[0].attacktime.timestamp() % 60)
    foremost_min = latest_min - 600
    after_min = int(latest_min) + 60
    previous_min = int(latest_min)
    visit_nums = []
    cnt = 0
    idx = 0
    min_stamp = []
    print(type(previous_min))
    while previous_min >= foremost_min:
        if previous_min < log_sorted_by_time[idx].attacktime.timestamp() <= after_min:
            cnt += 1
            idx += 1
        else:
            after_min, previous_min = previous_min, previous_min - 60
            visit_nums.append(cnt)
            print(cnt)
            min_stamp.append(datetime.utcfromtimestamp(previous_min).strftime("%m-%d %H:%M"))
            cnt = 0

    return render(requests, "index.html",
                  {'ip_info': ip_info, 'visit_nums': visit_nums, 'min_stamp': min_stamp})


def login(requests):
    return HttpResponse("hello man")


def replay(requests):
    logid = requests.GET['id[]']
    log = Log.objects.get(pk=logid)
    return HttpResponse(log.replay())


def show(requests):
    log_list = Log.objects.all()
    ip_addrs = set(log_list.values_list("attackip"))
    ip_info = {}
    for ip in ip_addrs:
        ip_info[ip[0]] = {}
        visited_log = log_list.filter(attackip=ip[0])
        ip_info[ip[0]]['visit_num'] = len(visited_log)
        ip_info[ip[0]]['attack_num'] = len(visited_log.exclude(attacktype="[]"))

    paginator = Paginator(log_list, 20)

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
    for log in logs:
        item = {}
        item['index'] = log.pk
        item['attackip'] = log.attackip
        item['attacktime'] = log.attacktime
        item['method'] = log.method
        item['path'] = log.path
        item['headers'] = log.headers
        item['post'] = log.post
        item['get'] = log.get
        item['response'] = log.response
        item['file'] = log.file
        item['attacktype'] = log.attacktype
        item['success'] = log.success
        dicts.append(item)

    return render(requests, "temp.html", {'contents': dicts, 'page_info': page_info})


def search(requests):

    log_list = 'filler'

    if "keyword" in requests.GET:
        keyword = requests.GET['keyword']
        log_list = Log.objects.filter(Q(headers__iregex=keyword)|Q(post__iregex=keyword)|Q(get__iregex=keyword)|Q(response__iregex=keyword))

    if "ip" in requests.GET:
        if requests.GET['ip'] != '':
            ip = requests.GET['ip']
            if log_list != 'filler':
                log_list = log_list.filter(attackip=ip)
            else:
                log_list = Log.objects.filter(attackip=ip)

    if "method" in requests.GET:
        if requests.GET['method'] != '':
            method = requests.GET['method']
            if log_list != 'filler':
                log_list = log_list.filter(method=method)
            else:
                log_list = Log.objects.filter(method=method)

    if "post" in requests.GET:
        if requests.GET['post'] != '':
            post = requests.GET['post']
            if log_list != 'filler':
                log_list = log_list.filter(post__iregex=post)
            else:
                log_list = Log.objects.filter(post__iregex=post)

    if "get" in requests.GET:
        if requests.GET['get'] != '':
            get = requests.GET['get']
            if log_list != 'filler':
                log_list = log_list.filter(get__iregex=get)
            else:
                log_list = Log.objects.filter(get__iregex=get)

    paginator = Paginator(log_list, 20)

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
        item['attacktype'] = log.attacktype
        # item['pageHtml'] = mark_safe(log.response)
        dicts.append(item)

    return render(requests, "temp.html", {'contents': dicts, 'page_info': page_info})


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
    ips = Log.objects.values_list("attackip", flat=True).distinct()
    #list all different ip
    for ip in ips:
        print(ip)

    

    #ervery ip attack count
    ipcounts = Log.objects.values('attackip').annotate(Count('attackip')).order_by()
    for ipcount in ipcounts:
        print(ipcount)

    #every ip attack success count
    sucounts = Log.objects.filter(~Q(attacktype='[]')).values('attackip').annotate(Count('attackip')).order_by()

    for succount in sucounts:
        print(succount)

    # print(ipcounts[0].attackip__count)

    return HttpResponse("ok")