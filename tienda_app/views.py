from django.views import View
from django.shortcuts import render, HttpResponse
from .services import CompraService
from .infra.factories import PaymentFactory

class CompraView(View):
    """
    CBV: Vista Basada en Clases. 
    Actúa como un "Portero": recibe la petición y delega al servicio.
    TUTORIAL 02: Usa PaymentFactory para desacoplar la infraestructura
    """
    template_name = 'tienda_app/compra.html'
    
    def setup_service(self):
        gateway = PaymentFactory.get_processor()  # Factory desacopla la infraestructura
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(request, self.template_name, {
                'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                'total': total
            })
        except (ValueError, Exception) as e:
            # Manejo de errores de negocio transformados a respuesta de usuario
            return render(request, self.template_name, {
                'error': str(e)
            }, status=400)



import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Libro, Inventario, Orden

def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        inventario = Inventario.objects.get(libro=libro)
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19

            with open("pagos_manuales.log", "a") as f:
                f.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")

            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total, direccion_envio="Por defecto")

            return HttpResponse(f"Compra exitosa: {libro.titulo}")
        else:
            return HttpResponse("Sin stock", status=400)

    total_estimado = float(libro.precio) * 1.19
    return render(request, 'tienda_app/compra_rapida.html', {
        'libro': libro,
        'total': total_estimado
    })

class CompraRapidaView(View):
    """
    CBV: Vista Basada en Clases.
    Separa GET y POST en métodos distintos.
    Aún con lógica acoplada, pero mejor estructura.
    """
    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19
        return render(request, self.template_name, {
            'libro': libro,
            'total': total
        })

    def post(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inv = Inventario.objects.get(libro=libro)

        if inv.cantidad > 0:
            total = float(libro.precio) * 1.19
            return HttpResponse("Comprado via CBV")

        return HttpResponse("Error", status=400)




from .services import CompraRapidaService

class CompraRapidaConServicioView(View):
    """
    CBV mejorada que delega toda la lógica al servicio.
    La vista solo es un "Portero" entre HTTP y la lógica de negocio.
    """
    template_name = 'tienda_app/compra_rapida.html'

    def setup_service(self):
        """Inyección de dependencias: creamos el servicio con su infraestructura"""
        gateway = BancoNacionalProcesador()
        return CompraRapidaService(procesador_pago=gateway)

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19
        return render(request, self.template_name, {
            'libro': libro,
            'total': total
        })

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.procesar(libro_id)
            return render(request, self.template_name, {
                'mensaje_exito': f'¡Compra exitosa! Total: ${total}',
                'libro': get_object_or_404(Libro, id=libro_id),
                'total': total
            })
        except ValueError as e:
            return render(request, self.template_name, {
                'error': str(e),
                'libro': get_object_or_404(Libro, id=libro_id),
                'total': float(get_object_or_404(Libro, id=libro_id).precio) * 1.19
            }, status=400)
        except Exception as e:
            return render(request, self.template_name, {
                'error': f'Error en el procesamiento: {str(e)}',
                'libro': get_object_or_404(Libro, id=libro_id),
                'total': float(get_object_or_404(Libro, id=libro_id).precio) * 1.19
            }, status=500)