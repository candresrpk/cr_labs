from django.shortcuts import render, redirect
from django.db.models import F
from .models import Encuesta, PermisosEncuesta, DatosDistribucion
from django.db.models import Sum
from django.db.models.functions import Round
from .forms import EncuestaForm, DistribucionForm
from my_apps.accounts.models import Profile, InvitacionEncuestador
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def encuestasListView(request):
    # obtienes el profile correctamente
    profile = Profile.objects.get(usuario=request.user)

    # usas el profile.id como corresponde (FK hacia Profile)
    encuestas_usuario = PermisosEncuesta.objects.filter(
        usuario_id=profile.id
    ).values_list('encuesta_id', flat=True)

    # obtienes las encuestas
    encuestas = Encuesta.objects.filter(id__in=encuestas_usuario)

    return render(request, 'encuestas/list.html', {
        "title": "Lista de Encuestas",
        "cargo": profile.cargo,
        "encuestas": encuestas
    })




# ================== CREAR ENCUESTA ==========================
@login_required
def crearEncuestaView(request):
    cliente = request.user.profile.cliente  # obtenemos el cliente dueño

    if request.method == 'POST':
        form = EncuestaForm(request.POST, cliente=cliente)  # ← SE PASA CLIENTE
        form_distribucion = DistribucionForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                encuesta = form.save()

                # Crear permiso para el usuario creador
                PermisosEncuesta.objects.create(
                    encuesta=encuesta,
                    usuario=request.user.profile
                )

            messages.success(request, "Encuesta creada exitosamente.")
            return redirect('encuestas:list')

    else:
        form = EncuestaForm(cliente=cliente)  # ← IMPORTANTE EN GET TAMBIÉN
        form_distribucion = DistribucionForm()

    return render(request, 'encuestas/crear.html', {
        'title': 'Crear Encuesta',
        'form_distribucion': form_distribucion,
        'form': form,
    })


# ================== CREAR DISTRIBUCIÓN ======================
@login_required
def crearDistribucionView(request):
    # Obtener cliente desde el perfil del usuario
    profile = request.user.profile
    cliente = profile.cliente

    if request.method == "POST":
        dist_form = DistribucionForm(request.POST)

        if dist_form.is_valid():
            nueva_dist = dist_form.save(commit=False)
            nueva_dist.cliente = cliente
            nueva_dist.save()

            messages.success(request, "Distribución creada correctamente.")
            return redirect('encuestas:crear')  # vuelve al modal original

        else:
            # Si el form falla, recargamos la vista principal con errores visibles en el modal
            encuesta_form = EncuestaForm(cliente=cliente)

            return render(request, "encuestas/crear.html", {
                'form': encuesta_form,
                'form_distribucion': dist_form,  # ← mantiene errores
                'open_modal_distribucion': True  # ← para abrir el modal
            })

    return redirect('encuestas:crear')

@login_required
def encuestaDetailView(request, encuesta_id):

    try:
        profile = Profile.objects.get(usuario=request.user)

        # Verifica que el usuario tenga permiso sobre la encuesta
        encuesta_usuario = PermisosEncuesta.objects.get(
            usuario_id=profile.id,
            encuesta_id=encuesta_id
        ).encuesta_id

        encuesta = Encuesta.objects.get(id=encuesta_usuario)

        # 📊 PROGRESO DE USUARIOS
        progreso = (
            DatosDistribucion.objects
                .filter(distribucion=encuesta.distribucion)
                .values("encuestador__username")  # Agrupa por encuestador
                .annotate(
                    nombre_encuestador = F("encuestador__username"),
                    total = Sum("cuota_total"),         # Campo real
                    completas = Sum("completadas"),     # Campo real con alias nuevo
                    porcentaje = Round(
                        Sum("completadas") * 100.0 / Sum("cuota_total"), 2
                    )
                )
        )

        # 🔗 Invitaciones activas del cliente al que pertenece el usuario
        invitaciones = InvitacionEncuestador.objects.filter(
            cliente=profile.cliente
        )

    except PermisosEncuesta.DoesNotExist:
        messages.error(request, "No tienes permiso para ver esta encuesta.")
        return redirect('encuestas:list')

    except Encuesta.DoesNotExist:
        messages.error(request, "La encuesta no existe.")
        return redirect('encuestas:list')


    return render(request, 'encuestas/detalle.html', {
        "title": f"Detalle de Encuesta: {encuesta.titulo}",
        "encuesta": encuesta,
        "progreso": progreso,
        "invitaciones": invitaciones
    })