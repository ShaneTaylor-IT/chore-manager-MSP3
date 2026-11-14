from django.shortcuts import render
from .forms import RegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Household, Member, Chore
from .forms import ChoreForm, MemberForm


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

    weekly_summary = {
    'Monday': {'assigned': 0, 'completed': 0},
    'Tuesday': {'assigned': 0, 'completed': 0},
    'Wednesday': {'assigned': 0, 'completed': 0},
    'Thursday': {'assigned': 0, 'completed': 0},
    'Friday': {'assigned': 0, 'completed': 0},
    'Saturday': {'assigned': 0, 'completed': 0},
    'Sunday': {'assigned': 0, 'completed': 0}
}

    for chore in Chore.objects.all():

        day_of_week = chore.due_date.strftime('%A')

        weekly_summary[day_of_week]['assigned'] += 1

    if chore.completed:
        weekly_summary[day_of_week]['completed'] += 1

    current_member = Member.objects.filter(user=request.user).first()
    
    context = {
        'household_count': household_count,
        'member_count': member_count,
        'chore_count': chore_count,
        'recent_chores': Chore.objects.all()[:5], # Show last 5 chores
        'recent_members': Member.objects.all()[:5],  # Show last 5 members
        'weekly_summary': weekly_summary,
        'current_member': current_member,
    }
    return render(
        request,
        'core/dashboard.html',
        context
    )

@login_required
def members(request):
    members = Member.objects.exclude(user=request.user)  # Exclude the current user from the list
    current_member = Member.objects.filter(user=request.user).first()  # Get the current member object for the logged-in user
    # After checking stack overflow, I found that the best way to get the current member object is to filter the Member model by the logged-in user and then use .first() to get the first result. 
    # This will return None if no member is found for the logged-in user, which is a safe way to handle this situation. Over the .get() method, which would raise an exception if no member is found.
    # I chose to use this method after creating a new superuser and while logged in as that super user, I tried to go to the members page with the .get() mothod and got an error message.
    context = {
        'members': members,
        'current_member': current_member
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

@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("members")
    else:
        form = MemberForm()

    return render(
        request, "core/add_member.html", {'form': form}
    )

@login_required
def edit_member(request, member_id):
    member = Member.objects.get(id=member_id)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members')
    else:
        form = MemberForm(instance=member)

    return render(request, "core/edit_member.html", {'form': form, 'member': member})

@login_required
def delete_member(request, member_id):
    member = Member.objects.get(id=member_id)

    if request.method == "POST":
        member.delete()
        return redirect('members')

    return render(request, "core/delete_member.html", {'member': member})
