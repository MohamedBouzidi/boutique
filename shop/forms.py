from django.forms import ModelForm, TextInput, Textarea, PasswordInput, FileInput, Select, CheckboxInput
from .models import Boutique, Product, Categorie


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
            'name': TextInput(attrs={'class': 'form-control'}),
            'price': TextInput(attrs={'class': 'form-control'}),
            'image': FileInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'quantite': TextInput(attrs={'class': 'form-control'}),
            'categorie': Select(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
        }