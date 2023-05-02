from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, Http404
from .forms import *
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect, get_object_or_404

# Create your views here.

# Home Page
def home(request):
    return render(request, 'urec_app/home.html')

# Accident Ticket Page
def accident(request):
    return render(request, 'urec_app/accident.html')

# Create Accident Ticket
# def create_accident_ticket(request):
#     if request.method == "POST":
#         accident_ticket = Accident_Ticket_Form(request.POST)
#         injury_type = Accident_Ticket_Injury_Form(request.POST)
#         contact_info = Accident_Ticket_Contact_Info_Form(request.POST)
#         if accident_ticket.is_valid() and injury_type.is_valid() and contact_info.is_valid():
#             accident_instance = accident_ticket.save(commit=False)
#             injury_instance = injury_type.save(commit=False)
#             contact_instance = contact_info.save(commit=False)
#             accident_instance.save()
#             injury_instance.accident_ticket = accident_instance
#             injury_instance.save()
#             contact_instance.accident_ticket = accident_instance
#             contact_instance.save()
#
#             return redirect('accident')
#             # accident_ticket = Accident_Ticket_Form()
#             # injury_type = Accident_Ticket_Injury_Form()
#             # contact_info = Accident_Ticket_Contact_Info_Form()
#     else:
#         accident_ticket = Accident_Ticket_Form()
#         injury_type = Accident_Ticket_Injury_Form()
#         contact_info = Accident_Ticket_Contact_Info_Form()
#     context = { 'accident_ticket': accident_ticket, 'injury_type': injury_type, 'contact_info': contact_info}
#     return render(request, 'urec_app/create_accident_ticket.html', context)


