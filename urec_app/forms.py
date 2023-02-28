from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from .models import *
from django.forms import modelformset_factory

class FormAccident(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ["staff_netid", "accident_type", "accident_description",
                  "first_name", "last_name", "phone_number"]

class AccidentTicketForm(forms.ModelForm):
    class Meta:
        model = AccidentTicket
        fields = ["urec_facility", "location_in_facility", "activity_causing_injury",
                  "injury_type", "injury_description"]

class AccidentTicketContactInfoForm(forms.ModelForm):
    class Meta:
        model = AccidentTicketContactInfo
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", ]
        # exclude = ('accident_ticket', 'accident_relation',)

class Accident_Ticket_Form(forms.ModelForm):
    class Meta:
        model = Accident_Ticket
        fields = ["urec_facility", "location_in_facility", "activity_causing_injury"]

# Accident Ticket Injury Form
# class Accident_Ticket_Injury_Form(forms.ModelForm):
#     class Meta:
#         model = Accident_Ticket_Injury
#         fields = ["injury_type", "injury_description", "care_provided"]


AccidentTicketInjury = modelformset_factory(
    Accident_Ticket_Injury, fields=('injury_type', 'injury_description', 'care_provided'), extra=1
)

class Accident_Ticket_Contact_Info_Form(forms.ModelForm):
    class Meta:
        model = Accident_Ticket_Contact_Info
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip"]

class Incident_Ticket_Form(forms.ModelForm):
    class Meta:
        model = Incident_Ticket
        fields = ["urec_facility", "location_in_facility", "activity_during_incident"]

class Incident_Ticket_Incident_Form(forms.ModelForm):
    class Meta:
        model = Incident_Ticket_Incident
        fields = ["incident_nature", "incident_description", "action_taken"]

class Incident_Ticket_Contact_Info_Form(forms.ModelForm):
    class Meta:
        model = Incident_Ticket_Contact_Info
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]

class Task_Form(forms.ModelForm):
    date_time_due = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    class Meta:
        model = Task
        fields = ["task_name", "task_description", "date_time_due", "text_input_required"]
        widgets = {
            "date": AdminDateWidget(),
            "time": AdminTimeWidget()
        }

# class Date_Time_Form(forms.Form):
#     date_time = forms.DateField(widget=AdminSplitDateTime)

CountFormSet = forms.modelformset_factory(
    Count, fields=("location_in_facility", "location_count"), extra=4
)