from django.contrib import admin
from people.models import PythonFrameWorks


class PythonFrameWorksAdmin(admin.ModelAdmin):
    pass
admin.site.register(PythonFrameWorks, PythonFrameWorksAdmin)
