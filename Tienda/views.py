from django.shortcuts import render
from Tienda.models import Usuario,Perfil_Usuario,Marca,Descuento,Prenda,Inventario,Pedido,Opinion,Inventario,Cesta
from django.db.models import Q,Avg,Max,Min,Prefetch

# Menu de inicio
def index(request):
    return render(request, 'index.html')