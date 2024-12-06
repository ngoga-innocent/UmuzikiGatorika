from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from .serializers import PaymentSerializer
from .models import Payment
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
    def Deposit(self,phone_number,device_token,subscription_type=None):
        url = "https://payments.paypack.rw/api/transactions/cashin"
        
        payload = json.dumps({
        "amount": 100,
        "number":phone_number
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.authorize()["access"]}',
        'X-Webhook-Mode':'development'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code ==200:
            payment_status=response.json().get('status')
            amount=response.json().get('amount')
            reference_key=response.json().get('ref')
            payment=Payment.objects.create(payment_status=payment_status,device_tokem=device_token,amount=amount,reference_key=reference_key,subscription_type=subscription_type)
            payment.save()
        return Response({"response":response.json()})
    def post(self,request, *args, **kwargs):
        
        
        if kwargs.get("action")=="deposit":
            phone_number=request.data['phone_number']
            device_token=request.data['device_token']
            if subscription_type:=request.data.get("subscription_type"):
                return self.Deposit(phone_number,device_token,subscription_type)
            return self.Deposit(phone_number,device_token) 
        if kwargs.get("action")=="webhook":
            return self.webhook(request)  # Assuming webhook is POST request for this action  # This method is not implemented in the current code. You can implement this method as per your requirements.  # For example, you can save the webhook data to your database.  # You can also use the webhook data to process the payment and update the status of the transaction.  # Make sure to validate the webhook data before processing it.  # You can use the `request.data` to access the webhook data.  # You can also use the `request.headers` to access the headers of the webhook request.  # You can use the `request.method` to check the HTTP method of the webhook request.  # You can use the `request.path` to check the path of the webhook request.  # You can use the `request.query_params` to access the query parameters of the webhook request.  # You can use the `request.
        else:
            return Response({"message": "Invalid action"})
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
        except Payment.DoesNotExist:
            payment = Payment.objects.create(reference_key=ref, payment_status=status, amount=amount)
            payment.save()
        
        return Response({"message": "Webhook received"})
    

