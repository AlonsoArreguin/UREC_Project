from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.forms import UserChangeForm
from .models import *
from django.forms import modelformset_factory, formset_factory, TextInput, EmailInput, NumberInput, Textarea, SelectMultiple

from django.contrib.auth import get_user_model

#Global Variable for contact widgets
CONTACT_WIDGETS = {
            'first_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'First Name',
            }),
            'middle_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Middle Name'
            }),
            'last_name': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Last Name'
            }),
            'email_address': EmailInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Email Address'
            }),
            'personal_phone_number': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Personal Phone Number',
                'maxlength' : '10',
            }),
            'home_phone_number': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Home Phone Number',
                'maxlength' : '10',
            }),
            'street_address': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Street Address'
            }),
            'city': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'City'
            }),
            'state': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'State'
            }),
            'zip': NumberInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Zip Code',
                'maxlength': '5', 
            }),
            'minor_status': TextInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
                'placeholder' : 'Minor Status'
            }),
}

#widget function for different injury/illness/incident fields
def type_widget(placeholder: str, max_width: str = '400px') -> TextInput:
    return TextInput(attrs={'class' : 'form-control',
            'style' : f'max-width:{max_width};',
            'placeholder' : f'{placeholder}'
        })

#widget function for different description fields
def type_description_widgets(placeholder: str, max_width: str = '500px') -> Textarea:
    return Textarea(attrs={'class' : 'form-control',
            'style' : f'max-width:{max_width};',
            'placeholder' : f'{placeholder}'
        })



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
        'activity_causing_injury' : type_widget('How did the injury occur?')
        }


# Incident Report Form
class IncidentReportForm(UrecReportForm):
    class Meta(UrecReportForm.Meta):
        model = IncidentReport
        fields = UrecReportForm.Meta.fields + ["activity_during_incident"]
        widgets={
        'activity_during_incident' : type_widget('How did the incident occur?')
        }


# Report Specific Formsets


# Injury Formset for Injury/Illness Report
injury_illness_report_injury_formset = modelformset_factory(
    InjuryIllnessReportInjury, fields=('injury_type', 'injury_description', 'care_provided'), extra=1,
    widgets={
        'injury_type' : type_widget('Injury Type'),
        'injury_description' : type_description_widgets('Describe the Injury'),
        'care_provided' : type_widget('Care Provided'),
    }
    
)


# Incident Formset for Incident Report
incident_report_incident_formset = modelformset_factory(
    IncidentReportIncident, fields=('incident_nature', 'incident_description', 'action_taken'), extra=1,
    widgets={
        'incident_nature' : type_widget('Incident'),
        'incident_description' : type_description_widgets('Describe the Incident'),
        'action_taken' : type_widget('Actions Taken'),
    }
    
)


# Report Contact Forms


# Generic Contact Form for Injury/Illness and Incident Patient Contacts
class UrecContactForm(forms.ModelForm):
    class Meta:
        model = UrecContact
        fields = ["first_name", "middle_name", "last_name", "email_address", "personal_phone_number",
                  "home_phone_number", "street_address", "city", "state", "zip", "minor_status"]
        widgets= CONTACT_WIDGETS


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
        widgets= CONTACT_WIDGETS
    )


# Generic Contact Information Formset for Generic UREC Report
urec_contact_formset = create_urec_contact_formset(UrecContact)


# Witness Contact Information Formset for Injury/Illness Report
injury_illness_report_contact_witness_formset = create_urec_contact_formset(InjuryIllnessReportContactWitness)


# Witness Contact Information Formset for Incident Report
incident_report_contact_witness_formset = create_urec_contact_formset(IncidentReportContactWitness)


class CountForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=UrecLocation.objects.all())
 
    class Meta:
        model = Count
        fields = ('location', 'location_count')
        widgets ={
            'location_count': NumberInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 200px;',
                'placeholder' : 'Count'
                })
            }


CountFormSet = formset_factory(CountForm, extra=1)        


class TaskForm(forms.ModelForm):
    model = get_user_model()
    date_time_due = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    staff_netid = forms.ModelChoiceField(queryset=model.objects.all())

    class Meta:
        model = Task
        fields = ["task_name", "task_description", "staff_netid", "date_time_due", "text_input_required", "recurrence_pattern"]
        widgets = {
            "date": AdminDateWidget(),
            "time": AdminTimeWidget()
        }


class TaskCompletionForm(forms.Form):
    completion_text = forms.CharField(label='Completion Text', max_length=255)


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

        widgets = {
            'email': type_widget('Email'),
            'username': type_widget('Username'),
            'first_name': type_widget('First Name'),
            'last_name': type_widget('Last Name'),
            'phone_number': NumberInput(attrs={
                'class' : 'form-control',
                'style' : 'max-width: 400px;',
            }),
        }
