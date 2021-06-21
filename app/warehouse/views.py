from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from website.mixins import CheckAdminUserMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import (
    ProductCategory, ProductSubCategory, Product, WareHouse,
    ProductTransaction
)
from .forms import (
    WarehouseTransactionForm, WarehouseTransactionUpdateForm
)


class ProductCategoryList(CheckAdminUserMixin, ListView):
    model = ProductCategory
    template_name = 'warehouse/category/product_category_list.html'
    context_object_name = 'categories'


class ProductCategoryCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = ProductCategory
    fields = ('name', 'status', 'remark')
    template_name = 'warehouse/category/product_category_form.html'
    success_url = reverse_lazy('warehouse:product_category_list')
    success_message = 'Product Category was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Product Category'
        context['form_action'] = reverse_lazy('warehouse:product_category_add')
        return context


class ProductCategoryUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = ProductCategory
    fields = ('name', 'status', 'remark')
    template_name = 'warehouse/category/product_category_form.html'
    success_url = reverse_lazy('warehouse:product_category_list')
    success_message = 'Product Category was updated successfully'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Product Category - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'warehouse:product_category_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class ProductCategoryDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = ProductCategory
    http_method_names = ['get']
    success_url = reverse_lazy('warehouse:product_category_list')
    success_message = 'Product Category was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class ProductSubCategoryList(CheckAdminUserMixin, ListView):
    model = ProductSubCategory
    template_name = 'warehouse/category/product_subcategory_list.html'
    context_object_name = 'categories'


class ProductSubCategoryCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = ProductSubCategory
    fields = ('name', 'status', 'category', 'remark')
    template_name = 'warehouse/category/product_subcategory_form.html'
    success_url = reverse_lazy('warehouse:product_subcategory_list')
    success_message = 'Product Sub-Category was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Product Sub-Category'
        context['form_action'] = reverse_lazy('warehouse:product_subcategory_add')
        return context


class ProductSubCategoryUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = ProductSubCategory
    fields = ('name', 'status', 'category', 'remark')
    template_name = 'warehouse/category/product_subcategory_form.html'
    success_url = reverse_lazy('warehouse:product_subcategory_list')
    success_message = 'Product Sub-Category was updated successfully'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Product Sub-Category - ' + self.get_object().name
        context['form_action'] = reverse_lazy(
            'warehouse:product_subcategory_update',
            kwargs={'slug': self.get_object().slug}
        )
        return context


class ProductSubCategoryDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = ProductSubCategory
    http_method_names = ['get']
    success_url = reverse_lazy('warehouse:product_subcategory_list')
    success_message = 'Product Sub-Category was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class ProductList(CheckAdminUserMixin, ListView):
    model = Product
    template_name = 'warehouse/product/product_list.html'
    context_object_name = 'products'


class ProductCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = [
        'name', 'category', 'discipline', 'warehouse', 'image',
        'is_online_product', 'include_in_prescription',
        'required_prescription', 'remark', 'composition'
    ]
    success_url = reverse_lazy('warehouse:product_list')
    success_message = 'Product was created successfully'
    template_name = 'warehouse/product/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Product'
        context['form_action'] = reverse_lazy('warehouse:product_add')
        return context


class ProductUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = [
        'name', 'category', 'discipline', 'warehouse', 'image',
        'is_online_product', 'include_in_prescription',
        'required_prescription', 'remark', 'composition'
    ]
    success_url = reverse_lazy('warehouse:product_list')
    success_message = 'Product was updated successfully'
    template_name = 'warehouse/product/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Product'
        context['form_action'] = reverse_lazy(
            'warehouse:product_update',
            kwargs={'slug': self.kwargs['slug']}
        )
        return context


class ProductDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = Product
    http_method_names = ['get']
    success_url = reverse_lazy('warehouse:product_list')
    success_message = 'Product was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class WareHouseList(CheckAdminUserMixin, ListView):
    model = WareHouse
    template_name = 'warehouse/inventory/warehouse_list.html'
    context_object_name = 'warehouses'


class WareHouseCreate(CheckAdminUserMixin, SuccessMessageMixin, CreateView):
    model = WareHouse
    template_name = 'warehouse/inventory/warehouse_form.html'
    fields = [
        'name', 'discipline', 'status', 'remark',
    ]
    success_url = reverse_lazy('warehouse:warehouse_list')
    success_message = 'Warehouse was created successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Warehouse'
        context['form_action'] = reverse_lazy('warehouse:warehouse_add')
        return context


