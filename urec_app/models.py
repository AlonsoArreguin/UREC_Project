from django.db import models

UREC_FACILITIES = (
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

# Create your models here.

# ----------------------------------------------------------------------------------------------------------------------
# To-Be Deleted
# First from Models and Forms
# And then from Database

class Accident(models.Model):
    staff_netid = models.CharField(max_length=255)
    accident_type = models.CharField(max_length=255)
    accident_description = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

class AccidentTicket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    urec_facility = models.CharField(max_length=255)
    location_in_facility = models.CharField(max_length=255)
    activity_causing_injury = models.CharField(max_length=255)
    injury_type = models.CharField(max_length=255)
    injury_description = models.CharField(max_length=1023)
    staff_netid = models.CharField(max_length=255, default='tst123')

class AccidentTicketContactInfo(models.Model):
    accident_ticket = models.ForeignKey(AccidentTicket, on_delete=models.CASCADE) # foreign key
    accident_relation = models.CharField(max_length=255, default='wip') # Acidentee or Witness (multiple witness/ticket)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email_address = models.CharField(max_length=255, blank=True)
    personal_phone_number = models.CharField(max_length=255, blank=True)
    home_phone_number = models.CharField(max_length=255, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
# ----------------------------------------------------------------------------------------------------------------------


class Accident_Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    urec_facility = models.CharField(max_length=255)
    location_in_facility = models.CharField(max_length=255)
    activity_causing_injury = models.CharField(max_length=255)
    staff_netid = models.CharField(max_length=255, default='tst123')

    objects = models.Manager()

class Accident_Ticket_Injury(models.Model):
    accident_ticket = models.ForeignKey(Accident_Ticket, on_delete=models.CASCADE)  # foreign key
    injury_type = models.CharField(max_length=255)
    injury_description = models.TextField(max_length=1023)
    care_provided = models.TextField(max_length=1023)

    objects = models.Manager()

class Accident_Ticket_Contact_Info(models.Model):
    accident_ticket = models.ForeignKey(Accident_Ticket, on_delete=models.CASCADE)  # foreign key
    accident_relation = models.CharField(max_length=255, default='wip')  # Acidentee or Witness
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

    objects = models.Manager()

class Incident_Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    urec_facility = models.CharField(max_length=255)
    location_in_facility = models.CharField(max_length=255)
    activity_during_incident = models.CharField(max_length=255)
    staff_netid = models.CharField(max_length=255, default='tst123')

    objects = models.Manager()

class Incident_Ticket_Incident(models.Model):
    incident_ticket = models.ForeignKey(Incident_Ticket, on_delete=models.CASCADE)  # foreign key
    incident_nature = models.CharField(max_length=255)
    incident_description = models.TextField(max_length=1023)
    action_taken = models.TextField(max_length=1023)

    objects = models.Manager()

class Incident_Ticket_Contact_Patient(models.Model):
    incident_ticket = models.ForeignKey(Incident_Ticket, on_delete=models.CASCADE)  # foreign key
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


class Incident_Ticket_Contact_Witness(models.Model):
    incident_ticket = models.ForeignKey(Incident_Ticket, on_delete=models.CASCADE)  # foreign key
    patient = models.ForeignKey(Incident_Ticket_Contact_Patient, on_delete=models.CASCADE)  # foreign key
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

class Count(models.Model):
    count_id = models.AutoField(primary_key = True)
    date_time_submission = models.DateTimeField(auto_now_add=True)
    location_in_facility = models.CharField(max_length=255, choices=UREC_FACILITIES)
    location_count = models.SmallIntegerField()
    staff_netid = models.CharField(max_length=255, default='tst123')

    objects = models.Manager()

    # def __str__(self):
    #     return self.location_in_facility