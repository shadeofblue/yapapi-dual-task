from django import forms


class BlenderForm(forms.Form):
    scene_file = forms.FileField(help_text="Blender scene file", required=True)
    x = forms.CharField(help_text="horizontal size in pixels", initial=100)
    y = forms.CharField(help_text="vertical size in pixels", initial=100)
    frame = forms.CharField(help_text="frame number", initial=1)
