from django.contrib.admin.apps import AdminConfig


class UrecAdminConfig(AdminConfig):
    default_site = "urec.admin.UrecAdminSite"
