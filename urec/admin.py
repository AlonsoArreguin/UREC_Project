from django.contrib import admin


class UrecAdminSite(admin.AdminSite):
    site_header = 'UREC Risk Management System'
    site_title = 'UREC Risk Management System'
    index_title = 'UREC Risk Management System'


urec_admin_site = UrecAdminSite(name='urec_admin')
