from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Prefetch
from .models import Product, NutritionalInformation, ProductNutritionalValue
from .forms import ProductForm, NutritionalInformationForm, ProductNutritionalValueFormSet
from django.views import View

# Create your views here.

class NutritionalInformationListView(ListView):
    model = NutritionalInformation
    template_name = 'nutrition/nutritionalinformation_list.html'
    context_object_name = 'nutritional_informations'

class NutritionalInformationCreateView(CreateView):
    model = NutritionalInformation
    form_class = NutritionalInformationForm
    template_name = 'nutrition/nutritionalinformation_form.html'
    success_url = reverse_lazy('nutritionalinformation-list')

class NutritionalInformationUpdateView(UpdateView):
    model = NutritionalInformation
    form_class = NutritionalInformationForm
    template_name = 'nutrition/nutritionalinformation_form.html'
    success_url = reverse_lazy('nutritionalinformation-list')

class NutritionalInformationDetailView(DetailView):
    model = NutritionalInformation
    template_name = 'nutrition/nutritionalinformation_detail.html'
    context_object_name = 'nutritional_information'

class NutritionalInformationDeleteView(DeleteView):
    model = NutritionalInformation
    template_name = 'nutrition/nutritionalinformation_confirm_delete.html'
    success_url = reverse_lazy('nutritionalinformation-list')



class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
            Prefetch('nutritional_values', queryset=ProductNutritionalValue.objects.select_related('nutritional_info'))
        )
        # Filtering
        name = self.request.GET.get('name')
        status = self.request.GET.get('status')
        if name:
            queryset = queryset.filter(name__icontains=name)
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        return queryset


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = ProductNutritionalValueFormSet()
        return render(request, self.template_name, {"form": form, "formset": formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = ProductNutritionalValueFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form, "formset": formset})
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.form_class(instance=product)
        formset = ProductNutritionalValueFormSet(instance=product)
        return render(request, self.template_name, {"form": form, "formset": formset, "object": product})

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = self.form_class(request.POST, instance=product)
        formset = ProductNutritionalValueFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form, "formset": formset, "object": product})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

class ProductNutritionalValueDeleteView(DeleteView):
    model = ProductNutritionalValue
    template_name = "products/nutritionalvalue_confirm_delete.html"
    context_object_name = "nutritional_value"

    def get_success_url(self):
        return reverse_lazy("product-detail", kwargs={"pk": self.object.product.id})
    

class ProductNutritionalValuesUpdateView(View):
    template_name = "products/product_nutritional_values_form.html"

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        formset = ProductNutritionalValueFormSet(instance=product)
        return render(request, self.template_name, {"product": product, "formset": formset})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        formset = ProductNutritionalValueFormSet(request.POST, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect("product-detail", pk=product.id)
        return render(request, self.template_name, {"product": product, "formset": formset})
