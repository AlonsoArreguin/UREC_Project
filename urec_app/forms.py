from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
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


AccidentTicketInjury = modelformset_factory(
    Accident_Ticket_Injury, fields=('injury_type', 'injury_description', 'care_provided'), extra=1
)


class Accident_Ticket_Contact_Patient_Form(forms.ModelForm):
    class Meta:
        model = Accident_Ticket_Contact_Patient
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip"]


class Accident_Ticket_Contact_Witness_Form(forms.ModelForm):
    class Meta:
        model = Accident_Ticket_Contact_Witness
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip"]


class Incident_Ticket_Form(forms.ModelForm):
    class Meta:
        model = Incident_Ticket
        fields = ["urec_facility", "location_in_facility", "activity_during_incident"]


IncidentTicketIncidentForm = modelformset_factory(
    Incident_Ticket_Incident, fields=('incident_nature', 'incident_description', 'action_taken'), extra=1
)


class Incident_Ticket_Contact_Patient_Form(forms.ModelForm):
    class Meta:
        model = Incident_Ticket_Contact_Patient
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]


class Incident_Ticket_Contact_Witness_Form(forms.ModelForm):
    class Meta:
        model = Incident_Ticket_Contact_Witness
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]


class Task_Form(forms.ModelForm):
    date_time_due = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    staff_netid = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Task
        fields = ["task_name", "task_description", "staff_netid", "date_time_due", "text_input_required"]
        widgets = {
            "date": AdminDateWidget(),
            "time": AdminTimeWidget()
        }


CountFormSet = forms.modelformset_factory(
    Count, fields=("location_in_facility", "location_count"), extra=4
)


class ERP_Form(forms.ModelForm):
    class Meta:
        model = Erp
        fields = ["title", "description"]


class ERP_Upload_Form(forms.ModelForm):
    class Meta:
        model = Erp_Upload
        fields = ["file"]


class EditAccountForm(UserChangeForm):
    # Removes Password field from Edit Account Form
    password = None

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'\
        )