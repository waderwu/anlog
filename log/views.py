from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Log
from django.db.models import Count


# Create your views here.

def index(requests):

    return render(requests, "index.html")


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

    paginator = Paginator(log_list, 10)

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
        # item['pageHtml'] = mark_safe(log.response)
        dicts.append(item)

    return render(requests, "temp.html", {'contents': dicts, 'page_info': page_info, 'ip_info': ip_info})


def search(requests):

    log_list = 'ggg'

    if "keyword" in requests.GET:
        keyword = requests.GET['keyword']
        log_list = Log.objects.filter(Q(headers__iregex=keyword)|Q(post__iregex=keyword)|Q(get__iregex=keyword)|Q(response__iregex=keyword))

    print(type(log_list))
    if requests.GET['ip'] != '':
        ip = requests.GET['ip']
        if log_list !='ggg':
            log_list = log_list.filter(attackip=ip)
        else:
            log_list = Log.objects.filter(attackip=ip)

    if requests.GET['method'] != '':
        method = requests.GET['method']
        if log_list !='ggg':
            log_list = log_list.filter(method=method)
        else:
            log_list = Log.objects.filter(method=method)

    if requests.GET['post'] != '':
        post = requests.GET['post']
        if log_list !='ggg':
            log_list = log_list.filter(post__iregex=post)
        else:
            log_list = Log.objects.filter(post__iregex=post)

    if requests.GET['get'] != '':
        get = requests.GET['get']
        if log_list !='ggg':
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