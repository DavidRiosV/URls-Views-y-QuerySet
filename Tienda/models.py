from django.db import models

# Create your models here.

# 1 Usuario/Cliente
class Usuario(models.Model):
    nombre = models.CharField(max_length=15)
    correo = models.EmailField(db_column="email_usuario",unique=True)
    contrasena = models.CharField(max_length=20)
    fecha_registro = models.DateTimeField(auto_now_add=True)

# 2 Perfil Usuario
class Perfil_Usuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE)

    apodo = models.CharField(max_length=20 , unique=True)
    biografia = models.TextField(max_length=200)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

# 3 Marca 
class Marca(models.Model):
    nombre = models.CharField(max_length=20 , unique=True)
    pais_origen=models.CharField(max_length=100, blank=True)
    descripcion=models.TextField(blank=True)
    anio_fundacion=models.PositiveIntegerField(null=True,blank=True)

# 4 Descuento 
class Descuento(models.Model):
    codigo=models.CharField(max_length=20 , unique=True)
    porcentaje=models.DecimalField(max_digits=5 , decimal_places=2)
    activo=models.BooleanField(default=True)
    fecha_expiracion=models.DateField()

# 5 Prenda
class Prenda(models.Model):
    TALLAS = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]
    marca = models.ForeignKey(Marca, on_delete= models.CASCADE)
    descuento = models.ManyToManyField(Descuento)

    nombre=models.CharField(max_length=100)
    descripcion=models.TextField(blank=True)
    precio=models.DecimalField(max_digits=8,decimal_places=2)
    talla=models.CharField(max_length=3, choices=TALLAS)
    
# 6 Cesta
class Cesta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete= models.CASCADE,null=True,blank=True)
    prenda = models.ManyToManyField(Prenda,through='ItemCesta')

    fecha_creacion=models.DateTimeField(auto_now_add=True)
    activo=models.BooleanField(default=True)
    objetos_en_cesta=models.IntegerField()
    total=models.FloatField(default=1)

class ItemCesta(models.Model):
    cesta = models.ForeignKey(Cesta, on_delete= models.CASCADE)
    prenda = models.ForeignKey(Prenda, on_delete= models.CASCADE)

    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
# 7 Inventario
class Inventario(models.Model):
    prenda=models.ForeignKey(Prenda, on_delete=models.CASCADE)

    cantidad_disponible=models.PositiveIntegerField(default=0)
    ubicacion_almacen=models.CharField(max_length=255,blank=True)
    stock_minimo=models.PositiveIntegerField(default=1)
    stock_maximo=models.PositiveIntegerField(default=100)
    
# 8 Pedido
class Pedido(models.Model):
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('PROC', 'Procesando'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    prenda = models.ManyToManyField(Prenda, through='DetallePedido')

    fecha=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    estado=models.CharField(max_length=4,choices=ESTADOS, default='PEND')
    direccion_envio = models.CharField(max_length=255)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE)
    
    cantidad = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
# 9 Factura
class Factura(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete= models.CASCADE)

    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
# 10 Opinion/Reseña
class Opinion (models.Model):
    usuario = models.ForeignKey(Usuario, on_delete= models.CASCADE)
    prenda = models.ForeignKey(Prenda, on_delete= models.CASCADE)

    clasificacion=models.PositiveIntegerField(default=5)
    comentario=models.TextField(blank=True)
    fecha=models.DateField(auto_now_add=True)
    recomendado=models.BooleanField(default=True)
