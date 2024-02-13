from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

# List of possible locations within facilities template
UREC_LOCATIONS = (
        ('Facility 1', (
            ('Location 1', 'Location 1'),
            ('Location 2', 'Location 2'),
            ('Location 3', 'Location 3'),
        )),
        ('Facility 2', (
            ('Location 4', 'Location 4'),
            ('Location 5', 'Location 5'),
            ('Location 6', 'Location 6'),
        )),
        ('Facility 3', (
            ('Location 7', 'Location 7'),
            ('Location 8', 'Location 8'),
            ('Location 9', 'Location 9'),
        )),
    )

# List of possible Facilities
UREC_FACILITIES = (
        ('Facility 1', 'Facility 1'),
        ('Facility 2', 'Facility 2'),
        ('Facility 3', 'Facility 3'),
    )

# Create your models here.


# This model acts as the basis for all other contact related models.
class UrecContact(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email_address = models.EmailField(max_length=255, blank=True)
    personal_phone_number = models.CharField(max_length=255, blank=True)
    home_phone_number = models.CharField(max_length=255, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    minor_status = models.CharField(max_length=255)

    objects = models.Manager()


# Primary Injury/Illness Report Model
class InjuryIllnessReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    urec_facility = models.CharField(max_length=255, choices=UREC_FACILITIES)
    location_in_facility = models.CharField(max_length=255, choices=UREC_LOCATIONS)
    activity_causing_injury = models.CharField(max_length=255)
    staff_netid = models.CharField(max_length=255)

    objects = models.Manager()


# Injury Model for Injury/Illness Report
class InjuryIllnessReportInjury(models.Model):
    injury_illness_report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)  # foreign key
    injury_type = models.CharField(max_length=255)
    injury_description = models.TextField(max_length=1023)
    care_provided = models.TextField(max_length=1023)

    objects = models.Manager()


# Patient Contact Information Model for Injury/Illness Report
class InjuryIllnessReportContactPatient(UrecContact):
    injury_illness_report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)  # foreign key
    injury_illness_relation = models.CharField(max_length=255, default='wip')  # Witness


# Witness Contact Information Model for Injury/Illness Report
class InjuryIllnessReportContactWitness(UrecContact):
    injury_illness_report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)  # foreign key
    injury_illness_relation = models.CharField(max_length=255, default='wip')  # Witness
    patient = models.ForeignKey(InjuryIllnessReportContactPatient, on_delete=models.CASCADE)


# Primary Incident Report Model
class IncidentReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    urec_facility = models.CharField(max_length=255, choices=UREC_FACILITIES)
    location_in_facility = models.CharField(max_length=255, choices=UREC_LOCATIONS)
    activity_during_incident = models.CharField(max_length=255)
    staff_netid = models.CharField(max_length=255)

    objects = models.Manager()


# Incident Sub-Model for Incident Specifics
class IncidentReportIncident(models.Model):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)  # foreign key
    incident_nature = models.CharField(max_length=255)
    incident_description = models.TextField(max_length=1023)
    action_taken = models.TextField(max_length=1023)

    objects = models.Manager()


# Patient Contact Information Model for Incident Report
class IncidentReportContactPatient(UrecContact):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)  # foreign key


# Witness Contact Information Model for Incident Report
class IncidentReportContactWitness(UrecContact):
    incident_report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)  # foreign key
    patient = models.ForeignKey(IncidentReportContactPatient, on_delete=models.CASCADE)  # foreign key


# Task Model
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=255, blank=True)
    date_time_due = models.DateTimeField()
    text_input_required = models.BooleanField(default=False)
    optional_text = models.CharField(max_length=255, blank=True)
    task_completion = models.BooleanField(default=False)
    date_time_completion = models.DateTimeField(null=True)
    staff_netid = models.CharField(max_length=255, blank=True)

    objects = models.Manager()


# Count Model
class Count(models.Model):
    count_id = models.AutoField(primary_key=True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    location_in_facility = models.CharField(max_length=255, choices=UREC_LOCATIONS)
    location_count = models.SmallIntegerField()
    staff_netid = models.CharField(max_length=255)

    objects = models.Manager()


# Erp Model for Database
class Erp(models.Model):
    # erp_id = models.AutoField()
    filename = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1023)
    uploaded_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()


# Erp Model for FileUpload ONLY
class ErpUpload(models.Model):
    file = models.FileField(validators=[FileExtensionValidator(allowed_extensions=["pdf"])])


class UrecUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
