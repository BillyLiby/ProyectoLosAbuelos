from django import forms

from .models import Proveedor, ComprasEnc

class ProveedorForm(forms.ModelForm):
    email = forms.EmailField(max_length=254)
    class Meta:
        model=Proveedor
        exclude = ['um','fm','uc','fc']
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    # Personalizar campo teléfono
        self.fields['telefono'].widget.attrs.update({
            'pattern': '[0-9]+',
            'inputmode': 'numeric',
            'maxlength': '10',
            'title': 'Ingrese solo números'
        })

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono
    
    def clean(self):
        try:
            sc = Proveedor.objects.get(
                descripcion=self.cleaned_data["descripcion"].upper()
            )

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("Registro Ya Existe")
            elif self.instance.pk!=sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("Cambio No Permitido")
        except Proveedor.DoesNotExist:
            pass
        return self.cleaned_data

class ComprasEncForm(forms.ModelForm):
    fecha_compra = forms.DateInput()
    fecha_factura = forms.DateInput()

    class Meta:
        model=ComprasEnc
        fields=['proveedor','fecha_compra','observacion',
            'no_factura','fecha_factura','sub_total',
            'descuento','total']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields['proveedor'].queryset = Proveedor.objects.filter(estado=True)
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

         # Atributos adicionales para no_factura
        self.fields['no_factura'].widget.attrs.update({
            'pattern': '[0-9]+',
            'inputmode': 'numeric',
            'maxlength': '20',
            'title': 'Ingrese solo números',
            'placeholder': 'Ej: 784456'
        })

        self.fields['fecha_compra'].widget.attrs['readonly'] = True
        self.fields['fecha_factura'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True

    def clean_no_factura(self):
        no_factura = self.cleaned_data.get('no_factura')
        if no_factura and not no_factura.isdigit():
            raise forms.ValidationError("El número de recibo debe contener solo números.")
        return no_factura