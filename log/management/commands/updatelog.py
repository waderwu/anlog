import requests as rq
import json
import schedule
import time
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from log.models import Log
from log.plugin.attack import Attack


class Command(BaseCommand):
    help = 'update log'

    def handle(self, *args, **options):
        schedule.every(10).seconds.do(self.insertlog)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def insertlog(self):
        url = "http://u.cn/logser.php"
        r = rq.get(url)
        jsonr = json.loads(r.text)
        # print(jsonr)
        attack = Attack()
        for key in jsonr:
            jlog = json.loads(jsonr[key])
            ip = jlog['ip']
            time = datetime.strptime(jlog['time'], "%Y-%m-%d %H:%M:%S")
            method = jlog['method'].lower()
            response = jlog['response']
            attack_type = []
            if jlog['post']:
                for p in jlog['post']:
                    kind = attack.is_attack(jlog['post'][p])
                    if kind:
                        attack_type.append(kind)

            if jlog['get']:
                for g in jlog['get']:
                    kind = attack.is_attack(jlog['get'][g])
                    if kind:
                        attack_type.append(kind)

            log = Log(attackip=ip, attacktime=time, method=method, path=jlog['path'], headers=jlog['headers'],
                      post=jlog['post'], get=jlog['get'], response=response, attacktype=str(attack_type))
            log.save()

            self.stdout.write(self.style.SUCCESS('Successfully insert log "%s" attack type: %s' % (ip, str(attack_type))))