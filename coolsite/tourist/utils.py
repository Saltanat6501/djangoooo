from django.db.models import Count

from .models import *

menu = [{'title': "Біз туралы", 'url_name': 'about'},
        {'title': "Мақала қосу", 'url_name': 'add_page'},
        {'title': "Кері байланыс", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 20

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('tourist'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context