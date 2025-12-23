from django import forms 
from .models import Encuesta, Distribucion


class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['distribucion', 'titulo', 'descripcion']
        
        labels = {
            'distribucion': 'Distribución',
            'titulo': 'Título',
            'descripcion': 'Descripción',
        }
        
        widgets = {
            'distribucion': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título de la encuesta'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción de la encuesta', 'rows': 4}),
        }        
        error_messages = {
            'distribucion': {
                'required': 'Por favor, seleccione una distribución.',
            },
            'titulo': {
                'required': 'Por favor, ingrese el título de la encuesta.',
            },
            'descripcion': {
                'required': 'Por favor, ingrese la descripción de la encuesta.',
            },
        }

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)  # <<— lo recibimos desde la vista
        super().__init__(*args, **kwargs)

        if cliente:
            self.fields['distribucion'].queryset = Distribucion.objects.filter(cliente=cliente)
        else:
            self.fields['distribucion'].queryset = Distribucion.objects.none()  # seguridad
        

    def get_from(self):
        form = super().get_form()
        form.fields['distribucion'].queryset = Distribucion.objects.filter(
            cliente = self.request.user.profile.cliente.nombre
        )
        
        return form
        
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if Encuesta.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError('Ya existe una encuesta con este título.')
        return titulo
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return descripcion
    
    def clean_distribucion(self):
        distribucion = self.cleaned_data.get('distribucion')
        if not distribucion:
            raise forms.ValidationError('Por favor, seleccione una distribución.')
        return distribucion
    
    
    
class DistribucionForm(forms.ModelForm):
    class Meta:
        model = Distribucion
        fields = ['nombre', 'descripcion']
        
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la distribución'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el descripcion de la distribución', 'rows': 4}),
        }        
        error_messages = {
            'nombre': {
                'required': 'Por favor, ingrese el nombre de la distribución.',
            },
            'descripcion': {
                'required': 'Por favor, ingrese el descripcion de la distribución.',
            },
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Distribucion.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('Ya existe una distribución con este nombre.')
        return nombre
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError('El descripcion debe tener al menos 10 caracteres.')
        return descripcion
    