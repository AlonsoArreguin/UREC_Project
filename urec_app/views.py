from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .forms import *
# from .storage_backends import *

from collections import defaultdict
from datetime import datetime


# Home Page
@login_required
def home(request):
    return render(request, 'urec_app/home.html')


# Edit User Account
@login_required
def edit_account(request):
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditAccountForm(instance=request.user)
        args = {'form': form}
        return render(request, 'urec_app/edit_account.html', args)


# Report Homepages


# Injury/Illness Report Page
@login_required
def injury_illness(request):
    context = {
        'report_name': 'Injury/Illness',
        'create_report_url': 'create_injury_illness_report',
        'view_reports_url': 'view_injury_illness_reports'
    }
    return render(request, 'urec_app/report_homepage.html', context)


# Incident Report Page
@login_required
def incident(request):
    context = {
        'report_name': 'Incident',
        'create_report_url': 'create_incident_report',
        'view_reports_url': 'view_incident_reports'
    }
    return render(request, 'urec_app/report_homepage.html', context)


# Create Reports


# Generic Create Report View for Injury/Illness and Incident Reports
class CreateUrecReport(TemplateView):
    template_name = "urec_app/create_report.html"
    report_name = "UREC"
    report_home_url = "injury_illness"
    report_specific_name = "Specific"

    ReportForm = UrecReportForm

    ReportContactPatientForm = UrecContactForm

    ReportSpecific = UrecReportSpecific
    report_specific_formset = urec_report_specific_formset

    ReportContactWitness = UrecContact
    report_contact_witness_formset = urec_contact_formset

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/accounts/login')

        context = {
            'report_name': self.report_name,
            'report_form': self.ReportForm(prefix='report'),

            'report_specific_name': self.report_specific_name,
            'report_specific_formset': self.report_specific_formset(
                prefix='specific',
                queryset=self.ReportSpecific.objects.none()),

            'report_contact_patient': self.ReportContactPatientForm(prefix='patient'),

            'report_contact_witness_formset': self.report_contact_witness_formset(
                prefix='witness',
                queryset=self.ReportContactWitness.objects.none())
        }

        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/accounts/login')

        report_form = self.ReportForm(prefix='report', data=self.request.POST)

        report_contact_patient = self.ReportContactPatientForm(prefix='patient', data=self.request.POST)

        report_specific_formset = self.report_specific_formset(prefix='specific', data=self.request.POST)

        report_contact_witness_formset = self.report_contact_witness_formset(prefix='witness', data=self.request.POST)

        all_good = (report_form.is_valid(), report_specific_formset.is_valid(), report_contact_patient.is_valid(),
                    report_contact_witness_formset.is_valid())

        if False not in all_good:
            report_form_instance = report_form.save(commit=False)
            report_form_instance.staff_netid = self.request.user
            report_form_instance.save()

            report_contact_patient_instance = report_contact_patient.save(commit=False)
            report_contact_patient_instance.report = report_form_instance
            report_contact_patient_instance.save()

            report_specific_instance = report_specific_formset.save(commit=False)
            for instance in report_specific_instance:
                instance.report = report_form_instance
                instance.save()

            report_contact_witness_formset_instances = report_contact_witness_formset.save(commit=False)
            for instance in report_contact_witness_formset_instances:
                instance.patient = report_contact_patient_instance
                instance.report = report_form_instance
                instance.save()

            return redirect(self.report_home_url)

        print(all_good)

        context = {
            'report_name': self.report_name,
            'report_form': report_form,

            'report_specific_name': self.report_specific_name,
            'report_specific_formset': report_specific_formset,

            'report_contact_patient': report_contact_patient,
            'report_contact_witness_formset': report_contact_witness_formset,
        }

        return self.render_to_response(context)


# Create Injury/Illness View
class CreateInjuryIllnessReport(CreateUrecReport):
    report_name = "Injury/Illness"
    report_home_url = "injury_illness"
    report_specific_name = "Injury Type"

    ReportForm = InjuryIllnessReportForm

    ReportContactPatientForm = InjuryIllnessReportContactPatientForm

    ReportSpecific = InjuryIllnessReportInjury
    report_specific_formset = injury_illness_report_injury_formset

    ReportContactWitness = InjuryIllnessReportContactWitness
    report_contact_witness_formset = injury_illness_report_contact_witness_formset


