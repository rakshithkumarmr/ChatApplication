from django import forms
from simplecaptcha import captcha ,captchaform
from simplecaptcha.fields import  CaptchaField,CaptchaWidget

@captcha
class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    conform_assword = forms.CharField(max_length=100)
    captchaform = CaptchaWidget()
