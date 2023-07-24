from django.db import models


class Demo(models.Model):
    name = models.CharField(max_length=50)
    another_field = models.IntegerField(db_index=True)


