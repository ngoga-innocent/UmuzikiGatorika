from django import forms
from .models import NotificationModal

class NotificationModalForm(forms.ModelForm):
    class Meta:
        model = NotificationModal
        fields = ['type', 'notification']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'block w-full mt-1 py-2 rounded-md border px-2 border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            }),
            'notification': forms.Textarea(attrs={
                'class': 'block w-full mt-1  rounded-md border px-2 border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
                'rows': 4,
                'placeholder': 'Enter notification message here...'
            }),
            
            # 'notification_owner': forms.Select(attrs={
            #     'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            # }),
        }
