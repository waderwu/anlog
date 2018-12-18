import requests as rq
import json
import schedule
import time
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from log.models import Log
from log.plugin.attack import Attack
import ast

class Command(BaseCommand):
    help = 'update log'

    def handle(self, *args, **options):
        self.host = "http://u.cn/"
        schedule.every(10).seconds.do(self.insertlog)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def insertlog(self):
        try:
            self.insertreq()
        except Exception as e:
            print("EXception", e)

        try:
            self.insertres()
        except Exception as e:
            print("Exception", e)


    def insertreq(self):
        url = self.host + "wulogser.php?dir=req"
        r = rq.get(url)
        print(r.text)
        jsonr = r.json()
        print(jsonr)
        attack = Attack()
        for key in jsonr:
            jlog = json.loads(jsonr[key])
            ip = jlog['ip']
            time = datetime.strptime(jlog['time'], "%Y-%m-%d %H:%M:%S")
            method = jlog['method'].lower()
            attack_type = []

            if jlog['post']:
                for p in jlog['post']:
                    kind = attack.is_attack(jlog['post'][p])
                    if kind:
                        attack_type.append(kind)

            if jlog['get']:
                for g in jlog['get']:
                    print("here")
                    kind = attack.is_attack(jlog['get'][g])
                    if kind:
                        attack_type.append(kind)

            log = Log(attackip=ip, attacktime=time, method=method, path=jlog['path'], headers=jlog['headers'],
                      post=jlog['post'], get=jlog['get'], uid=jlog['uid'], file=jlog['file'], attacktype=str(attack_type))
            log.save()

            self.stdout.write(self.style.SUCCESS('Successfully insert log "%s" attack type: %s' % (ip, str(attack_type))))


    def insertres(self):
        url = self.host + "wulogser.php?dir=res"
        r = rq.get(url)
        jsonr = r.json()
        print("hhh", jsonr)
        print(type(jsonr))
        for key in jsonr:
            print(key)
            jlog = json.loads(jsonr[key])
            print(jlog)
            uid = jlog['uid']
            response = jlog['res']
            attack = jlog['attack']

            log = Log.objects.get(uid=uid)
            print(log.uid)
            if log:
                log.response = response
                log.success = attack
                log.save()
                if attack:
                    turl = self.host+"wuaddip.php"
                    data = {"p": "wsniubi", "pass": "ws666", "ip": log.attackip}
                    rq.post(turl, data=data)

            self.stdout.write(self.style.SUCCESS('Successfully insert res success: %s' % attack))