# Create Incident View
class CreateIncidentReport(CreateUrecReport):
    report_name = "Incident"
    report_home_url = "incident"
    report_specific_name = "Incident Type"

    ReportForm = IncidentReportForm

    ReportContactPatientForm = IncidentReportContactPatientForm

    ReportSpecific = IncidentReportIncident
    report_specific_formset = incident_report_incident_formset

    ReportContactWitness = IncidentReportContactWitness
    report_contact_witness_formset = incident_report_contact_witness_formset


# View Reports


# Generic View Function for Injury/Illness and Incident Reports
def view_report(request, report, report_name, specific_field_names, specific_field_labels):
    field_names = ['report_id', 'date_time_submission', 'urec_facility', 'location_in_facility', 'staff_netid']
    field_names.extend(specific_field_names)

    field_labels = ['Report ID', 'Date/Time Submission', 'UREC Facility', 'Location in Facility', 'Staff NetID']
    field_labels.extend(specific_field_labels)

    raw_reports = report.objects.all()
    reports = []
    for raw_report in raw_reports:
        report = []
        for field_name in field_names:
            report.append(getattr(raw_report, field_name))
        reports.append(report)
    context = {
        'report_name': report_name,
        'field_labels': field_labels,
        'reports': reports
    }
    return render(request, 'urec_app/view_reports.html', context)


# View all Injury/Illness Reports
@login_required
def view_injury_illness_reports(request):
    return view_report(request, InjuryIllnessReport, "Injury/Illness",
                       ['activity_causing_injury'],
                       ['Activity Causing Injury'])


# View all Incident Reports
@login_required
def view_incident_reports(request):
    return view_report(request, IncidentReport, "Incident",
                       ['activity_during_incident'],
                       ['Activity During Incident'])


# Injury/Illness Functions


@login_required
def edit_injury_illness(request):
    if request.method == 'POST':
        var = request.POST['id']
        ill_id = InjuryIllnessReport.objects.filter(report_id=var)
        injury_type = InjuryIllnessReportInjury.objects.filter(report=ill_id[0])
        patient = InjuryIllnessReportContactPatient.objects.filter(report=ill_id[0])
        context = {'var': var, 'ill_id': ill_id, 'injury_type': injury_type, 'contact_info': patient}
    return render(request, 'urec_app/view_injury_illness.html', context)


@login_required
def delete_injury_illness(request, injury_illness_id):
    injury_illness = InjuryIllnessReport.objects.get(report_id=injury_illness_id)
    if request.method == "POST":
        # delete from database
        injury_illness.delete()

    return redirect('view_injury_illness_reports')


# Incident Functions


# View/Edit an individual Incident Reports
@login_required
# @staff_member_required
def view_incident_id(request):
    if request.method == 'POST':
        var = request.POST['id']
        inc_id = IncidentReport.objects.filter(report_id=var)
        incident_type = IncidentReportIncident.objects.filter(report=inc_id[0])
        patient = IncidentReportContactPatient.objects.filter(report=inc_id[0])
        witness = IncidentReportContactWitness.objects.filter(report=inc_id[0])
        context = {'var': var, 'inc_id': inc_id, 'incident_type': incident_type, 'patient': patient, 'witness': witness}
    return render(request, 'urec_app/view_incident.html', context)


# Delete Incident Report
@login_required
# @staff_member_required
def delete_incident(request, incident_id):
    incident = IncidentReport.objects.get(report_id=incident_id)
    if request.method == "POST":
        # delete from database
        incident.delete()

    return redirect('view_incident_reports')


# Count Functions


# Counts Page
@login_required
def count(request):
    return render(request, 'urec_app/count.html')


# Update Count in Facilities
@login_required
def count_update(request):
    if request.method == 'POST':
        count_form = CountFormSet(data=request.POST)
        if count_form.is_valid():
            for count in count_form:
                count_instance = count.save(commit=False)
                count_instance.staff_netid = request.user
                count_instance.save()

            return redirect('count')
    count_form = CountFormSet(queryset=Count.objects.none())

    context = {'count_form': count_form}
    return render(request, 'urec_app/count_update.html', context)


