from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import os, platform
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from .forms import *
from .models import *
# from .storage_backends import *

from collections import defaultdict
from datetime import datetime

from django.views import generic


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
            report_form_instance.date_time_submission = timezone.now()
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
def view_reports(request, report_model, report_name, view_url):
    raw_reports = report_model.objects.all()
    reports = []
    field_labels = report_model.get_labels(report_model)
    for raw_report in raw_reports:
        report = {
            'id': raw_report.report_id,
            'values': raw_report.get_values()
        }
        reports.append(report)
    context = {
        'report_name': report_name,
        'view_url': view_url,
        'field_labels': field_labels,
        'reports': reports
    }
    return render(request, 'urec_app/view_reports.html', context)


# View all Injury/Illness Reports
@login_required
def view_injury_illness_reports(request):
    return view_reports(request, InjuryIllnessReport, "Injury/Illness", "view_injury_illness")


# View all Incident Reports
@login_required
def view_incident_reports(request):
    return view_reports(request, IncidentReport, "Incident", "view_incident")


# View Report


def view_report(request, report_model, special_model, patient_model, witness_model, report_id, special_name):
    raw_report = get_object_or_404(report_model, report_id=report_id)
    raw_patient = patient_model.objects.filter(report=report_id).first()

    context = {
        'report_name': str(raw_report),
        'report_labels': report_model.get_labels(report_model),
        'report': raw_report.get_values(),
        'special_name': special_name,
        'special_labels': special_model.get_labels(special_model),
        'specials': [],
        'patient_labels': patient_model.get_labels(patient_model),
        'patient': raw_patient.get_values(),
        'witness_labels': witness_model.get_labels(witness_model),
        'witnesses': [],
    }

    raw_specials = special_model.objects.filter(report=report_id)
    for raw_special in raw_specials:
        context['specials'].append(raw_special.get_values())

    raw_witnesses = witness_model.objects.filter(report=report_id)
    for raw_witness in raw_witnesses:
        context['witnesses'].append(raw_witness.get_values())

    return render(request, 'urec_app/view_report.html', context)


# View Single Incident Report by ID
@login_required
def view_incident_report(request, report_id):
    return view_report(request, IncidentReport, IncidentReportIncident, IncidentReportContactPatient,
                       IncidentReportContactWitness, report_id, "Incidents")


# View Single Injury/Illness Report by ID
@login_required
def view_injury_illness_report(request, report_id):
    return view_report(request, InjuryIllnessReport, InjuryIllnessReportInjury, InjuryIllnessReportContactPatient,
                       InjuryIllnessReportContactWitness, report_id, "Injuries")


# Delete Report TODO: Ask client if these are necessary (should non-admins be allowed to delete reports)


@login_required
def delete_injury_illness(request, injury_illness_id):
    injury_illness = InjuryIllnessReport.objects.get(report_id=injury_illness_id)
    if request.method == "POST":
        # delete from database
        injury_illness.delete()

    return redirect('view_injury_illness_reports')


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
    CountFormSet = formset_factory(CountForm, extra=1)
    if request.method == 'POST':
        formset = CountFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    count_instance = form.save(commit=False)
                    count_instance.staff_netid = request.user.username
                    count_instance.save()
            return redirect('count')
    else:
        # fresh form for non-POST requests
        formset = CountFormSet()

    context = {'formset': formset}
    return render(request, 'urec_app/count_update.html', context)

# View All Count History
@login_required
# @staff_member_required
def count_view_history(request):
    count_items = Count.objects.all().order_by('-count_id')
    recent_counts = []

    for location in UrecLocation.objects.all().values():
        most_recent_count = Count.objects.filter(location=location['location_id']).order_by(
                '-date_time_submission').first()
        if most_recent_count:
            recent_counts.append(most_recent_count)

    context = {'count_item': count_items, 'recent_list': recent_counts}
    return render(request, 'urec_app/count_view_history.html', context)

# Helper function for count_hourly()
def convert_to_ampm(hour):
    if hour == 0:
        return "12:00 AM"
    elif hour == 12:
        return "12:00 PM"
    elif hour < 12:
        return f"{hour}:00 AM"
    else:
        return f"{hour - 12}:00 PM"

# View Hourly Counts
@login_required
def count_hourly(request):
    counts = Count.objects.all()

    # Filter counts based on datepicker
    # If 'date' is provided in GET params, parse it. Otherwise, use today's date.
    selected_date_str = request.GET.get('date', None)
    selected_date = datetime.today().date()

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    else:
        selected_date = datetime.today().date()

    today_counts = [count for count in counts 
    if count.date_time_submission.astimezone(timezone.get_current_timezone()).date() == selected_date]

    hourly_counts = defaultdict(dict)

    for count in today_counts:
        # Convert UTC formatted datetime to timezone-aware datetime
        local_dt = count.date_time_submission.astimezone(timezone.get_current_timezone())
        hour = local_dt.hour
        ampm_hour = convert_to_ampm(hour)

        # If the location isn't already in the hour or if the current count is more recent
        if (count.location not in hourly_counts[ampm_hour] or
            local_dt > hourly_counts[ampm_hour][count.location].date_time_submission):
            # Update this count object to most recent count object
            hourly_counts[ampm_hour][count.location] = count
    
    # Sort by the hours first, then by the most recent count within each hour
    sorted_hourly_counts = {
        hour: dict(sorted(locations.items(), key=lambda item: item[1].date_time_submission, reverse=True))
        for hour, locations in hourly_counts.items()}

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

