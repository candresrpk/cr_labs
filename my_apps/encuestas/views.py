from django.shortcuts import render, redirect
from .models import Encuesta, PermisosEncuesta
from .forms import EncuestaForm, DistribucionForm
from my_apps.accounts.models import Profile
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
    form = EncuestaForm()
    form_distribucion = DistribucionForm()  # ← NECESARIO PARA QUE APAREZCA EN EL MODAL
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        form_distribucion = DistribucionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                encuesta = form.save()

                # Crear permiso para el usuario creador (opcional pero recomendado)
                PermisosEncuesta.objects.create(
                    encuesta=encuesta,
                    usuario=request.user.profile
                )

            messages.success(request, "Encuesta creada exitosamente.")
            return redirect('encuestas:list')

    context = {
        'title': 'Crear Encuesta',
        'form_distribucion': form_distribucion,
        'form': form,
    }
    return render(request, 'encuestas/crear.html', context)


# ================== CREAR DISTRIBUCIÓN ======================
@login_required
def crearDistribucionView(request):
    dist_form = DistribucionForm()

    if request.method == "POST":
        dist_form = DistribucionForm(request.POST)
        if dist_form.is_valid():
            dist_form.save()
            messages.success(request, "Distribución registrada correctamente.")

            # Si venimos desde el modal, nos devuelve a crear encuesta
            return redirect('encuestas:crear')

    return render(request, 'encuestas/crear_distribucion.html', {'dist_form': dist_form})