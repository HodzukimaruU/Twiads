from django import forms

class AddCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
