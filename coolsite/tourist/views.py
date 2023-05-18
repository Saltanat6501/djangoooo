from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .forms import *
from .models import Tourist, Category
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import TouristSerializer
from .utils import *


#openai.api_key = "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"


class TouristAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2


class TouristAPIList(generics.ListCreateAPIView):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = TouristAPIListPagination

class TouristAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    # authentication_classes = (TokenAuthentication, )


class TouristAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer
    permission_classes = (IsAdminOrReadOnly, )





class TouristHome(DataMixin, ListView):
    model = Tourist
    template_name = 'tourist/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Басты бет")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Tourist.objects.filter(is_published=True).select_related('cat')


def about(request):
    contact_list = Tourist.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tourist/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'Біз туралы'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'tourist/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мақала қосу")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'tourist/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Кері байланыс")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("Авторизация")


def pageNotFound(request, exception):#запростар туралы инфр. туратын TttpRequest класссына көрсететін ссылка
    return HttpResponseNotFound('<h1>Бет табылмады</h1>')


class ShowPost(DataMixin, DetailView):
    model = Tourist
    template_name = 'tourist/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class TouristCategory(DataMixin, ListView):
    model = Tourist
    template_name = 'tourist/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Tourist.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'tourist/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Тіркелу")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'tourist/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Кіру")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class TouristAPIView(generics.ListAPIView):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer
