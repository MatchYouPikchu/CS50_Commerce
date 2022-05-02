from django import forms

class formListing(forms.Form):
    title = forms.CharField(label="Title", max_length=40)
    description = forms.CharField(label="Description", max_length=100)
    startingBid = forms.DecimalField(label="Starting bid", max_digits=5)
    imageLink = forms.ImageField(label='Image URL', required=False)
    category = forms.CharField(label='Category', max_length=40)

class formBid(forms.Form):
    bid = forms.DecimalField(label='User bid', max_digits=2)

class formComment(forms.Form):
    comment = forms.CharField(label="Comment", max_length=200)
