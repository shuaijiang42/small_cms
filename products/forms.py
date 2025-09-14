from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Product, NutritionalInformation, ProductNutritionalValue

from django.forms import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'is_active']

class NutritionalInformationForm(forms.ModelForm):
    class Meta:
        model =NutritionalInformation
        fields = ['name', 'unit']


class BaseProductNutritionalValueFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_value = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                has_value = True
        if not has_value:
            raise forms.ValidationError("Debes añadir al menos un valor nutricional.")

ProductNutritionalValueFormSet = inlineformset_factory(
    Product,
    ProductNutritionalValue,
    fields=["nutritional_info", "value"],
    extra=1,
    can_delete=True,
    formset=BaseProductNutritionalValueFormSet,

)