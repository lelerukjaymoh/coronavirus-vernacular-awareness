from django.contrib import admin
from .models import Recipient, Language, Donation, Volunteer, Message, VernacularMessage, SMSDonation, SMSBalance

admin.site.register(Recipient)
admin.site.register(Language)
admin.site.register(Donation)
admin.site.register(Volunteer)
admin.site.register(Message)
admin.site.register(VernacularMessage)
admin.site.register(SMSDonation)
admin.site.register(SMSBalance)
