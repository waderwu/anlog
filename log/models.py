import json
from django.db import models

# Create your models here.


class Log(models.Model):
    attackip = models.CharField(max_length=20)
    attacktime = models.DateTimeField()
    method = models.CharField(max_length=10)
    uri = models.TextField()
    headers = models.TextField()
    data = models.TextField()

    def attacktype(self):
        return "rce"

    def replay(self):
        uri = self.uri
        headers = json.loads(self.headers)
        data = self.data
        host = headers['host']
        headers = str(headers)
        method = self.method

        with open("replay", "r") as f:
            script = f.read()

        script = script.replace("{uri}", uri)

        script = script.replace("{headers}", headers)

        script = script.replace("{data}", data)

        script = script.replace("{host}", host)

        script = script.replace("{method}", method)

        return script
