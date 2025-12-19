# GymPlace - Gym Management System

## Overview
A Django web application that transforms a paper-based gym signup system into a modern digital platform. Members can create accounts, log in, sign up for classes, and check in at the gym. Staff can manage everything through the Django admin interface.

## Project Status
- **Status**: Development
- **Created**: November 17, 2025
- **Framework**: Django 5.2.8
- **Python**: 3.11
- **Branding**: GymPlace with vibrant sky blue/white color scheme

## Recent Changes
- **December 9, 2025**: Added Meet Our Instructors page
  - Created Instructor model with bio, certifications, experience
  - Built instructors page at `/instructors/` with all staff profiles
  - Instructor names in class schedule and class detail link to their profile
  - Added 5 sample instructors (Sarah, Marcus, Elena, David, Amanda)
  - Added Instructors link to navigation dropdown

- **December 9, 2025**: Added user authentication system
  - Implemented user registration with linked Member profiles
  - Added login/logout functionality with Django auth
  - Created member dashboard with class schedules, gym hours, and check-in history
  - Check-in now requires login (no more email lookup)
  - Updated navigation to show different options for logged-in vs anonymous users
  - Redesigned UI with "GymPlace" branding
  - Made Quick Check-In button prominent on home page

- **November 17, 2025**: Initial project setup
  - Created Django project and gym app
  - Implemented Member, GymClass, ClassRegistration, and Attendance models
  - Built all views and templates with Bootstrap 5
  - Configured admin interface for staff management
  - Added sample gym classes to database

## Features
### User Authentication
- Account registration with username/password
- Login/logout functionality
- Member profiles linked to user accounts
- Protected routes requiring authentication

### Member Dashboard
- Personalized welcome with membership info
- One-click check-in button
- Class schedule access
- Gym hours display (Mon-Fri: 5AM-11PM, Sat-Sun: 6AM-10PM)
- Registered classes list
- Recent check-in history

### Class Management
- Class schedule display showing all available gym classes
- Class registration system with capacity limits
- Registration tracking per member
- Admin interface for managing classes

### Attendance System
- One-click check-in for logged-in members
- Check-in history per member
- Attendance tracking in admin

### Admin Dashboard
- Full admin interface at `/admin/`
- Manage members, classes, registrations, and attendance
- Searchable and filterable lists

## Project Architecture
### Database Models
- **Member**: Stores member information, membership type, status, and linked User account
- **Instructor**: Instructor profiles with bio, specialty, certifications, experience
- **GymClass**: Gym class details including schedule, instructor, and capacity
- **ClassRegistration**: Links members to classes they've registered for
- **Attendance**: Tracks member check-ins and check-outs
- **GymEvent**: Events like workshops, competitions, special classes
- **SpecialHours**: Holiday closures and modified hours

### URL Structure
- `/` - Home page with Quick Check-In button
- `/register/` - New member registration (creates account)
- `/login/` - User login
- `/logout/` - User logout
- `/dashboard/` - Member dashboard (requires login)
- `/classes/` - Class schedule
- `/classes/<id>/` - Class detail
- `/classes/<id>/register/` - Register for class
- `/check-in/` - Member check-in (requires login)
- `/instructors/` - Meet Our Instructors page
- `/info/` - Gym info (hours, calendar, events)
- `/admin/` - Admin interface

### Technology Stack
- **Backend**: Django 5.2.8, Python 3.11
- **Authentication**: Django built-in auth
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, Django Templates
- **Icons**: Bootstrap Icons

## Running the Project
The Django development server runs automatically on port 5000 via the configured workflow.

### Creating an Admin User
```bash
python manage.py createsuperuser
```

### Populating Sample Data
Sample gym classes are already loaded. To reload:
```bash
python populate_data.py
```

## File Structure
```
gymapp/             - Main Django project
├── settings.py     - Django settings (includes auth config)
├── urls.py         - Main URL routing
└── wsgi.py         - WSGI config

gym/                - Gym application
├── models.py       - Database models (Member linked to User)
├── views.py        - View functions (auth views included)
├── forms.py        - Django forms (registration form)
├── admin.py        - Admin configuration
├── urls.py         - App URL routing
└── templates/      - HTML templates
    └── gym/
        ├── base.html       - Base template with nav
        ├── home.html       - Home page
        ├── login.html      - Login page
        ├── register.html   - Registration page
        ├── dashboard.html  - Member dashboard
        ├── check_in.html   - Check-in page
        ├── class_*.html    - Class related pages
        └── member_*.html   - Member pages (admin use)

populate_data.py    - Script to populate sample classes
manage.py           - Django management script
```

## User Preferences
- Clean, minimal interface focused on three main features: Join, Classes, Check In
- Remove descriptive/marketing text, keep interface clean
- GymPlace branding with orange/navy gradient theme
- Big, obvious Quick Check-In button

## Next Steps
- Add email notifications for class confirmations
- Implement class capacity limits and waitlists
- Add member profile editing
- Create reports and analytics
- Add payment tracking
- Implement membership renewal system
