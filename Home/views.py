from django.shortcuts import render,redirect
from django.views import View
from Documents.models import Copies,SongCategory,SongType
from Notifications.send_Push_Notification import send_push_notification

# Create your views here.
def HomeView(request):
    
    return render(request,'privacy.html')
def AboutView(request):
    return render(request,'about_us.html')
class Home(View):
    def get(self, request):
        
        categories=SongCategory.objects.all()
        # print(categories)
        context={"categories":categories}
        return render(request,'home.html',context)
    
    

    
  # Change 'home' to your actual URL name if different
