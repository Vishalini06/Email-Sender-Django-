from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import EmailForm
from django.conf import settings

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # Split the recipients input by commas
            recipients = [email.strip() for email in form.cleaned_data['recipients'].split(',')]
            attachment = request.FILES.get('attachment')

            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)

            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)

            try:
                # Send the email
                email.send()
                # Add success message to be shown to the user
                messages.success(request, 'Email sent successfully to ' + ', '.join(recipients))
            except Exception as e:
                messages.error(request, f"Failed to send email. Error: {str(e)}")
        else:
            messages.error(request, 'There was an error in the form. Please check the fields.')

    else:
        form = EmailForm()

    return render(request, 'index.html', {'form': form})
