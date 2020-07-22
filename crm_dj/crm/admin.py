from django.contrib import admin

# Register your models here.

from .models import Relation, Region, Account, Contact, Project
admin.site.register(Relation)
admin.site.register(Region)
admin.site.register(Account)
admin.site.register(Contact)
admin.site.register(Project)
