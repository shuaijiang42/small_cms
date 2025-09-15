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
        formset = ProductNutritionalValueFormSet(
            instance=Product(),
            prefix='nutritional_values'
        )
        return render(request, self.template_name, {"form": form, "formset": formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        temp_instance = Product()

        formset = ProductNutritionalValueFormSet(
            request.POST,
            instance=temp_instance,
            prefix='nutritional_values'
        )
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form, "formset": formset})
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        product = self.object

        if self.request.POST:
            data['formset'] = ProductNutritionalValueFormSet(
                self.request.POST,
                instance=self.object,
                prefix='nutritional_values',
                form_kwargs={'product': product}  
            )
        else:
            data['formset'] = ProductNutritionalValueFormSet(
                instance=self.object,
                prefix='nutritional_values',
                form_kwargs={'product': product}  
            ) 
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        #import ipdb; ipdb.set_trace()
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('product-detail', kwargs={'pk': self.object.pk})
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')

class ProductNutritionalValuesUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ProductNutritionalValueFormSet(
                self.request.POST, instance=self.object
            )
        else:
            data['formset'] = ProductNutritionalValueFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)