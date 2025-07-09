# helpdesk/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import TicketForm
from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden

def home(request):
    return render(request, 'helpdesk/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'helpdesk/register.html', {'form': form})





@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'helpdesk/create_ticket.html', {'form': form})



@login_required
def user_dashboard(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'helpdesk/user_dashboard.html', {'tickets': tickets})




@staff_member_required
def admin_dashboard(request):
    tickets = Ticket.objects.all().order_by('-created_at')

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        new_status = request.POST.get('status')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = new_status
            ticket.save()
        except Ticket.DoesNotExist:
            return HttpResponseForbidden("Ticket not found.")

    return render(request, 'helpdesk/admin_dashboard.html', {'tickets': tickets})
