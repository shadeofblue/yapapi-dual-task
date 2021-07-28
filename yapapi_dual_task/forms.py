from django import forms


class BlenderForm(forms.Form):
    scene_file = forms.FileField(help_text="Blender scene file", required=True)
    x = forms.CharField(help_text="x dimension")
    y = forms.CharField(help_text="y dimension")
    frame = forms.CharField(help_text="frame number")
