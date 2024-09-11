from django.contrib import admin

# model
from entry_management.models import Entry

# Register your models here.
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    search_fields = ('=id', "name__contains", "email__contains")
    list_display = ('id', 'name', 'email', 'comments', 'created_at')
    ordering = ('-id',)
    list_per_page = 25