class CreateAccidentTicket(TemplateView):
    template_name = "urec_app/create_accident_ticket.html"

    def get(self, *args, **kwargs):
        formset = AccidentTicketInjury(queryset=Accident_Ticket_Injury.objects.none())
        accident_ticket = Accident_Ticket_Form()
        patient = Accident_Ticket_Contact_Patient_Form()
        witness = Accident_Ticket_Contact_Witness_Form()
        context = {
            'accident_ticket': accident_ticket,
            'accident_ticket_injury_formset': formset,
            'patient': patient,
            'witness': witness,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        accident_ticket = Accident_Ticket_Form(data=self.request.POST)
        injury_type = AccidentTicketInjury(data=self.request.POST)
        patient = Accident_Ticket_Contact_Patient_Form(data=self.request.POST)
        witness = Accident_Ticket_Contact_Witness_Form(data=self.request.POST)

        if accident_ticket.is_valid() and injury_type.is_valid() and patient.is_valid() and witness.is_valid():
            accident_instance = accident_ticket.save(commit=False)
            injury_instance = injury_type.save(commit=False)
            patient_instance = patient.save(commit=False)
            witness_instance = witness.save(commit=False)
            accident_instance.save()
            for i in injury_instance:
                i.accident_ticket = accident_instance
                i.save()

            patient_instance.accident_ticket = accident_instance
            patient_instance.save()
            witness_instance.patient = patient_instance
            witness_instance.accident_ticket = accident_instance
            witness_instance.save()

            return redirect('home')

        return self.render_to_response({'accident-ticket-injury-formset': injury_type})


# View all Accident Tickets
def view_accident_tickets(request):
    accident_ticket = Accident_Ticket.objects.all()
    injury_type = Accident_Ticket_Injury.objects.all()
    patient = Accident_Ticket_Contact_Patient.objects.all()

    context = {'accident_ticket': accident_ticket, 'injury_type': injury_type, 'contact_info': patient}
    return render(request, 'urec_app/view_accident_tickets.html', context)

def edit_accident_id(request):
    if request.method == 'POST':
        var = request.POST['id']
        acc_id = Accident_Ticket.objects.filter(ticket_id=var)
        injury_type = Accident_Ticket_Injury.objects.filter(accident_ticket=acc_id[0])
        patient = Accident_Ticket_Contact_Patient.objects.filter(accident_ticket=acc_id[0])
        context = {'var': var, 'acc_id': acc_id, 'injury_type': injury_type,'contact_info': patient}
    return render(request,'urec_app/edit_accident_id.html', context)

# Counts Page
def count(request):
    return render(request, 'urec_app/count.html')

# Update Count in Facilities
def count_update(request):
    if request.method == 'POST':
        count_form = CountFormSet(request.POST)
        if count_form.is_valid():
            count_form.save()

            return redirect('count')
    count_form = CountFormSet(queryset=Count.objects.none())

    context = {'count_form': count_form}
    return render(request, 'urec_app/count_update.html', context)

# View All Count History
def count_view_history(request):
    count_item = Count.objects.all()
    context = {'count_item': count_item}
    return render(request, 'urec_app/count_view_history.html', context)

# ERP Page
def erp(request):
    return render(request, 'urec_app/erp.html')
    # return erp_pdf('Example PDF 1')
    # return erp_pdf('accidentreport')

    # try:
    #     return FileResponse(open('urec_app/documents/Example PDF 1.pdf', 'rb'), content_type='application/pdf')
    #     #return FileResponse(open('urec_app/documents/accidentreport.pdf', 'rb'), content_type='application/pdf')
    # except FileNotFoundError:
    #     raise Http404()

# def erp_pdf(pdf_name):
#     file_name = 'urec_app/documents/' + pdf_name + '.pdf'
#     open_file = open(file_name, 'rb')
#     try:
#         return FileResponse(open_file, content_type='application/pdf')
#         # return FileResponse(open('urec_app/documents/accidentreport.pdf', 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404()

def form(request):
    return render(request, 'urec_app/form.html')

# Incident Ticket Page
def incident(request):
    return render(request, 'urec_app/incident.html')

# Create Incident Ticket
# def create_incident_ticket(request):
#     if request.method == "POST":
#         incident_ticket = Incident_Ticket_Form(request.POST)
#         incident_type = Incident_Ticket_Incident_Form(request.POST)
#         contact_info = Incident_Ticket_Contact_Info_Form(request.POST)
#         if incident_ticket.is_valid() and incident_type.is_valid() and contact_info.is_valid():
#             incident_instance = incident_ticket.save(commit=False)
#             incident_type_instance = incident_type.save(commit=False)
#             contact_instance = contact_info.save(commit=False)
#             incident_instance.save()
#             incident_type_instance.incident_ticket = incident_instance
#             incident_type_instance.save()
#             contact_instance.incident_ticket = incident_instance
#             contact_instance.save()
#
#             return redirect('incident')
#             # incident_ticket = Incident_Ticket_Form()
#             # incident_type = Incident_Ticket_Incident_Form()
#             # contact_info = Incident_Ticket_Contact_Info_Form()
#     else:
#         incident_ticket = Incident_Ticket_Form()
#         incident_type = Incident_Ticket_Incident_Form()
#         contact_info = Incident_Ticket_Contact_Info_Form()
#     context = { 'incident_ticket': incident_ticket, 'incident_type': incident_type, 'contact_info': contact_info}
#     return render(request, 'urec_app/create_incident_ticket.html', context)


class CreateIncidentTicket(TemplateView):
    template_name = "urec_app/create_incident_ticket.html"

    def get(self, *args, **kwargs):
        formset = IncidentTicketIncidentForm(queryset=Incident_Ticket_Incident.objects.none())
        incident_ticket = Incident_Ticket_Form()
        patient_contact = Incident_Ticket_Contact_Patient_Form()
        witness_contact = Incident_Ticket_Contact_Witness_Form()

        context = {
            'incident_ticket': incident_ticket,
            'incident_type_formset': formset,
            'patient_contact': patient_contact,
            'witness_contact': witness_contact,
        }
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        incident_ticket = Incident_Ticket_Form(data=self.request.POST)
        incident_type = IncidentTicketIncidentForm(data=self.request.POST)
        patient_contact = Incident_Ticket_Contact_Patient_Form(data=self.request.POST)
        witness_contact = Incident_Ticket_Contact_Witness_Form(data=self.request.POST)

        if incident_ticket.is_valid() and incident_type.is_valid() \
                and patient_contact.is_valid() and witness_contact.is_valid():

            ticket_instance = incident_ticket.save(commit=False)
            type_instance = incident_type.save(commit=False)
            patient_instance = patient_contact.save(commit=False)
            witness_instance = witness_contact.save(commit=False)
            ticket_instance.save()
            for i in type_instance:
                i.incident_ticket = ticket_instance
                i.save()

            patient_instance.incident_ticket = ticket_instance
            patient_instance.save()
            witness_instance.incident_ticket = ticket_instance
            witness_instance.patient = patient_instance
            witness_instance.save()

            return redirect('home')

        return self.render_to_response({'incident_type_formset': incident_type})


# View all Incident Tickets
def view_incident_tickets(request):
    incident_ticket = Incident_Ticket.objects.all()
    incident_type = Incident_Ticket_Incident.objects.all()
    patient_contact = Incident_Ticket_Contact_Patient.objects.all()

    context = {'incident_ticket': incident_ticket, 'incident_type': incident_type, 'patient_contact': patient_contact}
    return render(request, 'urec_app/view_incident_tickets.html', context)

def view_incident_id(request):
    if request.method == 'POST':
        var = request.POST['id']
        inc_id = Incident_Ticket.objects.filter(ticket_id=var)
        incident_type = Incident_Ticket_Incident.objects.filter(incident_ticket=inc_id[0])
        patient_contact = Incident_Ticket_Contact_Patient.objects.filter(incident_ticket=inc_id[0])
        context = {'var': var, 'inc_id': inc_id, 'incident_type': incident_type, 'patient_contact': patient_contact}
    return render(request, 'urec_app/view_incident_id.html', context)

def sop(request):
    return render(request, 'urec_app/sop.html')

# Task Page
def task(request):
    return render(request, 'urec_app/task.html')

# Create New Task
def create_task(request):
    if request.method == "POST":
        task_obj = Task_Form(request.POST)
        if task_obj.is_valid():
            task_obj.pk = None
            task_obj.save()
        # task_obj = Task_Form(request.POST)
        # if task_obj.is_valid():
        #     task_obj.pk = None
        #     task_obj.save()
        # task_obj = Task_Form(request.POST)
        # if task_obj.is_valid():
        #     task_obj.pk = None
        #     task_obj.save()

            return redirect('task')
    else:
        task_obj = Task_Form()
    context = {'task_obj': task_obj}
    return render(request, 'urec_app/create_task.html', context)

# View All Created Tasks reguardless of completion
def all_tasks(request):
    task_item = Task.objects.all()

    context = {'task_item': task_item}
    return render(request, 'urec_app/all_tasks.html', context)
def view_task_id(request):
    if request.method == 'POST':
        var = request.POST['id']
        task_id = Task.objects.filter(task_id=var)
        context = {'var': var, 'task_id': task_id}
    return render(request,'urec_app/task_id.html', context)
def survey(request):
    return render(request, 'urec_app/survey.html')
