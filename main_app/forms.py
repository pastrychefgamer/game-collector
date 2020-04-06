from django.forms import ModelForm
from .models import Outcome


class OutcomeForm(ModelForm):
    class Meta:
        model = Outcome
        fields = ['date', 'playTime']
