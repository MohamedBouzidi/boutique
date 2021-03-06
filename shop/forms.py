from django.forms import ModelForm, TextInput, Textarea, PasswordInput, FileInput, Select, CheckboxInput
from .models import Boutique, Product, Categorie, Picture, BusinessUser


class BusinessUserForm(ModelForm):
    class Meta:
        model = BusinessUser
        fields = ['description', 'type']
        widgets = {
            'description': Textarea(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'})
        }


class BoutiqueForm(ModelForm):
    class Meta:
        model = Boutique
        fields = ['name', 'processing_time', 'address', 'logo', 'description', 'facebook_link', 'instagram_link', 'phone']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'processing_time': TextInput(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'logo': FileInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'facebook_link': TextInput(attrs={'class': 'form-control'}),
            'instagram_link': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'active', 'quantite', 'categorie', 'type']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'price': TextInput(attrs={'class': 'form-control', 'id': 'price'}),
            'image': FileInput(attrs={'class': 'form-control', 'id': 'image'}),
            'description': Textarea(attrs={'class': 'form-control', 'id': 'description'}),
            'quantite': TextInput(attrs={'class': 'form-control', 'id': 'quantite'}),
            'categorie': Select(attrs={'class': 'form-control', 'id': 'categorie'}),
            'type': Select(attrs={'class': 'form-control', 'id': 'type'}),
        }


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['name']
        widgets = {
            'name': FileInput(attrs={'class': 'form-control'})
        }