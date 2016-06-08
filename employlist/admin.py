from django.contrib import admin

from .models import Department, Employee

# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    pass

class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal info', {'fields': ['first_name', 'last_name', 'patronymic', 'birth_date', 'phone', 'email']}),
        ('Employee info', {'fields': ['employ_date', 'dismiss_date', 'department', 'position']}),
    ]
    list_display = ('get_name_with_position', 'is_employed_now')
    list_filter  = ('department',)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
