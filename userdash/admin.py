from django.contrib import admin

from models import VcloudUserToken
from models import VcloudUserInstances


# Register your models here.
class VcloudUserInstanceAdmin(admin.ModelAdmin):
    pass


class VcloudUserTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(VcloudUserInstances, VcloudUserInstanceAdmin)
admin.site.register(VcloudUserToken, VcloudUserTokenAdmin)


