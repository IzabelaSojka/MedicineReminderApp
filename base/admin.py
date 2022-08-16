from django.contrib import admin
from .models import Medicine
from .models import Medicine_Database
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class MedicineResource(resources.ModelResource):

    class Meta:
        model = Medicine_Database
        skip_unchanged = True
        report_skipped = False

class MedicineAdmin(ImportExportModelAdmin):
    resource_class = MedicineResource

admin.site.register(Medicine)
admin.site.register(Medicine_Database, MedicineAdmin)
