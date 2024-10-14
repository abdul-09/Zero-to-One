import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponse

# from .tasks import email_users
from .forms import BulkEmailForm
from django.conf import settings
from django.contrib import messages
from .models import Resource, TrainingSchedule, User, InterestedTopic

# Register your models here.

# @admin.action(description='Send bulk email to selected users')
# def send_bulk_email(modeladmin, request, queryset):
#     # You can customize this subject and message as needed
#     subject = 'Update from Zero to One Farming'
#     message = 'Hello, we have important updates for you from the Zero to One: Farming for the Future campaign!'
    
#     # Get email addresses of the selected users
#     recipient_list = list(queryset.values_list('email', flat=True))
    
#     # Send the email
#     send_mail(
#         subject,
#         message,
#         'no-reply@zero-to-one-farming.com',  # From email address
#         recipient_list,  # To email addresses
#         fail_silently=False,
#     )
    
#     # Display a message in the admin interface after sending emails
#     modeladmin.message_user(request, f'Emails have been sent to {len(recipient_list)} users.')

@admin.action(description='Export selected users to CSV')
def export_users_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Full Name', 'Email', 'Location', 'Experience Level'])

    for user in queryset:
        writer.writerow([user.id, user.full_name, user.email, user.location, user.experience_level])

    return response


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'location', 'experience_level')
    search_fields = ('full_name', 'email')
    actions = ['send_bulk_email', export_users_to_csv]


    @admin.action(description='Send bulk email to selected users')
    def send_bulk_email(self, request, queryset):
        """Admin action to send bulk emails with a form for subject and message."""
        
        if 'apply' in request.POST:
            form = BulkEmailForm(request.POST)
            if form.is_valid():
                users = form.cleaned_data['users']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                email_users.delay(users, subject, message)
                messages.success(request, f'Emails sent to {queryset.count()} users.')
                return redirect('admin:users_user_changelist')
        else:
            form = BulkEmailForm(initial={'users': queryset})

        return render(request, 'admin/send_bulk_email.html', {'form': form, 'users': queryset})

    send_bulk_email.short_description = "Send email to selected users"

admin.site.register(User, UserAdmin)
admin.site.register(InterestedTopic)
admin.site.register(Resource)
admin.site.register(TrainingSchedule)
