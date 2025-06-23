from django import forms

from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombres','apellidos','tipo',
            'celular','estado']
        exclude = ['um','fm','uc','fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    
    def clean(self):
        try:
            nombres = self.cleaned_data.get("nombres", "").upper()
            apellidos = self.cleaned_data.get("apellidos", "").upper()
            
            if nombres and apellidos:
                cliente_existente = Cliente.objects.get(
                    nombres__iexact=nombres,
                    apellidos__iexact=apellidos
                )

                if not self.instance.pk:
                    raise forms.ValidationError("Cliente ya existe")
                elif self.instance.pk != cliente_existente.pk:
                    raise forms.ValidationError("No puede editar a un cliente existente")
                    
        except Cliente.DoesNotExist:
            pass
            
        return self.cleaned_data