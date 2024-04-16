from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'


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
        verbose_name = 'Location'


# Report Models


# Inheritable helper functions for grabbing field labels and values from a model
class ModelHelpers:
    def get_labels(self):
        for field in self._meta.get_fields(include_hidden=False):
            if hasattr(field, "verbose_name"):
                if ("_ptr" not in field.name) and (field.name not in ["report", "patient"]):
                    yield field.verbose_name

    def get_values(self):
        for field in self._meta.get_fields(include_hidden=False):
            if hasattr(field, "verbose_name"):
                if ("_ptr" not in field.name) and (field.name not in ["report", "patient"]):
                    yield getattr(self, field.name)


# Severity levels for reports
SEVERITY_LEVELS = (
    ('Minor', 'Minor'),
    ('Moderate', 'Moderate')
)


# Generic Report Model for Injury/Illness and Incident Models
class UrecReport(models.Model, ModelHelpers):
    report_id = models.AutoField("Report ID", primary_key=True)
    date_time_submission = models.DateTimeField("Date/Time Submitted")
    # models.RESTRICT will prevent the deletion of a location with at least one report associated with it
    location = models.ForeignKey(UrecLocation, verbose_name="Facility / Location", on_delete=models.RESTRICT)
    severity = models.CharField("Severity Level", max_length=255, choices=SEVERITY_LEVELS)
    ems_called = models.BooleanField("EMS / Fire Called")
    police_called = models.BooleanField("Police Called")
    staff_netid = models.CharField("Staff NetID", max_length=255)

    objects = models.Manager()


# Injury/Illness Report Model
class InjuryIllnessReport(UrecReport):
    activity_causing_injury = models.CharField("Activity Causing Injury", max_length=255)

    def __str__(self):
        return f"Injury/Illness Report #{self.report_id} - {self.activity_causing_injury}"

    class Meta:
        verbose_name = 'Injury/Illness Report'


# Incident Report Model
class IncidentReport(UrecReport):
    activity_during_incident = models.CharField("Activity During Incident", max_length=255)

    def __str__(self):
        return f"Incident Report #{self.report_id} - {self.activity_during_incident}"

    class Meta:
        verbose_name = 'Incident Report'


# Report Notifications


def find_applicable_users(users_to_notify, group_name):
    applicable_users = UrecUser.objects.filter(groups__name=group_name)
    for applicable_user in applicable_users:
        if applicable_user not in users_to_notify:
            users_to_notify[applicable_user] = []
        users_to_notify[applicable_user].append(group_name)


def send_notifications(instance, view_name, created):
    users_to_notify = {}

    if instance.ems_called:
        find_applicable_users(users_to_notify, 'EMS / Fire Called Notifications')
    if instance.police_called:
        find_applicable_users(users_to_notify, 'Police Called Notifications')
    if instance.severity == "Minor":
        find_applicable_users(users_to_notify, 'Minor Severity Notifications')
    if instance.severity == "Moderate":
        find_applicable_users(users_to_notify, 'Moderate Severity Notifications')

    domain = Site.objects.get_current().domain

    for user_to_notify in users_to_notify:
        if user_to_notify.email:
            view_url = domain + reverse(view_name, kwargs={'report_id': instance.report_id})
            reasons = ', '.join(users_to_notify[user_to_notify])
            reasons_condensed = reasons.replace(" Notifications", "")
            subject = f"Report Alert: {reasons_condensed}"
            html_message = render_to_string('urec_app/report_email.html', {
                "subject": subject,
                "created": created,
                "view_url": view_url,
                "reasons": reasons
            })
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                "from@example.com",
                [user_to_notify.email],
                html_message=html_message,
                fail_silently=True,
            )


@receiver(post_save, sender=InjuryIllnessReport)
def injury_illness_post_save_receiver(sender, instance, created, **kwargs):
    send_notifications(instance, 'view_injury_illness', created)


@receiver(post_save, sender=IncidentReport)
def incident_post_save_receiver(sender, instance, created, **kwargs):
    send_notifications(instance, 'view_incident', created)


# Report Specific Models


# Generic Specific Model for Generic UREC Report
class UrecReportSpecific(models.Model, ModelHelpers):
    report = models.ForeignKey(UrecReport, on_delete=models.CASCADE) 

    objects = models.Manager()


# Injury Model for Injury/Illness Report
class InjuryIllnessReportInjury(models.Model, ModelHelpers):
    report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE)
    injury_id = models.AutoField("Injury ID", primary_key=True)
    injury_type = models.CharField("Injury Type", max_length=255)
    injury_description = models.TextField("Injury Description", max_length=1023)
    care_provided = models.TextField("Care Provided", max_length=1023)

    objects = models.Manager()

    def __str__(self):
        return f"Injury/Illness Report Injury - {self.injury_type}"

    class Meta:
        verbose_name = 'Injury/Illness Report Injury'
        verbose_name_plural = 'Injury/Illness Report Injuries'


