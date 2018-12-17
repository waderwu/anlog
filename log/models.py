from django.db import models
import json
import base64
# Create your models here.


class Log(models.Model):
    uid = models.CharField(max_length=40)
    attackip = models.CharField(max_length=20)
    attacktime = models.DateTimeField()
    method = models.CharField(max_length=10)
    path = models.TextField()
    headers = models.TextField()
    post = models.TextField()
    get = models.TextField()
    attacktype = models.TextField()
    file = models.TextField()
    response = models.TextField(default='')
    success = models.BooleanField(default=False)



    def replay(self):
        path = self.path
        headers = self.headers
        post = self.post
        get = self.get
        method = self.method
        tmpfiles = json.loads(self.file.replace("\'", "\""))
        files = []
        for tmpf in tmpfiles:
            if 'type' not in tmpf:
                tmpf['type'] = 'text/html'
            tmpfile = (tmpf['name'], (tmpf['filename'], base64.b64decode(tmpf['content']), tmpf['type']))
            files.append(tmpfile)
        files = str(files)


        with open("./log/replay", "r") as f:
            script = f.read()

        script = script.replace("{path}", path)
        script = script.replace("{headers}", headers)
        script = script.replace("{data}", post)
        script = script.replace("{params}", get)
        script = script.replace("{method}", method)
        script = script.replace("{files}", files)

        return script
