from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import UserCreation
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect

class ResearcherSite(AdminSite):
    site_header = 'Researcher Site'  
    site_title = 'Researcher Site'
    def logout(self, request):
        logout(request)
        return redirect(reverse('index'))
    
researcher_site = ResearcherSite(name='researcher')


admin.site.site_header = 'Super Admin Site'
admin.site.site_title = 'Super Admin Site'

researcher_site.register(UserCreation)
admin.site.register(UserCreation)
