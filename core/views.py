from django.shortcuts import render
from .forms import RegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Household, Member, Chore
from .forms import ChoreForm


# Create your views here.

def landing_page(request):
    return render(
        request,
        'core/landing.html',        
    )

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing_page')
    else:
        form = RegistrationForm()

    return render(
        request,
        'core/registration.html',
        {'form': form}
    )

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing_page')
    else:
        form = AuthenticationForm()

    return render(
        request,
        'core/login.html',
        {'form': form}
    )

def user_logout(request):
    logout(request)
    return redirect('landing_page')

@login_required
def dashboard(request):

    household_count = Household.objects.count()
    member_count = Member.objects.count()
    chore_count = Chore.objects.count()

    context = {
        'household_count': household_count,
        'member_count': member_count,
        'chore_count': chore_count,
        'recent_chores': Chore.objects.all()[:5], # Show last 5 chores
        'recent_members': Member.objects.all()[:5],  # Show last 5 members
    }
    return render(
        request,
        'core/dashboard.html',
        context
    )

@login_required
def members(request):
    members = Member.objects.all()
    context = {
        'members': members,
    }
    return render(
        request,
        'core/members.html',
        context
    )

@login_required
def chores(request):
    chores = Chore.objects.all()
    context = {
        'chores': chores,
    }
    return render(
        request,
        'core/chores.html',
        context
    )

@login_required
def add_chore(request):
    if request.method == 'POST':
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chores')
    else:
        form = ChoreForm()
    return render(
        request,
        'core/add_chore.html',
        {'form': form}
    )

@login_required
def edit_chore(request, chore_id):

    chore = Chore.objects.get(id=chore_id)

    if request.method == "POST":
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            form.save()
            return redirect('chores')
    else:
        form = ChoreForm(instance=chore)

    return render(request, "core/edit_chore.html", {'form': form, 'chore': chore})

@login_required
def delete_chore(request, chore_id):

    chore = Chore.objects.get(id=chore_id)

    if request.method == "POST":
        chore.delete()
        return redirect('chores')

    return render(request, "core/delete_chore.html", {'chore': chore})
