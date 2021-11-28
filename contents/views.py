from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Content

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    # 직접 pk를 지적하지 않기 때문에, get_context_data 함수를 추가해주어야 함. --> **kwargs에 pk값이 들어온다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # all() 메서드 보다 select(prefetch)_related() 메서드를 사용해야 성능이 향상된다.
        # select_related()는 ForeignKey, OneToOne 관계에서 사용된다.
        # prefetch_related()는 ManyToMany 관계에서 사용된다.
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set')
        return context
