from django.urls import path, include
from django.contrib import admin
from . import views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.home, name='home'),


    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/edit', views.edit_account, name="edit"),


    path('accident/', views.accident, name='accident'),
    path('accident/create_accident_ticket/', views.CreateAccidentTicket.as_view(), name='create_accident_ticket'),
    path('accident/view_accident_tickets/', views.view_accident_tickets, name='view_accident_tickets'),
    path('accident/edit_accident_id/', views.edit_accident_id, name='edit_accident_id'),
    path('accident/delete/<str:accidentid>', views.delete_accident, name='delete_accident'),


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
    path('incident/view_incident_id/', views.view_incident_id, name='view_incident_id'),
    path('incident/delete/<str:incidentid>', views.delete_incident, name='delete_incident'),


    path('task/', views.task, name='task'),
    path('task/create_task', views.create_task, name='create_task'),
    path('task/my_tasks', views.my_tasks, name='my_tasks'),
    path('task/all_tasks', views.all_tasks, name='all_tasks'),
    path('task/view_task_id', views.view_task_id, name='view_task_id'),
    path('task/delete/<str:taskid>', views.delete_task, name='delete_task'),


    path('sop/', views.sop, name='sop'),


    path('survey/', views.survey, name='survey'),


    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catalog'),
]

# Low-Level Features to Add:
# Formset for submitting multiple form entries - Add row
#       https://www.brennantymrak.com/articles/django-dynamic-formsets-javascript
# Formset in Tasks for editing and submitting incomplete tasks if bool == 0
# Django Interactive Table / Interactive View