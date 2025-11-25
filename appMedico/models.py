from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('doctor', 'Doctor'),
        ('paciente', 'Paciente'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='paciente')

    def __str__(self):
        return f"{self.username} ({self.rol})"

class Doctor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.usuario.get_full_name()
class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.usuario.get_full_name()
    
class Atencion(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    diagnostico = models.TextField()

    def __str__(self):
        return f"Atención {self.fecha.strftime('%Y-%m-%d %H:%M')} - Dr. {self.doctor.usuario.last_name}"
