from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Member, GymClass, ClassRegistration, Attendance, GymEvent, SpecialHours, Instructor
from datetime import date, timedelta
import calendar
from .forms import MemberSignupForm, AttendanceForm, MemberRegistrationForm, ProfileForm


def home(request):
    total_members = Member.objects.filter(is_active=True).count()
    total_classes = GymClass.objects.filter(is_active=True).count()
    recent_members = Member.objects.filter(is_active=True)[:5]
    return render(request, 'gym/home.html', {
        'total_members': total_members,
        'total_classes': total_classes,
        'recent_members': recent_members,
    })


def member_signup(request):
    if request.method == 'POST':
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'Welcome {member.first_name}! Your membership has been created.')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberSignupForm()
    return render(request, 'gym/member_signup.html', {'form': form})


def member_list(request):
    members = Member.objects.filter(is_active=True)
    return render(request, 'gym/member_list.html', {'members': members})


def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    registrations = member.registrations.filter(is_cancelled=False)
    attendance = member.attendance_records.all()[:10]
    return render(request, 'gym/member_detail.html', {
        'member': member,
        'registrations': registrations,
        'attendance': attendance,
    })


def class_schedule(request):
    classes = GymClass.objects.filter(is_active=True)
    for gym_class in classes:
        gym_class.instructor_obj = Instructor.objects.filter(name=gym_class.instructor).first()
    return render(request, 'gym/class_schedule.html', {'classes': classes})


def class_detail(request, pk):
    gym_class = get_object_or_404(GymClass, pk=pk)
    gym_class.instructor_obj = Instructor.objects.filter(name=gym_class.instructor).first()
    registrations = gym_class.registrations.filter(is_cancelled=False)
    return render(request, 'gym/class_detail.html', {
        'gym_class': gym_class,
        'registrations': registrations,
    })


@login_required
def class_register(request, pk):
    gym_class = get_object_or_404(GymClass, pk=pk)
    
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.error(request, 'No member profile found. Please contact support.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            registration = ClassRegistration.objects.get(member=member, gym_class=gym_class)
            if registration.is_cancelled:
                if gym_class.spots_available() > 0:
                    registration.is_cancelled = False
                    registration.save()
                    messages.success(request, f'Successfully re-registered for {gym_class.name}!')
                    return redirect('class_detail', pk=gym_class.pk)
                else:
                    messages.error(request, 'Sorry, this class is full.')
            else:
                messages.info(request, 'You are already registered for this class.')
                return redirect('class_detail', pk=gym_class.pk)
        except ClassRegistration.DoesNotExist:
            if gym_class.spots_available() > 0:
                ClassRegistration.objects.create(
                    member=member,
                    gym_class=gym_class,
                    is_cancelled=False
                )
                messages.success(request, f'Successfully registered for {gym_class.name}!')
                return redirect('class_detail', pk=gym_class.pk)
            else:
                messages.error(request, 'Sorry, this class is full.')
    
    is_registered = ClassRegistration.objects.filter(member=member, gym_class=gym_class, is_cancelled=False).exists()
    return render(request, 'gym/class_register.html', {'gym_class': gym_class, 'member': member, 'is_registered': is_registered})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome to GymPlace! Your account has been created.')
                return redirect('dashboard')
    else:
        form = MemberRegistrationForm()
    return render(request, 'gym/register.html', {'form': form})


@login_required
def dashboard(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        member = None
    
    classes = GymClass.objects.filter(is_active=True)[:6]
    
    if member:
        registrations = member.registrations.filter(is_cancelled=False)[:5]
        recent_checkins = member.attendance_records.all()[:5]
    else:
        registrations = []
        recent_checkins = []
    
    return render(request, 'gym/dashboard.html', {
        'member': member,
        'classes': classes,
        'registrations': registrations,
        'recent_checkins': recent_checkins,
    })


@login_required
def check_in(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.error(request, 'No member profile found. Please contact support.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        Attendance.objects.create(member=member)
        messages.success(request, f'Welcome {member.first_name}! Checked in successfully.')
        return redirect('dashboard')
    
    recent_checkins = member.attendance_records.all()[:10]
    return render(request, 'gym/check_in.html', {
        'member': member,
        'recent_checkins': recent_checkins,
    })


@login_required
def profile(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.error(request, 'No member profile found. Please contact support.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            request.user.first_name = member.first_name
            request.user.last_name = member.last_name
            request.user.email = member.email
            request.user.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=member)
    
    return render(request, 'gym/profile.html', {
        'member': member,
        'form': form,
    })


def gym_info(request):
    today = date.today()
    year = today.year
    month = today.month
    
    upcoming_events = GymEvent.objects.filter(date__gte=today, is_active=True)[:10]
    special_hours = SpecialHours.objects.filter(date__gte=today)[:10]
    
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdatescalendar(year, month)
    
    calendar_weeks = []
    for week in month_days:
        week_days = []
        for day in week:
            day_info = {
                'date': day,
                'is_today': day == today,
                'is_current_month': day.month == month,
                'events': GymEvent.objects.filter(date=day, is_active=True),
                'special': SpecialHours.objects.filter(date=day).first(),
            }
            week_days.append(day_info)
        calendar_weeks.append(week_days)
    
    month_name = calendar.month_name[month]
    
    regular_hours = [
        {'day': 'Monday - Friday', 'hours': '5:00 AM - 11:00 PM'},
        {'day': 'Saturday', 'hours': '6:00 AM - 10:00 PM'},
        {'day': 'Sunday', 'hours': '6:00 AM - 10:00 PM'},
    ]
    
    return render(request, 'gym/gym_info.html', {
        'upcoming_events': upcoming_events,
        'special_hours': special_hours,
        'calendar_weeks': calendar_weeks,
        'month_name': month_name,
        'year': year,
        'regular_hours': regular_hours,
    })


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def instructors(request):
    instructors_list = Instructor.objects.all()
    return render(request, 'gym/instructors.html', {'instructors': instructors_list})
