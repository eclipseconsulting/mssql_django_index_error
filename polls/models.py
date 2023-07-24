from django.db import models


class Demo(models.Model):
    name = models.CharField(max_length=50)
    another_field = models.IntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'another_field'], name='my_custom_index')
        ]
