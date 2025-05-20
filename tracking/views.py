# your_tracking_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerEvent # Yukarıdaki modelinizi import edin
import json

class TrackingAPIView(APIView):
    # Eğer token tabanlı bir güvenlik kullanmayacaksanız,
    # sadece CORS'a güveniyorsanız CSRF korumasını kapatmanız gerekebilir.
    # Genellikle bu tür cross-domain POST isteklerinde CSRF devre dışı bırakılır
    # veya farklı bir kimlik doğrulama yöntemi (API key) kullanılır.
    authentication_classes = [] # Kimlik doğrulama sınıfı yok
    permission_classes = []     # İzin sınıfı yok

    def post(self, request, *args, **kwargs):
        try:
            data = request.data # DRF otomatik olarak JSON'ı ayrıştırır

            event_type = data.get('event')
            product_id = data.get('product_id')
            product_name = data.get('product_name')
            price = data.get('price')
            quantity = data.get('quantity')
            transaction_id = data.get('transaction_id')
            revenue = data.get('revenue')
            customer_id = data.get('customer_id') # GTM'den gönderebilirsiniz
            session_id = data.get('session_id') # GTM'den gönderebilirsiniz

            # Gelen veriyi kaydedin (veya istediğiniz gibi işleyin)
            CustomerEvent.objects.create(
                event_type=event_type,
                customer_id=customer_id,
                session_id=session_id,
                product_id=product_id,
                product_name=product_name,
                price=price,
                quantity=quantity,
                transaction_id=transaction_id,
                revenue=revenue,
                raw_data=data # Tüm gelen JSON'ı kaydetmek için
            )

            # Burada widget mantığınızı çalıştırabilirsiniz
            # Örneğin, bu veriye göre bir arama widget'ı için veri hazırlama
            # Veya sadece gelen veriyi onaylayıp dönebilirsiniz.

            return Response({'status': 'success', 'message': 'Veri başarıyla alındı.'}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'status': 'error', 'message': 'Geçersiz JSON formatı.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Widget'ınızın kullanacağı API endpoint'i (örneğin, popüler ürünler, son bakılanlar)
