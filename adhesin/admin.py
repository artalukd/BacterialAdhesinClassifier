# Register your models here.
from django.contrib import admin

from .models import ProteinData, FileData,FASTA,user_details

admin.site.register(ProteinData)
admin.site.register(FileData)
admin.site.register(FASTA)
admin.site.register(user_details)
