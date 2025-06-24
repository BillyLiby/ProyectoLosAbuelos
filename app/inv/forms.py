from django import forms

from .models import Categoria , SubCategoria, Marca, UnidadMedida, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descripcion', 'estado']
        labels = {
            'descripcion': "Descripción de la Categoría",
            "estado": "Estado"
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get("descripcion", "").upper()
        
        if not descripcion:
            return cleaned_data

        try:
            categoria_existente = Categoria.objects.get(
                descripcion__iexact=descripcion
            )
            
            if not self.instance.pk:  # Creando nueva
                raise forms.ValidationError("ERROR: Esta categoría ya existe")
            elif self.instance.pk != categoria_existente.pk:  # Editando
                raise forms.ValidationError("ERROR AL EDITAR: Categoría ya existe")
                
        except Categoria.DoesNotExist:
            pass
            
        cleaned_data["descripcion"] = descripcion
        return cleaned_data
        

class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descripcion')
    )
    class Meta:
        model=SubCategoria
        fields = ['categoria','descripcion','estado']
        labels = {'descripcion':"Sub Categoría",
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['categoria'].empty_label =  "Seleccione Categoría"
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get("descripcion", "").upper()
        
        if not descripcion:
            return cleaned_data

        try:
            categoria_existente = SubCategoria.objects.get(
                descripcion__iexact=descripcion
            )
            
            if not self.instance.pk:  # Creando nueva
                raise forms.ValidationError("ERROR: Esta Sub Categoría ya existe")
            elif self.instance.pk != categoria_existente.pk:  # Editando
                raise forms.ValidationError("ERROR AL EDITAR: Sub Categoría ya existe")
                
        except SubCategoria.DoesNotExist:
            pass
            
        cleaned_data["descripcion"] = descripcion
        return cleaned_data
    

class MarcaForm(forms.ModelForm):
    class Meta:
        model=Marca
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean(self):
        try:
            sc = Marca.objects.get(
                descripcion=self.cleaned_data["descripcion"].upper()
            )

            if not self.instance.pk:
                print("Registro ya existe")
                raise forms.ValidationError("ERROR: Esta marca ya existe")
            elif self.instance.pk!=sc.pk:
                print("Cambio no permitido")
                raise forms.ValidationError("ERROR AL EDITAR: Marca ya existe")
        except Marca.DoesNotExist:
            pass
        return self.cleaned_data

class UMForm(forms.ModelForm):
    class Meta:
        model=UnidadMedida
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Unidad de Medida",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    
    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get("descripcion", "").upper()
        
        if not descripcion:
            return cleaned_data

        try:
            um_existente = UnidadMedida.objects.get(
                descripcion__iexact=descripcion
            )
            
            if not self.instance.pk:  # Creando nueva
                raise forms.ValidationError("ERROR: Esta unidad de medida ya existe")
            elif self.instance.pk != um_existente.pk:  # Editando
                raise forms.ValidationError("ERROR AL EDITAR: Unidad de medida ya existe")
                
        except UnidadMedida.DoesNotExist:
            pass
            
        cleaned_data["descripcion"] = descripcion
        return cleaned_data

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'codigo_barra', 'descripcion', 'estado',
                  'precio', 'existencia', 'ultima_compra',
                  'marca', 'subcategoria', 'unidad_medida', 'foto']
        exclude = ['um', 'fm', 'uc', 'fc']
        widget = {'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True

        # Aquí filtramos los datos inactivos
        self.fields['marca'].queryset = Marca.objects.filter(estado=True)
        self.fields['unidad_medida'].queryset = UnidadMedida.objects.filter(estado=True)
        self.fields['subcategoria'].queryset = SubCategoria.objects.filter(estado=True)