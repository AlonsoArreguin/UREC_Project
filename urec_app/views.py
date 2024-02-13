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


# Injury/Illness Report Page
@login_required
def injury_illness(request):
    return render(request, 'urec_app/injury_illness.html')


# Create Injury/Illness View
class CreateInjuryIllnessReport(TemplateView):
    template_name = "urec_app/create_injury_illness_report.html"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/accounts/login')
        injury_formset = injury_illness_report_injury_formset(queryset=InjuryIllnessReportInjury.objects.none())
        injury_illness_report = InjuryIllnessReportForm()
        patient = InjuryIllnessReportContactPatientForm()
        witness_formset = injury_illness_report_witness_contact_formset(queryset=InjuryIllnessReportContactWitness.objects.none())
        context = {
            'injury_illness_report': injury_illness_report,
            'injury_illness_report_injury_formset': injury_formset,
            'patient': patient,
            'injury_illness_report_witness_formset': witness_formset,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/accounts/login')
        injury_illness_report = InjuryIllnessReportForm(data=self.request.POST)
        injury_type = injury_illness_report_injury_formset(data=self.request.POST)
        patient = InjuryIllnessReportContactPatientForm(data=self.request.POST)
        witness = injury_illness_report_witness_contact_formset(data=self.request.POST)

        all_good = (injury_illness_report.is_valid(), injury_type.is_valid(), patient.is_valid(), witness.is_valid())

        if False not in all_good:
            injury_illness_instance = injury_illness_report.save(commit=False)
            injury_instance = injury_type.save(commit=False)
            patient_instance = patient.save(commit=False)
            witness_instances = witness.save(commit=False)
            injury_illness_instance.staff_netid = self.request.user
            injury_illness_instance.save()
            for i in injury_instance:
                i.injury_illness_report = injury_illness_instance
                i.save()

            patient_instance.injury_illness_report = injury_illness_instance
            patient_instance.save()
            for witness_instance in witness_instances:
                witness_instance.patient = patient_instance
                witness_instance.injury_illness_report = injury_illness_instance
                witness_instance.save()

            return redirect('injury_illness')

        print(all_good)

        return self.render_to_response({'injury-illness-report-injury-formset': injury_type,
                                        'injury_illness_report_witness_formset': witness})


# View all Injury/Illness Reports
@login_required
def view_injury_illness_reports(request):
    injury_illness_report = InjuryIllnessReport.objects.all()
    injury_type = InjuryIllnessReportInjury.objects.all()
    patient = InjuryIllnessReportContactPatient.objects.all()

    context = {'injury_illness_report': injury_illness_report, 'injury_type': injury_type, 'contact_info': patient}
    return render(request, 'urec_app/view_injury_illness_reports.html', context)


@login_required
def edit_injury_illness(request):
    if request.method == 'POST':
        var = request.POST['id']
        ill_id = InjuryIllnessReport.objects.filter(report_id=var)
        injury_type = InjuryIllnessReportInjury.objects.filter(injury_illness_report=ill_id[0])
        patient = InjuryIllnessReportContactPatient.objects.filter(injury_illness_report=ill_id[0])
        context = {'var': var, 'ill_id': ill_id, 'injury_type': injury_type, 'contact_info': patient}
    return render(request, 'urec_app/view_injury_illness.html', context)


@login_required
def delete_injury_illness(request, injury_illness_id):
    injury_illness = InjuryIllnessReport.objects.get(report_id=injury_illness_id)
    if request.method == "POST":
        # delete from database
        injury_illness.delete()

    return redirect('view_injury_illness_reports')


# Incident Report Page
@login_required
def incident(request):
    return render(request, 'urec_app/incident.html')


# Create Incident View
class CreateIncidentReport(TemplateView):
    template_name = "urec_app/create_incident_report.html"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/accounts/login')
        incident_formset = incident_report_incident_formset(queryset=IncidentReportIncident.objects.none())
        incident_report = IncidentReportForm()
        patient_contact = IncidentReportContactPatientForm()
        witness_formset = incident_report_witness_formset(queryset=IncidentReportContactWitness.objects.none())

        context = {
            'incident_report': incident_report,
            'incident_type_formset': incident_formset,
            'patient_contact': patient_contact,
            'incident_witness_formset': witness_formset,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/accounts/login')
        incident_report = IncidentReportForm(data=self.request.POST)
        incident_type = incident_report_incident_formset(data=self.request.POST)
        patient_contact = IncidentReportContactPatientForm(data=self.request.POST)
        witness_contact = incident_report_witness_formset(data=self.request.POST)

        if incident_report.is_valid() and incident_type.is_valid() \
                and patient_contact.is_valid() and witness_contact.is_valid():

            report_instance = incident_report.save(commit=False)
            type_instance = incident_type.save(commit=False)
            patient_instance = patient_contact.save(commit=False)
            witness_instances = witness_contact.save(commit=False)
            incident_report.instance.staff_netid = self.request.user
            report_instance.save()
            for i in type_instance:
                i.incident_report = report_instance
                i.save()

            patient_instance.incident_report = report_instance
            patient_instance.save()

            for witness_instance in witness_instances:
                witness_instance.incident_report = report_instance
                witness_instance.patient = patient_instance
                witness_instance.save()

            return redirect('incident')

        return self.render_to_response({'incident_type_formset': incident_type})


# View all Incident Reports
@login_required
# @staff_member_required
def view_incident_reports(request):
    incident_reports = IncidentReport.objects.all().order_by('-report_id').values()

    context = {'incident_report': incident_reports}  # , 'incident_type': incident_type, 'patient': patient}
    return render(request, 'urec_app/view_incident_reports.html', context)


# View/Edit an individual Incident Reports
@login_required
# @staff_member_required
def view_incident_id(request):
    if request.method == 'POST':
        var = request.POST['id']
        inc_id = IncidentReport.objects.filter(report_id=var)
        incident_type = IncidentReportIncident.objects.filter(incident_report=inc_id[0])
        patient = IncidentReportContactPatient.objects.filter(incident_report=inc_id[0])
        witness = IncidentReportContactWitness.objects.filter(incident_report=inc_id[0])
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