# Used to detect user OS
def get_user_specific_directory():
    system = platform.system()
    if system == 'Windows':
        appdata_dir = os.environ.get('APPDATA', '')
        user_specific_dir = os.path.join(appdata_dir, 'Local', 'UREC')
    elif system == 'Darwin':
        user_specific_dir = os.path.expanduser('~/Library/Application Support/UREC')
    else:
        user_specific_dir = os.path.expanduser('~/.UREC')
    return user_specific_dir

# Create ERP Page
@login_required
# @staff_member_required
def create_erp(request):
    if request.method == "POST":
        # get form data from requests
        erp_file = ErpUploadForm(request.POST, request.FILES)
        erp_obj = ErpForm(request.POST)

        if erp_file.is_valid() and erp_obj.is_valid():
            # extract file information
            uploadfile = request.FILES['file']
            
            # Determine the user-specific directory
            custom_directory = get_user_specific_directory()
            # Create the directory if it doesn't exist
            os.makedirs(custom_directory, exist_ok=True)
            # Construct the file location within the custom directory
            filelocation = os.path.join(custom_directory, uploadfile.name)
            
            # Save uploaded file to custom directory
            with open(filelocation, 'wb+') as destination:
                for chunk in uploadfile.chunks():
                    destination.write(chunk)

            # Create instance of model with file information, then save to database
            erp = Erp(title=request.POST['title'], filename=uploadfile.name, description=request.POST['description'])
            erp.save()

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
    # Retrieve the ERP object from the database using the filename
    erp = get_object_or_404(Erp, filename=filename)

    if request.method == "POST":
        # Delete the ERP object from the database
        erp.delete()

        # Construct the file path within the custom directory
        custom_directory = get_user_specific_directory()
        file_path = os.path.join(custom_directory, filename)

        # Check if the file exists and deletes it
        if os.path.exists(file_path):
            os.remove(file_path)

        # Redirect to the view erps URL after deletion
        return redirect('view_erps')

    return redirect('view_erps')


# Download ERP pdf
@login_required
def download_erp(request, filename):

    # Retrieve the ERP object from the database using the filename
    erp = get_object_or_404(Erp, filename = filename)

    #Construct the file path within the custom directory
    custom_directory = get_user_specific_directory()
    file_path = os.path.join(custom_directory, filename)

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(),content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


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
    
    if task.text_input_required and request.method == "POST":
        form = TaskCompletionForm(request.POST)
        if form.is_valid():
            task.task_completion = True
            task.date_time_completion = timezone.now()
            task.completion_text = form.cleaned_data['completion_text']
            task.save()
            
            if task.recurrence_pattern:  # Check if a recurrence pattern is selected
                # Create a new recurring task
                new_task = create_recurring_task(task)
                return redirect('my_tasks')
            else:
                return redirect('my_tasks')
    elif task.text_input_required:
        form = TaskCompletionForm()
    else:
        # For tasks that don't require text input, directly mark them as completed
        task.task_completion = True
        task.date_time_completion = timezone.now()
        task.save()
        
        if task.recurrence_pattern:  # Check if a recurrence pattern is selected
            # Create a new recurring task
            new_task = create_recurring_task(task)
            return redirect('my_tasks')
        else:
            return redirect('my_tasks')
    
    return redirect('my_tasks')

def create_recurring_task(task):
    
    # Creates new task with same information and new due date
    new_task = Task.objects.create(
        task_name=task.task_name,
        task_description=task.task_description,
        date_time_due=calculate_next_due_date(task.date_time_due, task.recurrence_pattern),
        text_input_required=task.text_input_required,
        staff_netid=task.staff_netid,
        recurrence_pattern=task.recurrence_pattern
    )
    return new_task

def calculate_next_due_date(current_due_date, recurrence_pattern):
    
    #Calculates next due date depending on pattern

    if recurrence_pattern == 'daily':
        return current_due_date + timedelta(days=1)
    elif recurrence_pattern == 'weekly':
        return current_due_date + timedelta(weeks=1)
    elif recurrence_pattern == 'monthly':
        return current_due_date + relativedelta(months=1)
    elif recurrence_pattern == 'yearly':
        return current_due_date + relativedelta(years=1)
    else:
        # Default to returning the same date if recurrence pattern is not recognized
        return current_due_date

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
