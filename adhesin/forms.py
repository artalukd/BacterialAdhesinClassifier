from django import forms


class UploadFileForm(forms.Form):

    upFile = forms.FileField(label="File:")
