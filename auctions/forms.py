from django import forms

class formListing(forms.Form):
    title = forms.CharField(label="Title", max_length=40)
    description = forms.CharField(label="Description", max_length=100)
    startingBid = forms.DecimalField(label="Starting bid", max_digits=2)
    imageLink = forms.ImageField(label='Image URL', required=False)
    category = forms.CharField(label='Category', max_length=40)
