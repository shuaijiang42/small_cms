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

class ProductNutritionalValueForm(forms.ModelForm):
    class Meta:
        model = ProductNutritionalValue
        fields = ["nutritional_info", "value"]

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if product and not self.instance.pk:
            used_ids = product.nutritional_values.values_list(
                'nutritional_info_id', flat=True
            )
            self.fields['nutritional_info'].queryset = NutritionalInformation.objects.exclude(
                id__in=used_ids
            )

class BaseProductNutritionalValueFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_value = False

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                nutritional_info = form.cleaned_data.get('nutritional_info')
                value = form.cleaned_data.get('value')
                if nutritional_info and value:
                    has_value = True

        if not has_value:
            raise forms.ValidationError(
                "At least a nutritional information value is needed"
            )
 

ProductNutritionalValueFormSet = inlineformset_factory(
    Product,
    ProductNutritionalValue,
    form=ProductNutritionalValueForm,
    formset=BaseProductNutritionalValueFormSet,
    extra=1,
    can_delete=True,
)