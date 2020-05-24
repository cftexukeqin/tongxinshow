from django.db import models

# Create your models here.


class Data(models.Model):
    name = models.CharField(max_length=300,default="")
    year = models.CharField(max_length=4,default="")
    jidu_1 = models.FloatField(default=0)
    jidu_2 = models.FloatField(default=0)
    jidu_3 = models.FloatField(default=0)
    jidu_4 = models.FloatField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-add_time"]
