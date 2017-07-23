from django.forms import ModelForm
from messenger.models import Attachement


class AttachementForm(ModelForm):
  class Meta:
    model = Attachement
    fields = ['attachement']