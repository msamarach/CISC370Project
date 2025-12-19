from django.contrib import admin
from .models import Member, GymClass, ClassRegistration, Attendance, GymEvent, SpecialHours, Instructor


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership_type', 'date_joined', 'is_active']
    list_filter = ['membership_type', 'is_active', 'date_joined']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'day_of_week', 'start_time', 'capacity', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['name', 'instructor']


@admin.register(ClassRegistration)
class ClassRegistrationAdmin(admin.ModelAdmin):
    list_display = ['member', 'gym_class', 'registered_at', 'is_cancelled', 'attended']
    list_filter = ['is_cancelled', 'attended', 'registered_at']
    search_fields = ['member__first_name', 'member__last_name', 'gym_class__name']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['member', 'check_in_time', 'check_out_time']
    list_filter = ['check_in_time']
    search_fields = ['member__first_name', 'member__last_name']


@admin.register(GymEvent)
class GymEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'start_time', 'end_time', 'is_active']
    list_filter = ['event_type', 'is_active', 'date']
    search_fields = ['title', 'description']


@admin.register(SpecialHours)
class SpecialHoursAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'closure_type', 'is_closed', 'open_time', 'close_time']
    list_filter = ['closure_type', 'is_closed', 'date']
    search_fields = ['title']


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'years_experience', 'email']
    search_fields = ['name', 'specialty']
