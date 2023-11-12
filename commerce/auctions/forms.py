from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Max
from .models import *

"""
importing everything is not ideal
but best when developing atlast just edit those
"""

class createListing(forms.Form):
    name = forms.CharField(label="Name")
    description = forms.CharField(label="Desc :")
    image_url = forms.URLField(label="Image :")
    base_bid = forms.DecimalField(max_digits=10, decimal_places=2)
    catagory = forms.ChoiceField(choices=[(cat.id, str(cat)) for cat in Catagory.objects.all()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    def clean_base_bid(self):
        base_bid = self.cleaned_data.get('base_bid')
        if base_bid <= 0:
            raise ValidationError('Base bid must be greater than 0')
        return base_bid


class CatagoryFilter(forms.Form):
    catagory = forms.ChoiceField(choices=[(cat.id, str(cat)) for cat in Catagory.objects.all().order_by("type")])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class createBids(forms.Form):
    bid = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop('listing_id', None)
        super(createBids, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_bid(self):
        # print(self.cleaned_data)
        bid = self.cleaned_data.get('bid')

        highest_bid = Bid.objects.filter(listing_id=self.listing_id).aggregate(Max('bid_amount'))['bid_amount__max']
        if highest_bid is None:
            highest_bid = Listing.objects.get(id= self.listing_id).base_price

        if bid <= highest_bid:
            return False
        return bid


class createComment(forms.Form):
    comment = forms.CharField(max_length=255)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'