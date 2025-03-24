from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from .serializers import PaymentSerializer
from .models import Payment
from datetime import timedelta
from django.utils.timezone import now
# Create your views here.
class PaymentClass(APIView):
    BASE_url = "https://payments.paypack.rw"
    PAYPACK_ID='700c2faa-9695-11ef-99e6-dead742b0238'
    PAYPACK_SECRET='0468b57fef5436ed526a41d85555aab6da39a3ee5e6b4b0d3255bfef95601890afd80709'
    def authorize(self):
        url = f"{self.BASE_url}/api/auth/agents/authorize"
        payload = json.dumps({
        "client_id": self.PAYPACK_ID,
        "client_secret": self.PAYPACK_SECRET
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        
        return response.json()
    def Deposit(self, phone_number,amount, device_token, subscription_type=None):
        url = "https://payments.paypack.rw/api/transactions/cashin"
        # print(f"Phone Number: {phone_number}, Device Token: {device_token}")
        
        payload = json.dumps({
            "amount": amount,
            "number": phone_number
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.authorize()["access"]}',
            'X-Webhook-Mode': 'development'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            # print(f"Response Status Code: {response.status_code}")
            # print(f"Response Body: {response.text}")

            if response.status_code == 200:
                response_data = response.json()
                payment_status = response_data.get('status')
                amount = response_data.get('amount')
                reference_key = response_data.get('ref')
                # phone_number=response_data.get('phone_number')
                # Create a Payment object
                try:
                    payment = Payment.objects.create(
                    payment_status=payment_status,
                    device_tokem=device_token,
                    amount=amount,
                    reference_key=reference_key,
                    paid_number=phone_number
                    # subscription_type=subscription_type
                )
                    # print(payment)
                    payment.save()
                    return Response({"response": "Saved Successfully"}, status=status.HTTP_200_OK)
                except Exception as e:
                    print(f"Failed to save payment: {e}")
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Handle non-200 responses gracefully
            else:
                try:
                    error_message = response.json()
                except ValueError:
                    error_message = {"error": "Unexpected response from payment API"}
                return Response(error_message, status=response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def CashOut(self, amount):
        url = "https://payments.paypack.rw/api/transactions/cashout"

        payload = json.dumps({
        "amount": float(amount),
        "number": "0782214360"
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.authorize()["access"]}',
        'X-Webhook-Mode': 'development'
        }
        # print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response)
        if response.status_code==200:
            
            try:
                    response_data = response.json()
                    payment_status = response_data.get('status')
                    amount = response_data.get('amount')
                    reference_key = response_data.get('ref')
                    payment = Payment.objects.create(
                        payment_status=payment_status,
                        device_tokem='admin_withdran',
                        amount=amount,
                        reference_key=reference_key,
                        paid_number='0782214360',
                        transaction_kind='Cash out'
                        # subscription_type=subscription_type
                    )
                    print("withdraw",payment)
                    payment.save()
                    return Response({"response": "Saved Successfully","success":True}, status=status.HTTP_200_OK)
            except Exception as e:
                        print(f"Failed to save payment: {e}")
                        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        
        response=response.json()
        # print("result",response)
        # print(response.get('ref'))
        return Response({"message": response.status},status=status.HTTP_200_OK)   

    def post(self, request, *args, **kwargs):
        if kwargs.get("action") == "deposit":
            phone_number = request.data.get('phone_number')
            device_token = request.data.get('device_token')
            amount=request.data.get('amount')

            if not phone_number or not device_token:
                return Response({"error": "Phone number and device token are required."}, status=status.HTTP_400_BAD_REQUEST)

            subscription_type = request.data.get("subscription_type")
            # Properly return the response from the Deposit method
            return self.Deposit(phone_number, amount,device_token, subscription_type)

        elif kwargs.get("action") == "webhook":
            return self.webhook(request)
        elif kwargs.get("action") == "cashout":
            if not request.data.get('amount'):
                
                return Response({"error": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)
            amount=request.data.get('amount')
            # print(amount)
            print(self.CashOut(amount))
            return self.CashOut(amount)
        
        else:
            return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)


    def webhook(self,request):
        data = json.loads(request.body.decode('utf-8'))
        print("Webhook data:", data)
        event_id = data.get('event_id')
        kind = data.get('kind')
        transaction_data = data.get('data', {})
        ref = transaction_data.get('ref')
        status = transaction_data.get('status')
        amount = transaction_data.get('amount')
        try:
            payment = Payment.objects.get(reference_key=ref)
            payment.payment_status=status
            payment.save()
            print(payment)
        except Payment.DoesNotExist:
            payment = Payment.objects.create(reference_key=ref, payment_status=status, amount=amount)
            payment.save()
        
        return Response({"message": "Webhook received"})
    

class CheckDevicePaid(APIView):
    def get(self, request):
        # print("Received request:", request.GET)  # Debug incoming request
        
        device_token = request.GET.get("device_token") or request.data.get("device_token")
        # print("Extracted device_token:", device_token)  # Debug extracted token
        
        if not device_token:
            print("Error: Device token is missing")
            return Response({"error": "Device token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            last_payment = Payment.objects.filter(device_tokem=device_token).last()
            print("Last payment record:", last_payment)  # Debug last payment

            if not last_payment:
                return Response({"paid": False, "message": "No payment record found. Payment required."}, status=status.HTTP_200_OK)

            one_month_ago = now() - timedelta(days=30)
            # print("One month ago:", one_month_ago)
            # print("Last payment date:", last_payment.created_at)

            if last_payment.created_at >= one_month_ago and last_payment.payment_status =='completed':
                return Response({"paid": True, "message": "Device is active."}, status=status.HTTP_200_OK)
            else:
                return Response({"paid": False, "message": "Payment has expired. Please renew."}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error occurred:", str(e))  # Debug unexpected error
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
