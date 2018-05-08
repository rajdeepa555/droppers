from django import forms
from .models import EbayPriceFormula

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = EbayPriceFormula
        fields = ('ebay_final_value_fee','ebay_listing_fee','paypal_fees_perc','paypal_fees_fixed','perc_margin','fixed_margin') #Note that we didn't mention user field here.

    def save(self):
        user_profile = super(UserProfileForm, self).save(commit=False)
        user_profile.save()
        return user_profile