from django.shortcuts import render,get_object_or_404,redirect
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from django.db.models import Q
from django.views import View
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,logout
from django.contrib.auth import login, authenticate
from .serializers import UserSerializer
# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=get_object_or_404(Users,username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            print(serializer.data)
            return Response(serializer.data)
        else:
            print("error",serializer.errors)
            error_messages = " ".join(
                [f"{key}: {', '.join(value)}" for key, value in serializer.errors.items()]
            )
            
            print("error",serializer.errors)
            print(error_messages)
            return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)
    
        
class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        
        password = request.data.get('password')
        user =get_object_or_404(Users,Q(username=username) | Q(phone_number=username))
        if not user.check_password(request.data['password']):
            return Response({"detail":'Passwords doesnot match'},status=status.HTTP_400_BAD_REQUEST)
        token,created=Token.objects.get_or_create(user=user)
        serializer=UserSerializer(instance=user)
        return Response({"token":token.key,"user":serializer.data})

def TokenVerification(auth_token):
    # auth_token=request.META.get('HTTP_AUTHORIZATION')
    print(auth_token)
    if not auth_token:
        return Response({'detail':'No token '},status=403)
    else:
        try:
            
            token_prefix=auth_token.split(' ')[0]
            
            if token_prefix.lower() != 'token':
                return Response({'detail':'invalid token prefix'},status=403)
            user_token=Token.objects.get(key=auth_token.split(' ')[1])
            # user=UserSerializer(user_token.user,context={"request":request})
            # return Response({"user":user.data},status=200)
            print(user_token)
            return user_token.user
        except:
            return Response({'detail':'invalid Token'},status=401)

# @authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def TokenVerification(request):
#     return Response({"user":format(UserSerializer(instance=request.user).data)}) 

@api_view(['PUT'])
def ResetPassword(request):
    try:
        user=Users.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        serializer=UserSerializer(instance=user)
        return Response({'user':serializer.data})
    except Users.DoesNotExist:
        return Response({'detail':'user Not found'},status=status.HTTP_404_NOT_FOUND)
@api_view(['PUT'])
def UpdateProfile(request):
        auth_token=request.META.get('HTTP_AUTHORIZATION')
        user = TokenVerification(auth_token)
        if not user:
            return Response({'detail':'Please Login'},status=status.HTTP_401_UNAUTHORIZED)
        try:
            user_object=Users.objects.get(pk=user.id)
            serializer=UserSerializer(user_object,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail":serializer.data})
            else:
                print(serializer.errors)
                return Response({"detail":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Users.DoesNotExist:
            return Response({'detail':'user not found'},status=status.HTTP_401_UNAUTHORIZED)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"user":serializer.data})    
    def put(self, request):
        """Partially update user profile fields"""
        try:
            user = request.user
            print(request.data)
            serializer = UserSerializer(user, data=request.data, partial=True)  # Partial update
            if serializer.is_valid():
                serializer.save()
                return Response({"user": serializer.data}, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def patch(self, request):
        """Change user password without using a serializer"""
        user = request.user
        data = request.data

        # Extract old and new password
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        # confirm_password = data.get("confirm_password")

        # Validate required fields
        if not old_password or not new_password:
            return Response(
                {"error": "All fields (old_password, new_password) are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if old password is correct
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if new password matches confirmation
        # if new_password != confirm_password:
        #     return Response({"error": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Change password and save
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK) 
    def delete(self,request):
        # user=request.user
        if request.user:
            user=get_object_or_404(Users,id=request.user.id)
            print("users",user)
            if user:
                try:
                    user.delete()
                except Exception as e:
                    print(e)
                    return Response({"message":"Failed to Delete the account"},status=401)
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['GET'])
def GetProfile(request):
    auth_token=request.META.get('HTTP_AUTHORIZATION')
    user = TokenVerification(auth_token)
    print(user)
    if not user:
        return Response({"detail":'please Login'})
 
    # return Response("ok")
    
    try:
        user_object=Users.objects.get(pk=user.id)
        serializer=UserSerializer(user_object,context={"request":request})
        
        return Response({'user':serializer.data})
    except Users.DoesNotExist:
        return Response({"detail":"No user found"})
def WebLogout(request):
    logout(request)
    return redirect('home')
class WebLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request,'login.html')
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        #Finding user in database
        user_exists=Users.objects.filter(username=username).exists()
        if not user_exists:
            return render(request, 'login.html', {"form_error": 'Invalid username '})
        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)
        print(user)
        # Handle authentication failure
        if not user:
            return render(request, 'login.html', {"form_error": 'Incorrect  password'})

        # Log the user in and redirect to home
        login(request, user)
        return redirect('home')
class ChangePassword(APIView):
    # print("called")
    def post(self,request):
        phone_number = request.data.get("phone_number")
        print(phone_number)
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=400)

        try:
            user = Users.objects.get(phone_number=phone_number)
            return Response({"success": "Phone number verified"}, status=200)
        
        except Users.DoesNotExist:
            return Response({"error": "Phone number not found"}, status=404)
        except Exception as e:
            print(f"Unexpected error in phone verification: {str(e)}")
            return Response({"error": "Something went wrong"}, status=500)
    def patch(self,request):
        phone_number = request.data.get("phone_number")
        new_password = request.data.get("new_password")

        if not phone_number or not new_password:
            return Response({"error": "Phone number and new password required"}, status=400)

        try:
            user = Users.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
            return Response({"success": "Password updated successfully"}, status=200)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=404)