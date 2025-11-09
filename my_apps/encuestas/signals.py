from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Respuesta, DatosDistribucion


@receiver(post_save, sender=Respuesta)
def actualizar_cuota(sender, instance, created, **kwargs):
    if not created:
        return
    
    # Buscar la cuota que coincida con los datos de la respuesta
    cuota = DatosDistribucion.objects.filter(
        encuestador=instance.encuestador,
        distribucion=instance.encuesta.distribucion,
        edad=instance.edad,
        genero=instance.genero,
        barrio=instance.barrio
    ).first()

    if cuota:
        cuota.completadas = DatosDistribucion.objects.filter(id=cuota.id).values_list('completadas', flat=True).first() + 1
        if cuota.completadas > cuota.cuota_total:
            cuota.completadas = cuota.cuota_total  # evita pasarse
        cuota.save(update_fields=['completadas'])