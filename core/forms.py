# core/forms.py
from django import forms
from .models import Stage, Log

class StageForm(forms.ModelForm):
    poster_file = forms.FileField(required=False)

    class Meta:
        model = Stage
        fields = ['poster_file', 'title', 'cast', 'staff']
        
        # ラベルをなくす場合は label='' に
        labels = {
            'poster_file': '',
            'title': '',
            'cast': '',
            'staff': '',
        }
        
        # placeholder, class などを attrs で指定
        widgets = {
            'poster_file': forms.ClearableFileInput(
                attrs={
                    'class': 'custom-file-input',
                    'id': 'poster-upload',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'タイトル',
                }
            ),
            'cast': forms.Textarea(
                attrs={
                    'placeholder': '出演者（スペースやカンマ区切り）',
                    'rows': 3,
                }
            ),
            'staff': forms.Textarea(
                attrs={
                    'placeholder': 'スタッフ（スペースやカンマ区切り）',
                    'rows': 3,
                }
            ),
        }




class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['status', 'times', 'comment', 'watched_date']
        labels = {
            'status': 'ステータス',
            'times': '観劇回数',
            'comment': '',
            'watched_date': '観劇日',
        }
        widgets = {
            'status': forms.HiddenInput(),  # ← 例: hiddenにしてテンプレートで自力出す
            'times': forms.NumberInput(attrs={'placeholder': '回数'}),
            'comment': forms.Textarea(attrs={'placeholder': 'コメント', 'rows': 3}),
            'watched_date': forms.DateInput(attrs={'type': 'date'}),
        }
