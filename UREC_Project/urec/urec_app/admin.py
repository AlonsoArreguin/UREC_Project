from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Accident)
admin.site.register(AccidentTicket)
admin.site.register(AccidentTicketContactInfo)

admin.site.register(Accident_Ticket)
admin.site.register(Accident_Ticket_Injury)
admin.site.register(Accident_Ticket_Contact_Patient)
admin.site.register(Accident_Ticket_Contact_Witness)

admin.site.register(Incident_Ticket)
admin.site.register(Incident_Ticket_Incident)
admin.site.register(Incident_Ticket_Contact_Patient)
admin.site.register(Incident_Ticket_Contact_Witness)