# View All Count History
@login_required
# @staff_member_required
def count_view_history(request):
    count_item = Count.objects.all().order_by('-count_id').values()
    recent_list = []

    for facility, locations in UREC_LOCATIONS:
        for location_id, location_name in locations:
            recent_count = Count.objects.filter(location_in_facility=location_id).order_by(
                '-date_time_submission').first()
            recent_list.append(recent_count)

            # alternative way to append
            """
            if recent_count != None:
                recent_list.append(recent_count)
            """

    context = {'count_item': count_item, 'recent_list': recent_list}
    return render(request, 'urec_app/count_view_history.html', context)


# Helper function for count_hourly()
# TODO probably move somewhere else
def convert_to_ampm(hour):
    if hour == 0:
        return "12:00 AM"
    elif hour == 12:
        return "12:00 PM"
    elif hour < 12:
        return f"{hour}:00 AM"
    else:
        return f"{hour - 12}:00 PM"


# Helper function for count_hourly()
# TODO probably move somewhere else
# TODO change to sort by better hours
def sort_ampm_key(item):
    hour_str, meridiem = item[0].split(":")[0], item[0].split()[1]
    hour = int(hour_str) if hour_str != "12" else 0
    return (1 if meridiem == "PM" else 0, hour)


@login_required
def count_hourly(request):
    counts = Count.objects.all()

    # Filter counts based on today's date
    # today = datetime.today().date()
    # today_counts = [count for count in counts if count.date_time_submission.date() == today]

    # Filter counts based on datepicker
    # If 'date' is provided in GET params, parse it. Otherwise, use today's date.
    selected_date_str = request.GET.get('date', None)
    selected_date = datetime.today().date()

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.today().date()

    today_counts = [count for count in counts if count.date_time_submission.date() == selected_date]

    hourly_counts = defaultdict(list)

    # Initialize all hours in the dictionary
    for i in range(24):
        # hourly_counts[i] = []
        ampm_hour = convert_to_ampm(i)
        hourly_counts[ampm_hour] = []

    # Convert to AM/PM format and append to hourly_counts
    for count in today_counts:
        hour = count.date_time_submission.hour
        ampm_hour = convert_to_ampm(hour)

        hourly_counts[ampm_hour].append(count)

    # Sorted counts by hour
    sorted_hourly_counts = dict(sorted(hourly_counts.items(), key=sort_ampm_key))

    # context = {'hourly_counts': sorted_hourly_counts, 'today': today}
    context = {'hourly_counts': sorted_hourly_counts, 'selected_date': selected_date}
    return render(request, 'urec_app/count_hourly.html', context)


# Delete Task
@login_required
# @staff_member_required
def delete_count(request, count_id):
    count = Count.objects.get(count_id=count_id)
    if request.method == "POST":
        # delete from database
        count.delete()

    return redirect('count_view_history')


# ERP Functions


# ERP Page
@login_required
def erp(request):
    return render(request, 'urec_app/erp.html')


# Create ERP Page
@login_required
# @staff_member_required
def create_erp(request):
    if request.method == "POST":
        # get form data from requests
        erp_file = ErpUploadForm(request.POST, request.FILES)
        erp_obj = ErpForm(request.POST)

        # extract file information
        uploadfile = request.FILES['file']  # entire file
        filelocation = uploadfile.name  # file name from entire file
        if erp_file.is_valid() and erp_obj.is_valid():
            # make instance of model with files information, then save to database
            erp = Erp(title=request.POST['title'], filename=filelocation, description=request.POST['description'])
            erp.save()

            # make instance of media storage, then save the file
            mediastorage = PublicMediaStorage()
            mediastorage.save(filelocation, uploadfile)

            # return user to erp home
            return redirect('erp')
    else:
        # give blank forms if not POST request
        erp_file = ErpUploadForm()
        erp_obj = ErpForm()
    context = {'erp_obj': erp_obj, 'erp_file': erp_file}
    return render(request, 'urec_app/create_erp.html', context)


