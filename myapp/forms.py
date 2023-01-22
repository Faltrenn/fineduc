from django import forms

from pyUFbr.baseuf import ufbr

class RegisterForm(forms.Form):
    stateOptions = []
    for uf in ufbr.list_uf:
        stateOptions.append([uf, uf])
    cityOptions = []
    for cityy in ufbr.list_cidades("AC"):
        cityOptions.append([cityy, cityy])
    
    name = forms.CharField(label="Nome", max_length=40, required=True)
    username = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(label="Email", required=True, error_messages={"invalid": "Digite um email válido"})
    cellphone = forms.CharField(label="Telefone", max_length=11, required=True)
    state = forms.ChoiceField(label="Estado", choices=stateOptions)
    city = forms.ChoiceField(label="Cidade", choices=cityOptions)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(), min_length=8)
