from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # silence PyCharm CE inspection errors
    objects = models.Manager()

    def __str__(self):
        return self.title
