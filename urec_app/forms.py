from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.forms import UserChangeForm
from .models import *
from django.forms import modelformset_factory, TextInput, EmailInput, NumberInput, Textarea, SelectMultiple

from django.contrib.auth import get_user_model


# Report Forms


# Generic Report Form for Injury/Illness and Incident Forms
class UrecReportForm(forms.ModelForm):
    class Meta:
        model = UrecReport
        fields = ["location", "severity", "ems_called", "police_called"]


# Injury/Illness Report Form
class InjuryIllnessReportForm(UrecReportForm):
    class Meta(UrecReportForm.Meta):
        model = InjuryIllnessReport
        fields = UrecReportForm.Meta.fields + ["activity_causing_injury"]
        widgets={
        'activity_causing_injury' : TextInput(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 300px;',
            'placeholder' : 'How did the injury occur?'
        })}


# Incident Report Form
class IncidentReportForm(UrecReportForm):
    class Meta(UrecReportForm.Meta):
        model = IncidentReport
        fields = UrecReportForm.Meta.fields + ["activity_during_incident"]
        widgets={
        'activity_during_incident' : TextInput(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 300px;',
            'placeholder' : 'How did the incident occur?'
        })}


# Report Specific Formsets


# Generic Report Specific Formset for Generic UREC Report
urec_report_specific_formset = modelformset_factory(
    UrecReportSpecific, fields=(), extra=1
)


# Injury Formset for Injury/Illness Report
injury_illness_report_injury_formset = modelformset_factory(
    InjuryIllnessReportInjury, fields=('injury_type', 'injury_description', 'care_provided'), extra=1,
    widgets={
        'injury_type' : TextInput(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 300px;',
            'placeholder' : 'Injury Type',
        }),
        'injury_description' : Textarea(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 500px;',
            'placeholder' : 'Describe the Injury',
        }),
        'care_provided' : TextInput(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 300px;',
            'placeholder' : 'Care Provided',
    }),
    }
    
)


# Incident Formset for Incident Report
incident_report_incident_formset = modelformset_factory(
    IncidentReportIncident, fields=('incident_nature', 'incident_description', 'action_taken'), extra=1,
    widgets={
        'incident_nature' : TextInput(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 300px;',
            'placeholder' : 'Incident',
        }),
        'incident_description' : Textarea(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 500px;',
            'placeholder' : 'Describe the Incident',
        }),
        'action_taken' : TextInput(attrs={
            'class' : 'form-control',
            'style' : 'max-width: 300px;',
            'placeholder' : 'Actions Taken',
    }),
    }
    
)


# Report Contact Forms


# Generic Contact Form for Injury/Illness and Incident Patient Contacts
class UrecContactForm(forms.ModelForm):
    class Meta:
        model = UrecContact
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]
        widgets={
            'first_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'First Name',
            }),
            'middle_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Middle Name'
            }),
            'last_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Last Name'
            }),
            'email_address': EmailInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Email Address'
            }),
            'personal_phone_number': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Personal Phone Number'
            }),
            'home_phone_number': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Home Phone Number'
            }),
            'street_address': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Street Address'
            }),
            'city': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'City'
            }),
            'state': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'State'
            }),
            'zip': NumberInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Zip Code'
            }),
            'minor_status': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Minor Status'
            }),

        }


# Patient Contact Information Form for Injury/Illness Report
class InjuryIllnessReportContactPatientForm(UrecContactForm):
    class Meta(UrecContactForm.Meta):
        model = InjuryIllnessReportContactPatient


# Patient Contact Information Form for Incident Report
class IncidentReportContactPatientForm(UrecContactForm):
    class Meta(UrecContactForm.Meta):
        model = IncidentReportContactPatient


# Report Witness Contact Formsets


# Generic Formset Generator Function for Injury/Illness and Incident Witness Contacts
def create_urec_contact_formset(model):
    return modelformset_factory(
        model, fields=("first_name", "middle_name", "last_name", "email_address",
                       "personal_phone_number", "home_phone_number", "street_address",
                       "city", "state", "zip", "minor_status"), extra=1,
        widgets={
            'first_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'First Name',
            }),
            'middle_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Middle Name'
            }),
            'last_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Last Name'
            }),
            'email_address': EmailInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Email Address'
            }),
            'personal_phone_number': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Personal Phone Number'
            }),
            'home_phone_number': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Home Phone Number'
            }),
            'street_address': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Street Address'
            }),
            'city': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'City'
            }),
            'state': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'State'
            }),
            'zip': NumberInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Zip Code'
            }),
            'minor_status': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 300px;',
                'placeholder' : 'Minor Status'
            }),

        }
    )


# Generic Contact Information Formset for Generic UREC Report
urec_contact_formset = create_urec_contact_formset(UrecContact)


# Witness Contact Information Formset for Injury/Illness Report
injury_illness_report_contact_witness_formset = create_urec_contact_formset(InjuryIllnessReportContactWitness)


# Witness Contact Information Formset for Incident Report
incident_report_contact_witness_formset = create_urec_contact_formset(IncidentReportContactWitness)


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
    Count, fields=("location", "location_count"), extra=4
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
