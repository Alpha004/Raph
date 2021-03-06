from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# MODELO USUARIO
# se encargara de operar el sistema, marcando las alertas como atendidas o no, de imprimir los reportes, verificar las camaras
# en tiempo real y de dar aviso a las enfermeras sobre las alertas de atencion que mandan los pacientes
# class Usuarios(models.Model):
#
#     NombreU = models.CharField(max_length=30)
#     ApellidoU = models.CharField(max_length=30)
#     NickU = models.CharField(max_length=30)
#     ContraU = models.CharField(max_length=30)
#     CorreoU = models.EmailField(max_length=30)
#     PistaU = models.CharField(max_length=6)

# MODELO PUESTO
# simplemente contiene la descripcion sobre el cargo dentro de la institucion
from django.utils import timezone
from django.utils.datetime_safe import datetime


class Puesto(models.Model):
    DescripcionP = models.CharField(max_length=50)

# MODELO PERSONAL
# almacenara las datos necesarioas para el sistema de los miembros del personal

class Personal(models.Model):

    ID_S = models.CharField(max_length=10)
    NombreS =models.CharField(max_length=30)
    ApellidoS =models.CharField(max_length=30)
    Cargo = models.ForeignKey(Puesto)

#MODELO AREAA
# informacion de ls areas en que se divide hospitalizacion
class Area(models.Model):
    Descripcion_Area = models.CharField(max_length=60)

# MODELO PACIENTE
# se tiene data necesaria del paciente para que funcione el sistema, existen mas datos, pero son irrelevantes
class Paciente(models.Model):

    Nombre_P = models.CharField(max_length=50)
    Apellido_P = models.CharField(max_length=50)
    Fecha_Ingreso = models.DateField()
    Fecha_Salida = models.DateField(null=True, blank=True)

# MODELO CAMA
# se tiene los datos de las camas que estan actualmente en hospitalizacion
class Cama(models.Model):
    Nro_Cama = models.CharField(max_length=3)
    Id_paciente = models.ForeignKey(Paciente)
    Area = models.ForeignKey(Area)

#MODELO EDICIONES
# se almacenara la informacion de editar un registro de atencion, por motivos de seguridad
class Edicion(models.Model):
    IdUsuarios = models.ForeignKey(User)
    TiempoE = models.DateTimeField()
    TotalE = models.IntegerField(default=0)

# MODELO ATENCION
# Se almacenara las atenciones que se registren del paciente para la posterior generacion de reportes
class Atencion(models.Model):

    TiempoA = models.DateTimeField()
    DescripcionA = models.TextField(default=None, null=True )
    Estado = models.BooleanField(default=False)
    Ediciones = models.ForeignKey(Edicion,null=True, blank=True)
    NroCamaA = models.ForeignKey(Cama)
    Nombre_U = models.ForeignKey(User)
    ID_P = models.ForeignKey(Personal, default=None, null=True)