class WareHouseUpdate(CheckAdminUserMixin, SuccessMessageMixin, UpdateView):
    model = WareHouse
    template_name = 'warehouse/inventory/warehouse_form.html'
    fields = [
        'name', 'discipline', 'status', 'remark',
    ]
    success_url = reverse_lazy('warehouse:warehouse_list')
    success_message = 'Warehouse was updated successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Warehouse'
        context['form_action'] = reverse_lazy(
            'warehouse:warehouse_update',
            kwargs={'slug': self.kwargs['slug']}
        )
        return context


class WarehouseDelete(CheckAdminUserMixin, SuccessMessageMixin, DeleteView):
    model = WareHouse
    http_method_names = ['get']
    success_url = reverse_lazy('warehouse:warehouse_list')
    success_message = 'Warehouse was removed successfully'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.success_url)


class WarehouseProductList(CheckAdminUserMixin, ListView):
    template_name = 'warehouse/inventory/product_list.html'
    model = WareHouse
    context_object_name = 'products'

    def get_queryset(self):
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(warehouse=warehouse)
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        context['warehouse_name'] = warehouse.name
        context['warehouse_slug'] = warehouse.slug
        return context


class WarehouseTransactionList(CheckAdminUserMixin, ListView):
    model = ProductTransaction
    template_name = 'warehouse/inventory/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        transactions = ProductTransaction.objects.filter(
            product__warehouse=warehouse
        )
        return transactions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        context['warehouse_name'] = warehouse.name
        context['warehouse_slug'] = warehouse.slug
        return context


class WarehouseTransactionCreate(CheckAdminUserMixin, CreateView):
    model = ProductTransaction
    template_name = 'warehouse/inventory/transaction_form.html'
    form_class = WarehouseTransactionForm
    success_message = 'New Transaction added successfully'

    def get_form(self, form_class=None):
        form = super(WarehouseTransactionCreate, self).get_form(form_class)
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        form.fields['product'].queryset = Product.objects.filter(
            warehouse=warehouse
        )
        return form

    def form_valid(self, form):
        ProductTransaction.objects.create(
            product=form.cleaned_data['product'],
            user=self.request.user,
            transaction_type=form.cleaned_data['transaction_type'],
            rate=form.cleaned_data['rate'],
            quantity=form.cleaned_data['quantity'],
            discount=form.cleaned_data['discount'],
            brand=form.cleaned_data['brand'],
            company=form.cleaned_data['company']
        )
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'warehouse:warehouse_transaction',
            kwargs={'slug': self.kwargs['slug']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouse = WareHouse.objects.get(slug=self.kwargs['slug'])
        context['warehouse'] = warehouse
        context['form_title'] = 'Add New Transaction'
        context['form_action'] = reverse_lazy(
            'warehouse:warehouse_transaction_add',
            kwargs={'slug': self.kwargs['slug']}
        )
        return context


class WarehouseTransactionUpdate(CheckAdminUserMixin, UpdateView):
    model = ProductTransaction
    template_name = 'warehouse/inventory/transaction_update_form.html'
    form_class = WarehouseTransactionUpdateForm
    success_message = 'Transaction updated successfully'

    def form_valid(self, form):
        self.object = self.get_object()
        form.save()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            'warehouse:warehouse_transaction',
            kwargs={'slug': self.kwargs['warehouse']}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        warehouse = WareHouse.objects.get(slug=self.kwargs['warehouse'])
        context['warehouse'] = warehouse
        context['form_title'] = 'Update Transaction'
        context['form_action'] = reverse_lazy(
            'warehouse:warehouse_transaction_update',
            kwargs={
                'warehouse': self.kwargs['warehouse'],
                'pk': self.kwargs['pk']
            }
        )
        return context


class WarehouseTransactionDelete(CheckAdminUserMixin, DeleteView):
    model = ProductTransaction
    http_method_names = ['get']
    success_message = 'Transaction was removed successfully'

    def get_success_url(self):
        return reverse_lazy(
            'warehouse:warehouse_transaction',
            kwargs={'slug': self.kwargs['warehouse']}
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        messages.add_message(
            self.request, messages.SUCCESS, self.success_message
        )
        return HttpResponseRedirect(self.get_success_url())
