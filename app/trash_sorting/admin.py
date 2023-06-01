from django.contrib import admin
import trash_sorting.models as app_models

# Register your models here.

admin.site.register(app_models.ContentType)
admin.site.register(app_models.Content)
admin.site.register(app_models.SortSystem)
admin.site.register(app_models.Bin)
admin.site.register(app_models.Address)