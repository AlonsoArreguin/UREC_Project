from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser


# Facility / Location Models


# Facility Model for Reports and Counts
class UrecFacility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    facility_name = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.facility_name

    # Enforce that facilities must have a unique name
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["facility_name"],
                name="unique_facility_name",
            ),
        ]


# Location Model for Reports and Counts
class UrecLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    # models.RESTRICT will prevent the deletion of a facility with at least one location associated with it
    facility = models.ForeignKey(UrecFacility, on_delete=models.RESTRICT)
    location_name = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        facility_name = str(self.facility)
        return f"{facility_name} / {self.location_name}"

    # Enforce that a facility can't have two locations with the same name
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["facility", "location_name"],
                name="unique_facility_location_pair",
            ),
        ]


# Report Models


# Severity levels for reports
SEVERITY_LEVELS = (
    ('Minor', 'Minor'),
    ('Moderate', 'Moderate')
)


# Generic Report Model for Injury/Illness and Incident Models
class UrecReport(models.Model):
    report_id = models.AutoField("Report ID", primary_key=True)
    date_time_submission = models.DateTimeField("Date/Time Submitted", auto_now_add=True)
    # models.RESTRICT will prevent the deletion of a location with at least one report associated with it
    location = models.ForeignKey(UrecLocation, verbose_name="Facility / Location", on_delete=models.RESTRICT)
    severity = models.CharField("Severity Level", max_length=255, choices=SEVERITY_LEVELS)
    ems_called = models.BooleanField("EMS / Fire Called")
    police_called = models.BooleanField("Police Called")
    staff_netid = models.CharField("Staff NetID", max_length=255)

    objects = models.Manager()

    def get_labels(self):
        for field in self._meta.get_fields(include_hidden=False):
            if hasattr(field, "verbose_name"):
                if field.name != "urecreport_ptr":
                    yield field.verbose_name

    def get_values(self):
        for field in self._meta.get_fields(include_hidden=False):
            if hasattr(field, "verbose_name"):
                if field.name != "urecreport_ptr":
                    yield getattr(self, field.name)


# Injury/Illness Report Model
class InjuryIllnessReport(UrecReport):
    activity_causing_injury = models.CharField("Activity Causing Injury", max_length=255)


# Incident Report Model
class IncidentReport(UrecReport):
    activity_during_incident = models.CharField("Activity During Incident", max_length=255)


# Report Specific Models


# Generic Specific Model for Generic UREC Report
class UrecReportSpecific(models.Model):
    report = models.ForeignKey(UrecReport, on_delete=models.CASCADE)  # foreign key

    objects = models.Manager()


# Injury Model for Injury/Illness Report
class InjuryIllnessReportInjury(models.Model):
    report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)  # foreign key
    injury_type = models.CharField(max_length=255)
    injury_description = models.TextField(max_length=1023)
    care_provided = models.TextField(max_length=1023)

    objects = models.Manager()


# Incident Model for Incident Report
class IncidentReportIncident(models.Model):
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)  # foreign key
    incident_nature = models.CharField(max_length=255)
    incident_description = models.TextField(max_length=1023)
    action_taken = models.TextField(max_length=1023)

    objects = models.Manager()


# Report Contact Models


# Generic Contact Model for All Injury/Illness and Incident Contacts
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


# Patient Contact Information Model for Injury/Illness Report
class InjuryIllnessReportContactPatient(UrecContact):
    report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)  # foreign key
    injury_illness_relation = models.CharField(max_length=255, default='wip')  # Witness


# Patient Contact Information Model for Incident Report
class IncidentReportContactPatient(UrecContact):
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)  # foreign key


# Witness Contact Information Model for Injury/Illness Report
class InjuryIllnessReportContactWitness(UrecContact):
    report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)  # foreign key
    injury_illness_relation = models.CharField(max_length=255, default='wip')  # Witness
    patient = models.ForeignKey(InjuryIllnessReportContactPatient, on_delete=models.CASCADE)


# Witness Contact Information Model for Incident Report
class IncidentReportContactWitness(UrecContact):
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)  # foreign key
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
    # models.RESTRICT will prevent the deletion of a location with at least one count associated with it
    location = models.ForeignKey(UrecLocation, on_delete=models.RESTRICT)
    location_count = models.SmallIntegerField()
    staff_netid = models.CharField(max_length=255)

    objects = models.Manager()


# Erp Models


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


# Custom User Model containing Phone Number
class UrecUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
