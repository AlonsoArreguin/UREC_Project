from django.urls import path, include
from . import views
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/edit', views.edit_account, name="edit"),

    path('injury/', views.injury_illness, name='injury_illness'),
    path('injury/create_injury_report/', views.CreateInjuryIllnessReport.as_view(), name='create_injury_illness_report'),
    path('injury/view_injury_reports/', views.view_injury_illness_reports, name='view_injury_illness_reports'),
    path('injury/edit_injury/', views.edit_injury_illness, name='edit_injury_illness'),
    path('injury/delete/<str:injury_illness_id>', views.delete_injury_illness, name='delete_injury_illness'),

    path('count/', views.count, name='count'),
    path('count/update', views.count_update, name='count_update'),
    path('count/view_history', views.count_view_history, name='count_view_history'),
    path('count/count_hourly', views.count_hourly, name="count_hourly"),
    path('count/delete/<str:count_id>', views.delete_count, name='delete_count'),

    path('erp/', views.erp, name='erp'),
    path('erp/create_erp', views.create_erp, name='create_erp'),
    path('erp/view_erps', views.view_erps, name='view_erps'),
    path('erp/delete/<str:filename>', views.delete_erp, name='delete_erp'),
    path('erp/download/<str:filename>', views.download_erp, name='download_erp'),

    path('form/', views.form, name='form'),

    path('incident/', views.incident, name='incident'),
    path('incident/create_incident_report/', views.CreateIncidentReport.as_view(), name='create_incident_report'),
    path('incident/view_incident_reports/', views.view_incident_reports, name='view_incident_reports'),
    path('incident/view_incident/', views.view_incident_id, name='view_incident'),
    path('incident/delete/<str:incident_id>', views.delete_incident, name='delete_incident'),

    path('task/', views.task, name='task'),
    path('task/create_task', views.create_task, name='create_task'),
    path('task/my_tasks', views.my_tasks, name='my_tasks'),
    path('task/all_tasks', views.all_tasks, name='all_tasks'),
    path('task/view_task_id', views.view_task_id, name='view_task_id'),
    path('task/view_my_task', views.view_my_task, name='view_my_task'),
    path('task/delete/<str:taskid>', views.delete_task, name='delete_task'),
    path('task/complete/<str:taskid>', views.complete_task, name='complete_task'),

    path('sop/', views.sop, name='sop'),

    path('survey/', views.survey, name='survey'),

    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catalog'),


]
