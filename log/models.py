from django.db import models

# Create your models here.


class Log(models.Model):
    attackip = models.CharField(max_length=20)
    attacktime = models.DateTimeField()
    method = models.CharField(max_length=10)
    path = models.TextField()
    headers = models.TextField()
    post = models.TextField()
    get = models.TextField()
    attacktype = models.TextField()
    response = models.TextField()


    def replay(self):
        path = self.path
        headers = self.headers
        post = self.post
        get = self.get
        method = self.method

        with open("./log/replay", "r") as f:
            script = f.read()

        script = script.replace("{path}", path)
        script = script.replace("{headers}", headers)
        script = script.replace("{data}", post)
        script = script.replace("{params}", get)
        script = script.replace("{method}", method)

        return script
