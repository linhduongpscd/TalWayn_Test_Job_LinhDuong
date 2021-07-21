from django.db import models

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    status = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["id"]