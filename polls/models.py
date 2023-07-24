from django.db import models


class Demo(models.Model):
    name = models.CharField(max_length=50)
    another_field = models.IntegerField(null=True, db_index=True)


