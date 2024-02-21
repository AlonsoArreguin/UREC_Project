from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UrecUser)

admin.site.register(UrecFacility)
admin.site.register(UrecLocation)

admin.site.register(InjuryIllnessReport)
admin.site.register(InjuryIllnessReportInjury)
admin.site.register(InjuryIllnessReportContactPatient)
admin.site.register(InjuryIllnessReportContactWitness)

admin.site.register(IncidentReport)
admin.site.register(IncidentReportIncident)
admin.site.register(IncidentReportContactPatient)
admin.site.register(IncidentReportContactWitness)

admin.site.register(Count)