# Delete ERP Process
@login_required
# @staff_member_required
def delete_erp(request, filename):
    erp = Erp.objects.get(filename=filename)
    if request.method == "POST":
        # delete from database
        erp.delete()
        # set variables necessary for S3 connection
        AWS_REGION = settings.AWS_DEFAULT_REGION
        S3_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
        ACCESS_ID = settings.AWS_ACCESS_KEY_ID
        ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
        # initialize S3 connections
        s3_resource = boto3.resource("s3", aws_access_key_id=ACCESS_ID,
                                     aws_secret_access_key=ACCESS_KEY, region_name=AWS_REGION)
        # get instance of S3 object based on filename
        s3_object = s3_resource.Object(S3_BUCKET_NAME, 'erpfiles/' + str(filename))
        # delete S3 object
        s3_object.delete()

    return redirect('view_erps')


# Download ERP Page/Process
@login_required
def download_erp(request, filename):
    # set variables necessary for S3 connection
    AWS_REGION = settings.AWS_DEFAULT_REGION
    S3_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
    ACCESS_ID = settings.AWS_ACCESS_KEY_ID
    ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    # initialize S3 connection
    s3_client = boto3.client("s3", aws_access_key_id=ACCESS_ID,
                             aws_secret_access_key=ACCESS_KEY, region_name=AWS_REGION)
    # download object in user's browser
    # s3_client.download_file(S3_BUCKET_NAME, str(filename), 'erpfiles/' + str(filename))
    erp_url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': S3_BUCKET_NAME, 'Key': 'erpfiles/' + str(filename)},
                                               ExpiresIn=300)

    context = {"erp_url": erp_url, "filename": filename}
    return render(request, 'urec_app/download_erp.html', context)


# View all ERPs
@login_required
def view_erps(request):
    Erps = Erp.objects.all().order_by('filename').values()
    context = {"Erps": Erps}
    return render(request, 'urec_app/view_erps.html', context)


# Task Functions


# Task Page
@login_required
def task(request):
    return render(request, 'urec_app/task.html')


# Create New Task
@login_required
# @staff_member_required
def create_task(request):
    if request.method == "POST":
        task_obj = TaskForm(request.POST)
        if task_obj.is_valid():
            task_obj.pk = None
            task_obj.save()

            return redirect('task')
    else:
        task_obj = TaskForm()
    context = {'task_obj': task_obj}
    return render(request, 'urec_app/create_task.html', context)


# View All Tasks
@login_required
# @staff_member_required
def all_tasks(request):
    task_item = Task.objects.all().order_by('-task_id').values()

    context = {'task_item': task_item}
    return render(request, 'urec_app/all_tasks.html', context)


# View My Tasks
@login_required
def my_tasks(request):
    username = request.user.username
    uncompleted_tasks = Task.objects.filter(staff_netid=username, task_completion=False)
    completed_tasks = Task.objects.filter(staff_netid=username, task_completion=True)

    context = {'uncompleted': uncompleted_tasks, 'completed': completed_tasks}
    return render(request, 'urec_app/my_tasks.html', context)


# View an Individual Task
@login_required
def view_task_id(request):
    if request.method == 'POST':
        var = request.POST['id']
        task_id = Task.objects.filter(task_id=var)
        context = {'var': var, 'task_id': task_id}
    return render(request, 'urec_app/task_id.html', context)


# View an Individual Task
@login_required
def view_my_task(request):
    if request.method == 'POST':
        var = request.POST['id']
        task_id = Task.objects.filter(task_id=var)
        context = {'var': var, 'task_id': task_id}
    return render(request, 'urec_app/view_my_task.html', context)


# Complete Task
@login_required
def complete_task(request, taskid):
    task = Task.objects.get(task_id=taskid)
    if request.method == "POST":
        # change task status to complete
        task.task_completion = True
        task.date_time_completion = now()
        task.save()

    return redirect('my_tasks')


# Delete Task
@login_required
# @staff_member_required
def delete_task(request, taskid):
    task = Task.objects.get(task_id=taskid)
    if request.method == "POST":
        # delete from database
        task.delete()

    return redirect('all_tasks')


# Unused Functions


# Survey View (NOT YET IMPLEMENTED)
@login_required
def survey(request):
    return render(request, 'urec_app/survey.html')


# SOP Page (NOT YET IMPLEMENTED)
@login_required
def sop(request):
    return render(request, 'urec_app/sop.html')


# Form Page (NOT YET IMPLEMENTED)
@login_required
def form(request):
    return render(request, 'urec_app/form.html')
