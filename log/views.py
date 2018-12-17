from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Log
from django.db.models import Count
from datetime import timedelta
import base64
import ast


# Create your views here.

def debug(var):
    print(type(var))
    print(var)

def index(requests):
    log_list = Log.objects.all()

    # IP statistic
    ip_addrs = set(log_list.values_list("attackip"))
    ip_info = {}
    for ip in ip_addrs:
        ip_info[ip[0]] = {}
        visited_log = log_list.filter(attackip=ip[0])
        ip_info[ip[0]]['visit_num'] = len(visited_log)
        ip_info[ip[0]]['attack_num'] = len(visited_log.exclude(attacktype="[]"))

    # attacking number statistic
    log_sorted_by_time = log_list.order_by("-attacktime")
    previous_min = log_sorted_by_time[0].attacktime.replace(second=0)
    after_min = previous_min + timedelta(minutes=1)
    visit_nums = []
    min_point = []
    for i in range(11):
        visit_nums.append(len(log_sorted_by_time.filter(attacktime__range=(previous_min, after_min))))
        min_point.append(str(previous_min))
        after_min = previous_min
        previous_min = previous_min - timedelta(minutes=1)

    return render(requests, "index.html",
                  {'ip_info': ip_info, 'visit_nums': visit_nums, 'min_stamp': min_point})



def replay(requests):
    logid = [int(i) for i in requests.GET.getlist('id[]')]
    logs = Log.objects.filter(pk__in=logid)
    replays = []
    for log in logs:
        replays.append(log.replay())
    return render(requests, "replay.html", {'scripts': replays})


def show(requests):
    log_list = Log.objects.all()

    paginator = Paginator(log_list.order_by("-attacktime"), 20)

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
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    for log in logs:
        item = {}
        item['index'] = log.pk
        item['attackip'] = log.attackip
        item['attacktime'] = log.attacktime
        item['method'] = log.method
        item['path'] = log.path
        item['headers'] = log.headers
        item['post'] = log.post.strip('[').strip(']')
        item['get'] = log.get.strip('[').strip(']')
        item['response'] = log.response
        item['files'] = []
        files = ast.literal_eval(log.file)
        for file_json in files:
            tmpitem = {}
            filetype = is_binary_string(base64.b64decode(file_json['content']))
            tmpitem['name'] = file_json['name']
            tmpitem['filename'] = file_json['filename']
            tmpitem['content'] = base64.b64decode(file_json['content'])
            tmpitem['binary'] = filetype
            item['files'].append(tmpitem)
        # print(item['files'])

        item['attacktype'] = log.attacktype.strip('[').strip(']').replace(' ', '').replace("\'", '').split(',')
        item['success'] = log.success
        dicts.append(item)

    return render(requests, "show.html", {'contents': dicts, 'page_info': page_info})


def search(requests):

    log_list = 'filler'
    print(requests.GET)

    if "keyword" in requests.GET:
        keyword = requests.GET['keyword']
        log_list = Log.objects.filter(Q(headers__icontains=keyword)|Q(post__icontains=keyword)|Q(get__icontains=keyword)|Q(response__icontains=keyword))

    if "ip" in requests.GET:
        if requests.GET['ip'] != '':
            ip = requests.GET['ip']
            if log_list != 'filler':
                log_list = log_list.filter(attackip=ip)
            else:
                log_list = Log.objects.filter(attackip=ip)
    if 'path' in requests.GET:
        if requests.GET['path'] != '':
            path = requests.GET['path']
            if log_list != 'filler':
                log_list = log_list.filter(path__icontains=path)
            else:
                log_list = Log.objects.filter(path__icontains=path)

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

    paginator = Paginator(log_list.order_by("-attacktime"), 20)

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
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    for i, log in enumerate(logs):
        item = {}
        item['index'] = log.pk
        item['attackip'] = log.attackip
        item['attacktime'] = log.attacktime
        item['method'] = log.method
        item['path'] = log.path
        item['headers'] = log.headers
        item['post'] = log.post.strip('[').strip(']')
        item['get'] = log.get.strip('[').strip(']')
        item['response'] = log.response
        item['files'] = []
        files = ast.literal_eval(log.file)
        for file_json in files:
            tmpitem = {}
            filetype = is_binary_string(base64.b64decode(file_json['content']))
            tmpitem['name'] = file_json['name']
            tmpitem['filename'] = file_json['filename']
            tmpitem['content'] = base64.b64decode(file_json['content'])
            tmpitem['binary'] = filetype
            item['files'].append(tmpitem)
        # print(item['files'])

        item['attacktype'] = log.attacktype.strip('[').strip(']').replace(' ', '').replace("\'", '').split(',')
        item['success'] = log.success
        dicts.append(item)

    return render(requests, "show.html", {'contents': dicts, 'page_info': page_info})


def statistics(requests):
    ips = Log.objects.values_list("attackip", flat=True).distinct()
    #list all different ip
    for ip in ips:
        print(ip)


    #ervery ip attack count
    ipcounts = Log.objects.values('attackip').annotate(count=Count('attackip')).order_by('-count')
    for ipcount in ipcounts:
        debug(ipcount)

    #every ip attack success count
    sucounts = Log.objects.filter(~Q(attacktype='[]')).values('attackip').annotate(count=Count('attackip')).order_by('-count')

    for succount in sucounts:
        debug(succount)

    #ervery path count
    pathcounts = Log.objects.values('path').annotate(count=Count('attackip')).order_by('-count')
    for path in pathcounts:
        debug(path)

    # print(ipcounts[0].attackip__count)

    return HttpResponse("ok")