from django.urls import path
from .views import CompraView, compra_rapida_fbv, CompraRapidaView, CompraRapidaConServicioView
from .api.views import CompraAPIView

urlpatterns = [
    # Usamos .as_view() para habilitar la CBV
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    # PASO 1: FBV Spaghetti
    path('compra-rapida/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    # PASO 2: CBV
    path('compra-rapida-cbv/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida_cbv'),
    # PASO 3: CBV con Service Layer
    path('compra-rapida-servicio/<int:libro_id>/', CompraRapidaConServicioView.as_view(), name='compra_rapida_servicio'),
    # TUTORIAL 03: API REST
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]