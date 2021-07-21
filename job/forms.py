from django import forms
from .models import *
import datetime

class JobForm(forms.ModelForm):    
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'form-control'
        }
    ))
    CHOICES = ((False, 'Stop'), (True, 'Running'))
    status = forms.ChoiceField(label='Status', widget=forms.Select(attrs={'class' : 'form-control'}), choices=CHOICES)
    start_time = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'form-control my-icon'
        }
    ))
    end_time = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'form-control my-icon'
        }
    ))
    class Meta:
        model = Job
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['status'].required = False
        self.fields['status'].initial = False
        self.fields['status'].widget.attrs['disabled'] = 'disabled'
        self.fields['start_time'].required = False
        self.fields['end_time'].required = False

        if self.instance and self.instance.pk:
            self.fields['name'].initial = self.instance.name
            self.fields['status'].initial = self.instance.status
            self.fields['status'].widget.attrs.pop('disabled', None)
            self.fields['start_time'].initial = self.instance.start_time
            self.fields['end_time'].initial = self.instance.end_time

    def clean(self):
        name = self.cleaned_data.get('name')
        if len(name) == 0:
            self.add_error('name', 'Name is required')
        else:
            try:
                check_name = Job.objects.filter(name__iexact=name)
                if self.instance:
                    check_name = check_name.exclude(name__iexact=self.instance.name)
                if check_name:
                    self.add_error('name', 'Name already exists')
            except Job.DoesNotExist:
                pass
            
        start_time = self.cleaned_data.get('start_time')
        if len(start_time) == 0 or start_time is None:
            self.add_error('start_time', 'Start Time is required')
            
        end_time = self.cleaned_data.get('end_time')
        if len(end_time) == 0 or end_time is None:
            self.add_error('end_time', 'End Time is required')
            
        if len(end_time) != 0 and  len(start_time) != 0:
            try:
                start_time_object = datetime.datetime.fromisoformat(start_time)
            except Exception as e:
                self.add_error('start_time', 'Enter correct format')
            try:
                end_time_object = datetime.datetime.fromisoformat(end_time)
            except Exception as e:
                self.add_error('end_time', 'Enter correct format')
            if start_time_object >= end_time_object:
                 self.add_error('end_time', 'End time must be after Start time.')