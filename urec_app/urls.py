from django.urls import path, include
from django.contrib import admin
from . import views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.home, name='home'),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accident/', views.accident, name='accident'),
    path('accident/create_accident_ticket/', views.CreateAccidentTicket.as_view(), name='create_accident_ticket'),
    path('accident/view_accident_tickets/', views.view_accident_tickets, name='view_accident_tickets'),

    # path('accident/test/', views.showform5, name='form'),

    path('count/', views.count, name='count'),
    path('count/update', views.count_update, name='count_update'),
    path('count/view_history', views.count_view_history, name='count_view_history'),

    path('erp/', views.erp, name='erp'),
    path('erp/create_erp', views.create_erp, name='create_erp'),
    path('erp/view_erps', views.view_erps, name='view_erps'),
    path('erp/delete/<str:filename>', views.delete_erp, name='delete_erp'),
    path('erp/download/<str:filename>', views.download_erp, name='download_erp'),



    path('form/', views.form, name='form'),

    path('incident/', views.incident, name='incident'),
    path('incident/create_incident_ticket/', views.CreateIncidentTicket.as_view(), name='create_incident_ticket'),
    path('incident/view_incident_tickets/', views.view_incident_tickets, name='view_incident_tickets'),

    path('sop/', views.sop, name='sop'),
    path('survey/', views.survey, name='survey'),

    path('task/', views.task, name='task'),
    path('task/create_task', views.create_task, name='create_task'),
    # path('task/task_list', views.task, name='task'),
    path('task/all_tasks', views.all_tasks, name='all_tasks'),

    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catalog'),
]

# Low-Level Features to Add:
# Formset for submitting multiple form entries - Add row
#       https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript
# Formset in Tasks for editing and submitting incomplete tasks if bool == 0
# Django Interactive Table / Interactive View