from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

#provide a one off default value for the created field
#default_created_value = timezone.now()

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tittle = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tittle

    class Meta:
        ordering = ['complete']