# Incident Model for Incident Report
class IncidentReportIncident(models.Model, ModelHelpers):
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
    incident_id = models.AutoField("Incident ID", primary_key=True)
    incident_nature = models.CharField("Incident Nature", max_length=255)
    incident_description = models.TextField("Incident Description", max_length=1023)
    action_taken = models.TextField("Action Taken", max_length=1023)

    objects = models.Manager()

    def __str__(self):
        return f"Incident Report Incident - {self.incident_nature}"

    class Meta:
        verbose_name = 'Incident Report Incident'


# Report Contact Models


# Generic Contact Model for All Injury/Illness and Incident Contacts
class UrecContact(models.Model, ModelHelpers):
    contact_id = models.AutoField("Contact ID", primary_key=True)
    first_name = models.CharField("First Name", max_length=255)
    middle_name = models.CharField("Middle Name", max_length=255, blank=True)
    last_name = models.CharField("Last Name", max_length=255, blank=True)
    email_address = models.EmailField("E-Mail Address", max_length=255, blank=True)
    personal_phone_number = models.CharField("Personal Phone Number", max_length=255, blank=True)
    home_phone_number = models.CharField("Home Phone Number", max_length=255, blank=True)
    street_address = models.CharField("Street Address", max_length=255, blank=True)
    city = models.CharField("City", max_length=255, blank=True)
    state = models.CharField("State", max_length=255, blank=True)
    zip = models.CharField("Zip Code", max_length=255, blank=True)
    minor_status = models.CharField("Is Minor", max_length=255)

    def get_full_name(self):
        return (f"{self.first_name}" +
                (f" {self.middle_name}" if self.middle_name else "") +
                (f" {self.last_name}" if self.last_name else ""))

    objects = models.Manager()


# Patient Contact Information Model for Injury/Illness Report
class InjuryIllnessReportContactPatient(UrecContact):
    report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE) 
    injury_illness_relation = models.CharField("Relation to Witnesses", max_length=255, default='wip')  # Witness

    def __str__(self):
        return f"Injury/Illness Report Patient Contact - {self.get_full_name()}"

    class Meta:
        verbose_name = 'Injury/Illness Report Patient Contact'


# Patient Contact Information Model for Incident Report
class IncidentReportContactPatient(UrecContact):
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Incident Report Patient Contact - {self.get_full_name()}"

    class Meta:
        verbose_name = 'Incident Report Patient Contact'


# Witness Contact Information Model for Injury/Illness Report
class InjuryIllnessReportContactWitness(UrecContact):
    report = models.ForeignKey(InjuryIllnessReport, on_delete=models.CASCADE) 
    injury_illness_relation = models.CharField("Relation to Patient", max_length=255, default='wip')  # Witness
    patient = models.ForeignKey(InjuryIllnessReportContactPatient, on_delete=models.CASCADE)

    def __str__(self):
        return f"Injury/Illness Report Witness Contact - {self.get_full_name()}"

    class Meta:
        verbose_name = 'Injury/Illness Report Witness Contact'


# Witness Contact Information Model for Incident Report
class IncidentReportContactWitness(UrecContact):
    report = models.ForeignKey(IncidentReport, on_delete=models.CASCADE) 
    patient = models.ForeignKey(IncidentReportContactPatient, on_delete=models.CASCADE) 

    def __str__(self):
        return f"Incident Report Witness Contact - {self.get_full_name()}"

    class Meta:
        verbose_name = 'Incident Report Witness Contact'


RECURRENCE_CHOICES = (
    (None, 'None'),  # Default option
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
)


# Task Model
class Task(models.Model):
    task_id = models.AutoField("Task ID", primary_key=True)
    task_name = models.CharField("Task Name", max_length=255)
    task_description = models.CharField("Task Description", max_length=255, blank=True)
    date_time_due = models.DateTimeField("Date/Time Due")
    text_input_required = models.BooleanField("Text Input Required", default=False)
    completion_text = models.CharField("Completion Text", max_length=255, blank=True)
    task_completion = models.BooleanField("Task Completed", default=False)
    date_time_completion = models.DateTimeField("Date/Time Completed", blank=True)
    staff_netid = models.CharField("Staff NetID", max_length=255, blank=True)
    recurrence_pattern = models.CharField("Recurrence Pattern", max_length=20, choices=RECURRENCE_CHOICES, blank=True)
    
    objects = models.Manager()

    def __str__(self):
        human_date = self.date_time_due.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %I:%M %p")
        done = 'done' if self.task_completion else ''
        return f"{human_date} {self.recurrence_pattern} {done} - {self.staff_netid} - {self.task_name}"

    def clean(self):
        if self.task_completion and not self.date_time_completion:
            raise ValidationError("Date/Time Completed is required if task is completed.")

        if self.date_time_completion and not self.task_completion:
            raise ValidationError("Date/Time Completed cannot be set if task is not completed.")

        if self.completion_text and not self.text_input_required:
            raise ValidationError("Completion text cannot be set if text input is not required.")

        if (self.text_input_required and self.task_completion) and not self.completion_text:
            raise ValidationError("Completion text is required if text input is required and task is completed.")


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
