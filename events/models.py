from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Events(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255, default=' ')
    type = models.CharField(max_length=50, default=' ')
    description = models.CharField(max_length=255, default=' ')
    city = models.CharField(max_length=100, default=' ')
    address = models.CharField(max_length=100, default=' ')
    price = models.IntegerField(default=0)
    date = models.CharField(max_length=100, default=' ')
    time = models.CharField(max_length=100, default=' ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=255, default='https://www.inform.kz/fotoarticles/20160424104954.jpg')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events_admin")
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return smart_unicode(self.name)
