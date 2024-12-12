from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'thumbnail', 'location', 'date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full py-2 px-2 rounded-md border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full py-2 px-2 rounded-md border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Enter event description',
                'rows': 4
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'mt-1 block w-full py-2 px-2 rounded-md border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full py-2 px-2 rounded-md border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'placeholder': 'Enter event location'
            }),
            'date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full py-2 px-2 rounded-md border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'type': 'datetime-local'
            }),
        }
