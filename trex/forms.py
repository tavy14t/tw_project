from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(
        required=True
    )


class AvatarForm(forms.Form):
    url = forms.FileField(
        label='Select an image for your profile'
    )
