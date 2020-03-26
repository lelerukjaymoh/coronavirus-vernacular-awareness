from django.db import models
from django.utils import timezone

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language

class SMSDonation(models.Model):
    amount = models.IntegerField()

    def __str__(self):
        return str(self.amount)

class Recipient(models.Model):
    phone_number = models.CharField(max_length=50)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="recipients")
    sent_messages = models.IntegerField(default=0)
    date_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.phone_number

class Donation(models.Model):
    donor = models.CharField(max_length=100)
    amount = models.IntegerField()
    phone_number = models.IntegerField()

    def __str__(self):
        return self.donor

class Volunteer(models.Model):
    names = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    date_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.names

class Message(models.Model):
    language = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.message

class VernacularMessage(models.Model):
    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name="vernacularlanguages")
    main_message = models.ForeignKey(Message, on_delete=models.PROTECT, related_name="vernacularmessages")
    message = models.TextField(max_length=500)
    sent = models.BooleanField(default=False)
    correct = models.BooleanField(default=True)

    def __str__(self):
        return str(self.language)

class SMSBalance(models.Model):
    date = models.DateTimeField()
    balance = models.CharField(max_length=100, default=0)

    def __str__(self):
        return self.balance
