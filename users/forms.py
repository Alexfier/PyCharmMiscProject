from django.contrib.auth.forms import UserCreationForm
from django.db import models
from users.models import User


class UserRegisterForms(UserCreationForm):

    class Meta:

        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForms, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })