# helpdesk/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import TicketForm
from .models import Ticket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

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
