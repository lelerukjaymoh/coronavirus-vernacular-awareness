from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RecipientForm, VolunteerForm, DonationForm, MessageForm, VernacularMessageForm
from .models import Language, Volunteer, Donation, Recipient, Message, VernacularMessage, SMSDonation

from .sms import SMS
from datetime import datetime

def index(request):
    if request.method == "POST":
        # recipient form
        language = request.POST.get('language')
        form = RecipientForm(request.POST)
        if form.is_valid():
            phone = '+254'+request.POST['phone_number'][-9:]
            if Recipient.objects.filter(phone_number = phone).exists():
                messages.add_message(request, messages.SUCCESS, 'You had previously subscribed. You will be receiving notifications at 10 am everyday. If you think this is an error please contact 0717771518 to rectify that')
                return redirect('index')

            else:
                form = form.save(commit=False)
                language = Language.objects.get(language=language)
                form.language = language
                form.phone_number = phone
                form.save()
                messages.add_message(request, messages.SUCCESS, 'You have subscribed to notifications. You will receive coronavirus information everyday at around 10 am')
                return redirect('index')

        # volunteer form
        form = VolunteerForm(request.POST)
        if form.is_valid():
            phone = '+254'+request.POST['phone'][-9:]
            if Volunteer.objects.filter(phone = phone).exists():
                messages.add_message(request, messages.SUCCESS, 'You had already volunteered. If you think this is an error please contact 0717771518 to rectify that')
                return redirect('index')

            else:
                form = form.save(commit=False)
                print(phone)
                form.phone = phone
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Thanks for joining, let us fight this pandemic together')
                return redirect('index')
                
    else:
        form = RecipientForm
        form = VolunteerForm
        form = DonationForm

    languages = Language.objects.all()
    subscribers = Recipient.objects.all().count()
    sent_messages = VernacularMessage.objects.filter(sent=True).count()
    donations = Donation.objects.all().count()
    languages_count = Language.objects.all().count()
    volunteers = Volunteer.objects.all().count()
    languages = Language.objects.all()

    context = {"RecipientForm": RecipientForm, 'subscribers': subscribers, 'donations': donations, 
    'sent_messages': sent_messages, 'VolunteerForm': VolunteerForm, 'DonationForm': DonationForm, 
    'languages': languages, 'volunteers': volunteers, 'languages_count': languages_count}
    return render(request, 'index.html', context)

@login_required
def jay(request):
    if request.method == 'POST':
        # donor form
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        # Main message form
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

        #vernacular message form
        form = VernacularMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') 

    else:
        form = DonationForm
        form = MessageForm
        form = VernacularMessageForm
    
        
    volunteers = Volunteer.objects.all()
    languages = Language.objects.all()
    donations = SMSDonation.objects.all()
    recipients = Recipient.objects.all()
    messages = Message.objects.all()
    messages = Message.objects.all()
    vernacular_messages = VernacularMessage.objects.all()

    context = {
        'DonationForm': DonationForm,
        'MessageForm': MessageForm,
        'VernacularMessageForm': VernacularMessageForm,
        'volunteers': volunteers,
        'messages': messages,
        'languages': languages,
        'donations': donations,
        'recipients': recipients,
        'vernacular_messages': vernacular_messages,
    }
    return render(request, 'jay.html', context)

def send_messages(request):
    languages = Language.objects.all()
    for language in languages:
        recipient = Recipient.objects.filter(language=language)
        messages = VernacularMessage.objects.filter(language__language=language)
        print(recipient,messages)
        for each in recipient:
            phone = []
            phone.append(each.phone_number)
            for message in messages:
                message = message.message
                sms = SMS()
                response = sms.send(phone, message)
                response_status = response['SMSMessageData']['Recipients'][0]['status']
                if response_status == 'Success':
                    VernacularMessage.objects.filter(message=message).update(sent=True)
                    recipient = Recipient.objects.filter(phone_number=each.phone_number)
                    for each in recipient:
                        each.date_sent = timezone.now()
                        each.save()
                        count = each.sent_messages
                        count += 1
                        recipient.update(sent_messages=count)
                
    return HttpResponse('<h4 class="text-success">Currently sending SMS</h>')

def notify_volunteers(request):
    message = Message.objects.get(status=True)
    volunteers = Volunteer.objects.all()
    print(volunteers)
    for volunteer in volunteers:        
        phone = []
        phone.append(volunteer.phone)
        print(phone, message)
        sms = SMS()
        response = sms.send(phone, message)
        response_status = response['SMSMessageData']['Recipients'][0]['status']
        if response_status == 'Success':
            volunteer.date_sent = timezone.now()
            volunteer.save()


    return HttpResponse('<h4 class="text-success">Notifying volunteers</h>')

def translate(request):
    main_message = Message.objects.get(status=True)
    print(main_message.id)
    if request.method == 'POST':
        print(request.POST)
        # Translation form
        form = VernacularMessageForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.main_message = main_message
            form.save()
            return redirect('validate')

    else:
        form = VernacularMessageForm

    languages = Language.objects.all()

    context = {
        'VernacularMessageForm': VernacularMessageForm,
        'languages': languages,
        'main_message': main_message.message
    }
    return render(request, 'translate.html', context)

def validate(request):
    if request.method == "POST":
        if 'correct' in request.POST:
            message = request.POST.get('message')
            correct = request.POST.get('correct')

            message = VernacularMessage.objects.get(id=message)
            if message.correct == False:
                messages.add_message(request, messages.SUCCESS, 'This message had already been marked as wrong If you have a better translation in that language submit it at the translate page')
                return redirect('validate')

            else:
                VernacularMessage.objects.filter(id=message).update(correct=False)
                messages.add_message(request, messages.SUCCESS, 'You have marked a translation as being wrong, If you have a better translation in that language submit it at the translate page')
                return redirect('validate')

    vernacular_messages = VernacularMessage.objects.all()
    context = {'vernacular_messages': vernacular_messages}
    return render(request, 'validate.html', context)
