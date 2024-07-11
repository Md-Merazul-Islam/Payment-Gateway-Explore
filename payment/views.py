from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from django.conf import settings
import requests

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Add logic to handle SSLCommerz payment request and response
        # Example:
        payment_data = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASS,
            'total_amount': request.data['amount'],
            'currency': 'BDT',
            'tran_id': 'your_transaction_id',
            'success_url': 'your_success_url',
            'fail_url': 'your_fail_url',
            'cancel_url': 'your_cancel_url',
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_phone': 'your_customer_phone',
            'cus_add1': 'your_customer_address',
            'cus_city': 'your_customer_city',
            'cus_country': 'Bangladesh',
            'shipping_method': 'NO',
            'product_name': 'your_product_name',
            'product_category': 'your_product_category',
            'product_profile': 'your_product_profile',
        }

        response = requests.post('https://sandbox.sslcommerz.com/gwprocess/v4/api.php', data=payment_data)
        payment_response = response.json()

        if payment_response['status'] == 'SUCCESS':
            # Save payment info
            payment = Payment.objects.create(
                user=request.user,
                cart_id=request.data['cart_id'],
                amount=request.data['amount'],
                status='Pending',
                transaction_id=payment_response['tran_id'],
            )
            return Response({'payment_url': payment_response['GatewayPageURL']})
        else:
            return Response({'error': 'Payment initiation failed'}, status=400)
