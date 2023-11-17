from django.db import models

class QueryResult(models.Model):
    cadastre_number = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    response = models.BooleanField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)