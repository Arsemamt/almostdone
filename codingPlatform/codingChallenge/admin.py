from django.contrib import admin
from .models import Home,Contact,Course,QuesModel,About,ExerciseResult

admin.site.site_header="Coding Platform"

admin.site.register(Home)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','timestamp','message']
    list_filter = ['timestamp']
    search_fields = ('name',)

admin.site.register(Course)
admin.site.register(QuesModel)
admin.site.register(About)
admin.site.register(ExerciseResult)
