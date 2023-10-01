# Generated by Django 4.1.2 on 2023-10-01 02:29

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_netid', models.CharField(max_length=255)),
                ('accident_type', models.CharField(max_length=255)),
                ('accident_description', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Accident_Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time_submission', models.DateTimeField(auto_now_add=True)),
                ('urec_facility', models.CharField(choices=[('Facility 1', 'Facility 1'), ('Facility 2', 'Facility 2'), ('Facility 3', 'Facility 3')], max_length=255)),
                ('location_in_facility', models.CharField(choices=[('Facility 1', (('Location 1', 'Location 1'), ('Location 2', 'Location 2'), ('Location 3', 'Location 3'))), ('Facility 2', (('Location 4', 'Location 4'), ('Location 5', 'Location 5'), ('Location 6', 'Location 6'))), ('Facility 3', (('Location 7', 'Location 7'), ('Location 8', 'Location 8'), ('Location 9', 'Location 9')))], max_length=255)),
                ('activity_causing_injury', models.CharField(max_length=255)),
                ('staff_netid', models.CharField(default='tst123', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Accident_Ticket_Contact_Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accident_relation', models.CharField(default='wip', max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email_address', models.EmailField(blank=True, max_length=255)),
                ('personal_phone_number', models.CharField(blank=True, max_length=255)),
                ('home_phone_number', models.CharField(blank=True, max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('zip', models.CharField(blank=True, max_length=255)),
                ('accident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.accident_ticket')),
            ],
        ),
        migrations.CreateModel(
            name='AccidentTicket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time_submission', models.DateTimeField(auto_now_add=True)),
                ('urec_facility', models.CharField(max_length=255)),
                ('location_in_facility', models.CharField(max_length=255)),
                ('activity_causing_injury', models.CharField(max_length=255)),
                ('injury_type', models.CharField(max_length=255)),
                ('injury_description', models.CharField(max_length=1023)),
                ('staff_netid', models.CharField(default='tst123', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Count',
            fields=[
                ('count_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time_submission', models.DateTimeField(auto_now_add=True)),
                ('location_in_facility', models.CharField(choices=[('Facility 1', (('Location 1', 'Location 1'), ('Location 2', 'Location 2'), ('Location 3', 'Location 3'))), ('Facility 2', (('Location 4', 'Location 4'), ('Location 5', 'Location 5'), ('Location 6', 'Location 6'))), ('Facility 3', (('Location 7', 'Location 7'), ('Location 8', 'Location 8'), ('Location 9', 'Location 9')))], max_length=255)),
                ('location_count', models.SmallIntegerField()),
                ('staff_netid', models.CharField(default='tst123', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Erp',
            fields=[
                ('filename', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1023)),
                ('uploaded_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Erp_Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
            ],
        ),
        migrations.CreateModel(
            name='Incident_Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time_submission', models.DateTimeField(auto_now_add=True)),
                ('urec_facility', models.CharField(choices=[('Facility 1', 'Facility 1'), ('Facility 2', 'Facility 2'), ('Facility 3', 'Facility 3')], max_length=255)),
                ('location_in_facility', models.CharField(choices=[('Facility 1', (('Location 1', 'Location 1'), ('Location 2', 'Location 2'), ('Location 3', 'Location 3'))), ('Facility 2', (('Location 4', 'Location 4'), ('Location 5', 'Location 5'), ('Location 6', 'Location 6'))), ('Facility 3', (('Location 7', 'Location 7'), ('Location 8', 'Location 8'), ('Location 9', 'Location 9')))], max_length=255)),
                ('activity_during_incident', models.CharField(max_length=255)),
                ('staff_netid', models.CharField(default='tst123', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Incident_Ticket_Contact_Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email_address', models.EmailField(blank=True, max_length=255)),
                ('personal_phone_number', models.CharField(blank=True, max_length=255)),
                ('home_phone_number', models.CharField(blank=True, max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('zip', models.CharField(blank=True, max_length=255)),
                ('minor_status', models.CharField(max_length=255)),
                ('incident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.incident_ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=255)),
                ('task_description', models.CharField(blank=True, max_length=255)),
                ('date_time_due', models.DateTimeField()),
                ('text_input_required', models.BooleanField(default=False)),
                ('optional_text', models.CharField(blank=True, max_length=255)),
                ('task_completion', models.BooleanField(default=False)),
                ('date_time_completion', models.DateTimeField(null=True)),
                ('staff_netid', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Incident_Ticket_Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_nature', models.CharField(max_length=255)),
                ('incident_description', models.TextField(max_length=1023)),
                ('action_taken', models.TextField(max_length=1023)),
                ('incident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.incident_ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Incident_Ticket_Contact_Witness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email_address', models.EmailField(blank=True, max_length=255)),
                ('personal_phone_number', models.CharField(blank=True, max_length=255)),
                ('home_phone_number', models.CharField(blank=True, max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('zip', models.CharField(blank=True, max_length=255)),
                ('minor_status', models.CharField(max_length=255)),
                ('incident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.incident_ticket')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.incident_ticket_contact_patient')),
            ],
        ),
        migrations.CreateModel(
            name='AccidentTicketContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accident_relation', models.CharField(default='wip', max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email_address', models.CharField(blank=True, max_length=255)),
                ('personal_phone_number', models.CharField(blank=True, max_length=255)),
                ('home_phone_number', models.CharField(blank=True, max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('zip', models.CharField(blank=True, max_length=255)),
                ('accident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.accidentticket')),
            ],
        ),
        migrations.CreateModel(
            name='Accident_Ticket_Injury',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('injury_type', models.CharField(max_length=255)),
                ('injury_description', models.TextField(max_length=1023)),
                ('care_provided', models.TextField(max_length=1023)),
                ('accident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.accident_ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Accident_Ticket_Contact_Witness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accident_relation', models.CharField(default='wip', max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('email_address', models.EmailField(blank=True, max_length=255)),
                ('personal_phone_number', models.CharField(blank=True, max_length=255)),
                ('home_phone_number', models.CharField(blank=True, max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('zip', models.CharField(blank=True, max_length=255)),
                ('accident_ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.accident_ticket')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='urec_app.accident_ticket_contact_patient')),
            ],
        ),
        migrations.CreateModel(
            name='UREC_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
