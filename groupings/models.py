from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text as smart_unicode
from django.core.exceptions import ValidationError


# Create your models here.
class Grouping(models.Model):
    class Meta:
        app_label = 'groupings'

    title = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.CharField( max_length=100)
    time = models.CharField( max_length=100)
    min_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    members = models.ManyToManyField(User, through='Membership', related_name="members")

    def __str__(self):
        return self.title


class Membership(models.Model):
    ROLE_CHOICE = (
        ('1', 'Admin'),
        ('2', 'Member'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grouping = models.ForeignKey(Grouping, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(choices=ROLE_CHOICE, default='2', max_length=1)