menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class ContextMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        return context
