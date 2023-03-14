from django import forms

from .models import Cliente,AlquilerTubos, LiquidacionEnc,LiquidacionDet

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields=['nombres','apellidos','tipo',
            'celular','estado','direccion1','direccion2','direccion3','tipo_iva','cuit']
        exclude = ['um','fm','uc','fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class AlquilerForm(forms.ModelForm):
    class Meta:
        model=AlquilerTubos
        fields=['idpedido','fecha','cliente','fecha_entrega','fecha_retiro','codigo','descripcion','codigo_barra','fecha_venc']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['descripcion'].widget.attrs['readonly'] = True
        self.fields['codigo_barra'].widget.attrs['readonly'] = True
        self.fields['fecha_venc'].widget.attrs['readonly'] = True
        self.fields['idpedido'].widget.attrs['readonly'] = True
        self.fields['cliente'].widget.attrs['readonly'] = True
        self.fields['fecha'].widget.attrs['readonly'] = True
        
class LiquidacionEncForm(forms.ModelForm):
    class Meta:
        model=LiquidacionEnc
        fields=['fecha','mes','fecha_desde','fecha_hasta','realizada']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class LiquidacionDetForm(forms.ModelForm):
    class Meta:
        model=LiquidacionDet
        fields=['idliqenc','idalq','fecha_desde','fecha_hasta','dias','cliente','codigo_tubo']
       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })       