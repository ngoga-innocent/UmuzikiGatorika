from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Copies,SongType,SongCategory
from.serializers import CopiesSerializer,SongTypeSerializer,SongCategorySerializer,RequestDocumentSerializer
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated,AllowAny



import random
# Create your views here.
class CopiesClass(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Authentication required for POST
        return [AllowAny()]
    def get(self,request):
        copy_id = request.query_params.get("copy_id") 
        if copy_id is not None:
            copy=get_object_or_404(Copies,id=copy_id)
            serializer=CopiesSerializer(instance=copy,context={"request":request})
            print(serializer.data)
            return Response({"copy":serializer.data})
        else:
            copies=Copies.objects.all()
            paginator = Paginator(copies, 50)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            serializer=CopiesSerializer(page_obj,many=True,context={"request":request})
            return Response({"copies":serializer.data})
    def post(self,request):
        # self.permission_classes = [IsAuthenticated]
        # self.check_permissions(request)
        serializer=CopiesSerializer(data=request.data)
        if serializer.is_valid():
            song=serializer.save(uploader=request.user)
            
            return Response({"data":serializer.data})
        print(serializer.errors)
        return Response({"detail":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        copy_id=request.query_params.get('copy_id')
        if copy_id is not None:
            try:
                copy=get_object_or_404(Copies,id=copy_id)
                copy.delete()
                return Response({'details':'Copy deleted'})

            except Copies.DoesNotExist:
                return Response({'details':'Copies Does not Exist'},status=status.HTTP_404_NOT_FOUND) 
        else:
            return Response({'detail':'No copy has been provided'},status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
        copy_id=request.query_params.get('copy_id')
        if copy_id is not None:
            copy = get_object_or_404(Copies, id=copy_id)
            serializer = CopiesSerializer(instance=copy, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'copy':serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details":"copy id not provided"},status=status.HTTP_404_NOT_FOUND)
class SongTypeClass(APIView):
    def get(self,request):
        type_id = request.query_params.get("type_id") 
        if type_id is not None:
            try:
                type=SongType.objects.get(id=type_id)
                songs=Copies.objects.filter(category=type)
                serializer=CopiesSerializer(songs,many=True,context={'request':request})
                return Response({'copies':serializer.data})
            except SongType.DoesNotExist():
                return Response({'detail':'The Type is not found'})
        else:
            types=SongType.objects.all()
            serializer=SongTypeSerializer(types,many=True,context={'request':request})
            return Response({'types':serializer.data})
class SongCategoryView(APIView):
    def get(self,request):
        category_id = request.GET.get('category_id', None)
        season_id=request.GET.get('season',None)
        
        if category_id is not None:
            try:
                category=SongCategory.objects.get(id=category_id)
                types=Copies.objects.filter(part=category).order_by('name')
                if season_id is not None:
                    try:
                        season=SongType.objects.get(id=season_id)
                        types=types.filter(category=season)
                    except SongType.DoesNotExist:
                        return Response({'detail':'The Season is not found'})
                paginator = Paginator(types, 50)
                page_number = request.GET.get("page",1)
                page_obj = paginator.get_page(page_number)
                serializer=CopiesSerializer(page_obj,many=True,context={"request":request})
                    
                return Response({   
                                    'songs':serializer.data,
                                    'current_page': page_obj.number,  # Current page number
                                    'next': page_obj.next_page_number() if page_obj.has_next() else None
                                })
            except SongCategory.DoesNotExist:
                return Response({'detail':'The Category is not found'})
        if season_id is not None:
            try:
                season=SongType.objects.get(id=season_id)
                types=Copies.objects.filter(category=season).order_by('name')
                paginator = Paginator(types, 50)
                page_number = request.GET.get("page",1)
                page_obj = paginator.get_page(page_number)
                serializer=CopiesSerializer(page_obj,many=True,context={"request":request})
                return Response({   
                                    'songs':serializer.data,
                                    'current_page': page_obj.number,  # Current page number
                                    'next': page_obj.next_page_number() if page_obj.has_next() else None
                                })
            except SongType.DoesNotExist:
                return Response({'detail':'The Season is not found'})    
        else:
            all_songs=Copies.objects.all().count()
            categories=SongCategory.objects.all()
            serializer=SongCategorySerializer(categories,many=True,context={'request':request})
            return Response({'categories':serializer.data,"songs_number":all_songs})
    def post(self,request):
        serializer=SongCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data})
        return Response({"detail":serializer.errors},status=status.HTTP_400_BAD_REQUEST)   
class Search(APIView):
    def get(self,request):
        search_query = request.GET.get('q', '').strip()  # Get query and strip whitespace
    # print("search query:", search_query)

        if search_query:  # Check if search_query is provided
            songs = Copies.objects.filter(
                Q(name__icontains=search_query) | Q(composer__icontains=search_query)
            )
            
            # If no songs found, return a different message
            if not songs.exists():
                return Response({'detail': 'No songs found matching the query.'}, status=status.HTTP_404_NOT_FOUND)

            serializer = CopiesSerializer(songs, many=True, context={'request': request})
            return Response({"songs": serializer.data}, status=status.HTTP_200_OK)
        
        return Response({'detail': 'No search query provided.'}, status=status.HTTP_400_BAD_REQUEST)
class CreateRepertoire(APIView):
    def get(self,request):
        categories=SongCategory.objects.all()
        repertoire_songs={}
        for category in categories:
            songs=Copies.objects.filter(part=category)
            if songs.exists():
                # Choose a random song from the category's songs
                choosen_song=random.choice(songs)
                repertoire_songs[category.name]=CopiesSerializer(choosen_song).data
            else:
                repertoire_songs[category.name] = None     
        return  Response(repertoire_songs)   
# class FavoriteSongs(APIView):

#     def get(self, request):
#         pass
#     def post(self, request):
#         user= request.user

class RequestSongView(APIView):
    def post(self, request):
        serializer=RequestDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data})
        return Response({'error':serializer.error},status=status.HTTP_400_BAD_REQUEST)


            