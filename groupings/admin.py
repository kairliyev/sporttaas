from django.contrib import admin
from groupings.models import Grouping, Membership, Coordinate
# Register your models here.
admin.site.register(Grouping)
admin.site.register(Membership)
admin.site.register(Coordinate)