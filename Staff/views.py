from django.shortcuts import render,redirect
from django.views import View
from rest_framework.views import APIView
from Accounts.models import Users
from Advertise.models import Event, TrendingSongs
from Musicians.models import MusicianModel
from Documents.models import Copies,SongCategory,SongType,Request
from Advertise.models import Event,TrendingSongs
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse,JsonResponse
from Advertise.forms import EventForm
from Notifications.models import NotificationModal
from Notifications.forms import NotificationModalForm
from Documents.serializers import CopiesSerializer
from Payments.models import Payment
from django.db.models import Sum
from django.db.models import Q
import re
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from paypack.client import HttpClient
from paypack.oauth2 import Oauth
from paypack.merchant import Merchant
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.response import Response
import os
# Create your views here.
class Staff(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def get(self, request, *args, **kwargs):
        # Logic for staff dashboard page
        # Fetching data for dashboard
        users = Users.objects.all().order_by("-date_joined")[:20]
        musicians = MusicianModel.objects.all().order_by("-joined_at")[:30]
        copies = Copies.objects.all().order_by("-uploaded_on")[:50]
        events = Event.objects.all().order_by("-created_at")[:20]
        trending_songs = TrendingSongs.objects.all().order_by("-created_at")[:12]
        copies_Number=Copies.objects.all().count()
        request_number=Request.objects.filter(status=False).count()
        context = {
            'users': users,
           'musicians': musicians,
            'copies': copies,
            'events': events,
            'trending_songs': trending_songs,
            'copies_number': copies_Number,
            'request_number':request_number,
        }
        return render(request,'./Pages/Dashboard.html',context)
class MusicSheetView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def get(self, request, name=None):
        # Logic for displaying music sheet
        seasons=SongType.objects.all()
        if name is None:
            sheets=Copies.objects.all().order_by('-uploaded_on')
            paginator = Paginator(sheets, 25)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            categories=SongCategory.objects.all()
            
            return render(request,'./Pages/MusicSheets.html',{"sheets":page_obj,"categories":categories,"seasons":seasons})  # Redirect to music sheet list if no song id is provided
        print(name)
        try:
            part=SongCategory.objects.get(id=name)
        except SongCategory.DoesNotExist:
            return redirect('music_sheets')
             
        songs = Copies.objects.filter(part=part.id)
        
        paginator = Paginator(songs, 50)  # Show 25 contacts per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        categories=SongCategory.objects.all()
        context = {
           'sheets': page_obj,
           "categories": categories,
           "seasons":seasons
        }
        return render(request,'./Pages/MusicSheets.html',context)
    def post(self, request):
        category_id = request.POST.get('song_category')
        season_id = request.POST.get('season')
        
        if "delete" in request.POST:
            song_id = request.POST.get('id')
            try:
                song = Copies.objects.get(id=song_id)
                song.delete()
                return JsonResponse({"message": "Successfully deleted a song"})
            except Copies.DoesNotExist:
                return JsonResponse({"error": "Song not found"})
        if "check" in request.POST:
            song_id = request.POST.get('song_id')
            try:
                song = Copies.objects.get(id=song_id)
                song.checked = True
                song.save()
                print("saved")
                return JsonResponse({"message": "Successfully marked a song as checked"})
            except Copies.DoesNotExist:
                print("got an unknown song")
                return JsonResponse({"error": "Song not found"})
        try:
            category = SongCategory.objects.get(id=category_id)
            if season_id is not None:
                season = SongType.objects.get(id=season_id)
        except SongCategory.DoesNotExist:
            return render(request, 'home.html', {"error": "Invalid Category"})
        except SongType.DoesNotExist:
            season = None
            

        songs = request.FILES.getlist('songs')
        user = request.user

        if not songs:
            return render(request, 'home.html', {"error": "No songs uploaded."})

        errors = []
        allowed_extensions = ['pdf', 'mp3']
        max_file_size = 10 * 1024 * 1024  # 10 MB

        for song in songs:
            name = song.name
            if name.endswith('.pdf'):
                name = name[:-4]

            # Standardize and validate the filename
            standardized_name = re.sub(r"[\-()',`~]", "_", name)
            parts = standardized_name.split("_")
            if len(parts) < 2:
                errors.append(f"Skipping file {name}. Expected format: 'Title_Composer'")
                continue

            title = parts[0].strip()
            composer = " ".join(parts[1:]).strip()
            title = title[:100]  # Truncate to 100 characters
            composer = composer[:100]

            # Check file extension and size
            if song.size > max_file_size:
                errors.append(f"{name} exceeds the maximum file size of 10 MB.")
                continue

            if not any(song.name.lower().endswith(ext) for ext in allowed_extensions):
                errors.append(f"{name} has an unsupported file format.")
                continue

            # Prepare data for serializer
            data = {
                'name': title,
                'composer': composer,
                'uploader': user.id,
                'part': category_id,
                'document': song,
                'category': season_id
            }

            # Validate and save using the serializer
            serializer = CopiesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                # Collect validation errors
                errors.append(f"Failed to upload {name}: {serializer.errors}")

        # Provide feedback to the user
        if errors:
            return render(request, './Pages/MusicSheets.html', {"errors": errors})
        
        return redirect('music_sheets')

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")
        song_id = data.get("id")
        # field = request.POST.get("field")
        # value = request.POST.get("value")
        print(field,value)
        if not song_id or not field or not value:
            return JsonResponse({"error": "Invalid data"}, status=400)

        try:
            song = Copies.objects.get(id=song_id)
            if field=='part':
                category = SongCategory.objects.get(id=value)
                song.part = category
                song.save()
                return JsonResponse({"message": f"Part updated successfully"}, status=200)
            if field=='category':
                season = SongType.objects.get(id=value)
                song.category = season
                song.save()
                return JsonResponse({"message": f"Part updated successfully"}, status=200)
            if hasattr(song, field):
                setattr(song, field, value)
                song.save()
                return JsonResponse({"message": f"{field} updated successfully"}, status=200)
            else:
                return JsonResponse({"error": "Invalid field"}, status=400)
        except Copies.DoesNotExist:
            return JsonResponse({"error": "Song not found"}, status=404)
class SongCategoryView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def post(self, request, *args, **kwargs):
        
        # Check if it's a delete request
        if 'delete' in request.POST:
            category_id = request.POST.get('category_id')
            print(category_id)
            try:
                category = SongCategory.objects.get(id=category_id)
                print(category.name)
                category.delete()
                
                return JsonResponse({"message": "Category deleted successfully"}, status=200)
            except SongCategory.DoesNotExist:
                return JsonResponse({"error": "Invalid category"}, status=404)

        # Otherwise, handle category creation
        name = request.POST.get('category_name')
        try:
            SongCategory.objects.create(name=name)
            return redirect("music_sheets")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
class MusicianView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def get(self, request, name=None):
        musicians =MusicianModel.objects.all().order_by("-joined_at")     
        paginator=Paginator(musicians,25)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        return render(request,'./Pages/Musicians.html',{'musicians':page_obj})
    def post(self, request):
        
        field=request.POST.get('field')
        value=request.POST.get('value')
        musician_id=request.POST.get('id')
        verify=request.POST.get('verify')
        
        if 'verify' in request.POST:
            musician_id=request.POST.get('musician_id')
            print("verify")
            musician=MusicianModel.objects.get(id=musician_id)
            musician.verified=True
            musician.save()
            return JsonResponse({"message":f"Musician's verification status updated successfully"},status=200)
        if not musician_id or not field or not value:
            return JsonResponse({"error":"Invalid data"},status=400)
        try:
            musician=MusicianModel.objects.get(id=musician_id)
            if hasattr(musician,field):
                setattr(musician,field,value)
                musician.save()
                return JsonResponse({"message":f"{field} updated successfully"},status=200)
            else:
                return JsonResponse({"error":"Invalid field"},status=400)
        except MusicianModel.DoesNotExist:
            return JsonResponse({"error":"Musician not found"},status=404)   
class TredingVideo(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def get(self, request):
        videos=TrendingSongs.objects.all().order_by('-created_at')
        return render(request,'./Pages/TrendingVideos.html',{'songs':videos})
    def post(self,request):
        if 'delete' in request.POST:
            print('Delete')
            song_id=request.POST.get('song_id')
            try:
                song=TrendingSongs.objects.get(id=song_id)
                song.delete()
                return JsonResponse({"message":"Trending Song deleted successfully","success":True},status=200)
            except TrendingSongs.DoesNotExist:
                return JsonResponse({"error":"Invalid Trending Song"},status=404)
        link=request.POST.get('link')
        tredingVideo=TrendingSongs.objects.create(link=link)
        tredingVideo.save()
        return JsonResponse({"message":"Successfully created a new Trending Song","success":True},status=200)
class EventsView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def get(self, request):
        events=Event.objects.all().order_by('-created_at')
        form = EventForm()
        return render(request,'./Pages/Events.html',{'events':events,"form":form})
    def post(self, request):
        if 'delete' in request.POST:
            print('Delete')
            event_id=request.POST.get('event_id')
            try:
                event=Event.objects.get(id=event_id)
                event.delete()
                return JsonResponse({"message":"Event deleted successfully","success":True},status=200)
            except Event.DoesNotExist:
                return JsonResponse({"error":"Invalid Event"},status=404)
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('events')
        return render(request, './Pages/Events.html', {'form': form})
class NotificationView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url = '/account/login'  # Redirect for unauthenticated users

    def test_func(self):
        return self.request.user.is_staff  # Allow only staff use
    def get(self, request, *args, **kwargs):
        notifications=NotificationModal.objects.all().order_by('-created_at')
        form=NotificationModalForm()
        return render(request,'./Pages/Notifications.html',{'notifications':notifications,"form":form})
    def post(self, request):
        form=NotificationModalForm(request.POST)
        if form.is_valid():
            notification=form.save(commit=False)
            notification.save()
            return redirect('notifications')
        else:
            return render(request, './Pages/Notifications.html', {'form': form})
class Requests(View):
    def get(self, request, *args, **kwargs):
        requests=Request.objects.filter(status=False).order_by('-requested_on')
        
        return render(request,'./Pages/Requests.html',{'requests':requests})
    def post(self, request):
        request_id=request.POST.get('id')
        try:
            request_obj=Request.objects.get(id=request_id)
            request_obj.status=True
            request_obj.save()
            return JsonResponse({"message":"Request approved successfully","success":True},status=200)
        except Request.DoesNotExist:
            return JsonResponse({"error":"Invalid Request"},status=404)
class Payments(View):
    
    # client_id="700c2faa-9695-11ef-99e6-dead742b0238", 
    # client_secret="0468b57fef5436ed526a41d85555aab6da39a3ee5e6b4b0d3255bfef95601890afd80709"
    client_id=os.getenv("PAYPACK_ID")
    client_secret=os.getenv("PAYPACK_SECRET")

    HttpClient(client_id=client_id, client_secret=client_secret)
    auth = Oauth().auth()
    # print(auth)
    def get(self, request, *args, **kwargs):
        account_info=Merchant().me()
        today = now().date()
    
        # Generate the last 7 days, including today
        last_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
        
        # Prepare a dictionary to hold results
        payments_per_day = {day: 0 for day in last_week}
        
        # Query payments from the last 7 days
        start_date = last_week[0]
        end_date = last_week[-1] + timedelta(days=1)  # End date is exclusive
        
        payments = Payment.objects.filter(
            created_at__date__gte=start_date,  # Ensure date part matches
            created_at__date__lt=end_date
        ).values('created_at__date').annotate(total_amount=Sum('amount'))
        success_payments=Payment.objects.filter(payment_status='successful').count()
        failed_payments=Payment.objects.filter(payment_status='failed').count()
        # print(success_payments,failed_payments)
        # Populate the dictionary with the aggregated results
        for payment in payments:
            date = payment['created_at__date']
            if date in payments_per_day:
                payments_per_day[date] = payment['total_amount']
        
        # Return data in a format suitable for the chart (e.g., labels and values)
        labels = [day.strftime('%Y-%m-%d') for day in last_week]
        values = [payments_per_day[day] for day in last_week]
        
        payment_history=Payment.objects.filter(payment_status='successful').order_by('-created_at')[:50]
        
        context={
             'labels': labels,
             'values': values,
             'start_date': start_date,
             'end_date': end_date,
             'success_failure_label':["Successfull","Failed"],
             'success_failure_data':[success_payments,failed_payments],
             'account_info':account_info,
             'payment_histories':payment_history,
        }
        # print(context)
        return render(request,'./Pages/payments.html',context)
class PaymentInfoApi(APIView):
    client_id=os.getenv("PAYPACK_ID")
    client_secret=os.getenv("PAYPACK_SECRET")

    HttpClient(client_id=client_id, client_secret=client_secret)
    auth = Oauth().auth()
    def get(self,request):
        account_info=Merchant().me()
        return Response({"info":account_info})