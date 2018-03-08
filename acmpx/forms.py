# coding:utf-8

from django import forms
from django.forms import ModelForm, TextInput
from .models import Training


class SearchCertificateForm(forms.Form):
	type = forms.ChoiceField(
		label='类型',
		choices=(('student_no', '按学号查询'), ('certificate_no', '按证书编号查询')),
		widget=forms.Select(attrs={'class': 'form-control'})
	)
	query = forms.CharField(
		label='查询内容',
		max_length=128,
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入查询内容'})
	)


class AdminLoginForm(forms.Form):
	username = forms.CharField(
		label='用户名',
		max_length=128,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'})
	)
	password = forms.CharField(
		label='密码',
		max_length=128,
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'})
	)
	next = forms.CharField(label='next', max_length=512, required=False, widget=forms.HiddenInput)


class TrainingForm(ModelForm):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(TrainingForm, self).__init__(*args, **kwargs)

	class Meta:
		model = Training
		fields = ['title', 'title_en', 'started_at', 'ended_at', 'hidden']
		widgets = {
			'title': TextInput(attrs={'class': 'form-control'}),
			'title_en': TextInput(attrs={'class': 'form-control'}),
			'started_at': TextInput(attrs={'class': 'form-control date-picker'}),
			'ended_at': TextInput(attrs={'class': 'form-control date-picker'}),
		}


class AdminUploadCertificateForm(forms.Form):
	file = forms.FileField()
