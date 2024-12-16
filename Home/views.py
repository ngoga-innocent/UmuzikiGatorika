from django.shortcuts import render,redirect
from django.views import View
from Documents.models import Copies,SongCategory,SongType
from Notifications.send_Push_Notification import send_email

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
    def post(self, request):
        title=request.POST.get('title')
        message=request.POST.get('message')
        receiver=request.POST.get('email')
        try:
            send_email(f'Contact from message '+ title,message,['ngogainnocent1@gmail.com'])
            return render(request,'home.html',{'message':'message sent Successfully'})
        except Exception as e:
            print(f"Failed to send email: {e}")
            return redirect('home')
    

    
  # Change 'home' to your actual URL name if different
