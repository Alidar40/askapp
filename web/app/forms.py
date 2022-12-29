from django import forms
from .models import *
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                                             "placeholder": "Enter your login"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg",
                                                                 "placeholder": "Enter your password"}))


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                                             "placeholder": "dr_pepper"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control form-control-lg",
                                                            "placeholder": "dr.pepper@mail.ru"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg",
                                                                 "placeholder": "Enter your password"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg",
                                                                        "placeholder": "Enter your password again"}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control form-control-lg"}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password != password_repeat:
            self.add_error(None, "Passwords do not match!")
        if User.objects.filter(username=self.cleaned_data.get("username")).exists():
            self.add_error(None, "User exists!")
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            self.add_error(None, "Email exists!")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data.get("username"),
                                   password=self.cleaned_data.get("password"),
                                   email=self.cleaned_data.get("email"))
        Profile.objects.create(user=user, login=user.username)
        return user


class SettingsForm(forms.Form):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                                                             "placeholder": "dr_pepper"}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={"class": "form-control form-control-lg",
                                                                            "placeholder": "dr.pepper@mail.ru"}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control form-control-lg"}))


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                                          "placeholder": "How to build a moonpark?"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control form-control-lg",
                                                        "placeholder": "Really how?", "rows": 8}))
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg",
                                                         "placeholder": "Firefox, Mail.ru"}))

    def save(self):
        tags = []
        for tag in self.cleaned_data["tags"].split(','):
            tags.append(tag.strip())
        tag_list = []
        for tag in tags:
            t = Tag.objects.filter(name=tag).first()
            if t is None:
                t = Tag.objects.create(name=tag, rating=0)
            else:
                t.rating += 1
                t.save()
            tag_list.append(t)
        return tag_list


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control form-control-lg",
                                                        "placeholder": "Enter your answer...", "rows": 8}), label="")
