from django.db import models

class JobLock(models.Model):
    name = models.CharField(max_length=100, unique=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
