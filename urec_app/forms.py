from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.forms import UserChangeForm
from .models import *
from django.forms import modelformset_factory

from django.contrib.auth import get_user_model


class InjuryIllnessReportForm(forms.ModelForm):
    class Meta:
        model = InjuryIllnessReport
        fields = ["urec_facility", "location_in_facility", "activity_causing_injury"]


injury_illness_report_injury_formset = modelformset_factory(
    InjuryIllnessReportInjury, fields=('injury_type', 'injury_description', 'care_provided'), extra=1
)


class InjuryIllnessReportContactPatientForm(forms.ModelForm):
    class Meta:
        model = InjuryIllnessReportContactPatient
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]


injury_illness_report_witness_contact_formset = modelformset_factory(
    InjuryIllnessReportContactWitness, fields=("first_name", "middle_name", "last_name", "email_address",
                                               "personal_phone_number", "home_phone_number", "street_address",
                                               "city", "state", "zip", "minor_status"), extra=1
)


class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ["urec_facility", "location_in_facility", "activity_during_incident"]


incident_report_incident_formset = modelformset_factory(
    IncidentReportIncident, fields=('incident_nature', 'incident_description', 'action_taken'), extra=1
)


class IncidentReportContactPatientForm(forms.ModelForm):
    class Meta:
        model = IncidentReportContactPatient
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]


incident_report_witness_formset = modelformset_factory(
    IncidentReportContactWitness, fields=("first_name", "middle_name", "last_name", "email_address",
                                          "personal_phone_number", "home_phone_number", "street_address", "city",
                                          "state", "zip", "minor_status"), extra=1
)


class TaskForm(forms.ModelForm):
    model = get_user_model()
    date_time_due = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    staff_netid = forms.ModelChoiceField(queryset=model.objects.all())

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


class ErpForm(forms.ModelForm):
    class Meta:
        model = Erp
        fields = ["title", "description"]


class ErpUploadForm(forms.ModelForm):
    class Meta:
        model = ErpUpload
        fields = ["file"]


class EditAccountForm(UserChangeForm):
    # Removes Password field from Edit Account Form
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'phone_number'
        )
