from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


# Register your models here.


class UrecUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UrecUser


class UrecUserAdmin(UserAdmin):
    form = UrecUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )


admin.site.register(UrecUser, UrecUserAdmin)


admin.site.register(UrecFacility)
admin.site.register(UrecLocation)
admin.site.register(Count)


class InjuryIllnessReportContactPatientInline(admin.StackedInline):
    model = InjuryIllnessReportContactPatient
    extra = 0
    max_num = 1
    can_delete = False


class InjuryIllnessReportContactWitnessInline(admin.StackedInline):
    model = InjuryIllnessReportContactWitness
    extra = 0


class InjuryIllnessReportInjuryInline(admin.StackedInline):
    model = InjuryIllnessReportInjury
    extra = 0


class InjuryIllnessReportAdmin(admin.ModelAdmin):
    inlines = [InjuryIllnessReportContactPatientInline, InjuryIllnessReportInjuryInline,
               InjuryIllnessReportContactWitnessInline]


admin.site.register(InjuryIllnessReport, InjuryIllnessReportAdmin)


class IncidentReportContactPatientInline(admin.StackedInline):
    model = IncidentReportContactPatient
    extra = 0
    max_num = 1
    can_delete = False


class IncidentReportContactWitnessInline(admin.StackedInline):
    model = IncidentReportContactWitness
    extra = 0


class IncidentReportIncidentInline(admin.StackedInline):
    model = IncidentReportIncident
    extra = 0


class IncidentReportAdmin(admin.ModelAdmin):
    inlines = [IncidentReportContactPatientInline, IncidentReportIncidentInline,
               IncidentReportContactWitnessInline]


admin.site.register(IncidentReport, IncidentReportAdmin)
