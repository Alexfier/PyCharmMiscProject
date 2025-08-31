from django import forms

from .models import Mailing, Message, Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["full_name"].widget.attrs.update({"class": "form-control"})
        self.fields["comment"].widget.attrs.update({"class": "form-control"})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["topic", "text"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["topic"].widget.attrs.update({"class": "form-control"})
        self.fields["text"].widget.attrs.update({"class": "form-control"})


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("message", "recipients",)

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({"class": "form-control"})
        self.fields["recipients"].widget.attrs.update({"class": "form-control"})
