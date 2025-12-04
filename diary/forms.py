# diary/forms.py
from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['dish', 'country', 'rating', 'description', 'photo', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.RadioSelect,                 # ← обязательно RadioSelect
            'tags': forms.TextInput(attrs={'placeholder': 'острые, веган, быстро'}),
            'dish': forms.TextInput(attrs={'placeholder': 'Например: Тако аль пастор'}),
        }

    # Чтобы форма не проходила без оценки и названия
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dish'].required = True
        self.fields['rating'].required = True
        self.fields['country'].required = True