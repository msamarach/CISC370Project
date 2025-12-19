from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Member(models.Model):
    MEMBERSHIP_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('platinum', 'Platinum'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='basic')
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-date_joined']


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    bio = models.TextField()
    years_experience = models.IntegerField(default=1)
    certifications = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    photo = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class GymClass(models.Model):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    day_of_week = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    capacity = models.IntegerField(default=20)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_day_of_week_display()} {self.start_time}"
    
    def current_registrations(self):
        return self.registrations.filter(is_cancelled=False).count()
    
    def spots_available(self):
        return self.capacity - self.current_registrations()
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'


class ClassRegistration(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='registrations')
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(default=timezone.now)
    is_cancelled = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.member} - {self.gym_class}"
    
    class Meta:
        ordering = ['-registered_at']
        unique_together = ['member', 'gym_class']


class Attendance(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendance_records')
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.member} - {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-check_in_time']


class GymEvent(models.Model):
    EVENT_TYPES = [
        ('event', 'Event'),
        ('workshop', 'Workshop'),
        ('competition', 'Competition'),
        ('special', 'Special Class'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='event')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    class Meta:
        ordering = ['date', 'start_time']


class SpecialHours(models.Model):
    CLOSURE_TYPES = [
        ('holiday', 'Holiday'),
        ('closure', 'Closure'),
        ('modified', 'Modified Hours'),
    ]
    
    date = models.DateField()
    closure_type = models.CharField(max_length=20, choices=CLOSURE_TYPES, default='holiday')
    title = models.CharField(max_length=100)
    is_closed = models.BooleanField(default=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Special Hours'
        verbose_name_plural = 'Special Hours'
