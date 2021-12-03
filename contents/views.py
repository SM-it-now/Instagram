from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Content, FollowRelation

# Create your views here.
# 메인화면 뷰
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    # 직접 pk를 지적하지 않기 때문에, get_context_data 함수를 추가해주어야 함. --> **kwargs에 pk값이 들어온다.
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        user = self.request.user

        # followees 변수에 follower가 user로 필터를 하고, 얻을 값을 리스트 형태로 followee의 id 값을 저장한다.
        followees = FollowRelation.objects.filter(
            follower=user
        ).values_list('followee__id', flat=True)

        # 인스타 피드에는 본인이 작성한 글과 팔로우한 사람의 글이 출력되어야 함.
        # --> 변수에 본인의 id와 앞서 followees들의 id 값들이 저장된 리스트를 더한 값을 변수에 저장한다.
        lookup_user_ids = [user.id] + list(followees)

        # all() 메서드 보다 select(prefetch)_related() 메서드를 사용해야 성능이 향상된다.
        # select_related()는 ForeignKey, OneToOne 관계에서 사용된다.
        # prefetch_related()는 ManyToMany 관계에서 사용된다.
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set').filter(
            user__id__in=lookup_user_ids
        )
        return context


# 팔로우 화면 뷰
@method_decorator(login_required, name='dispatch')
class RelationView(TemplateView):
    template_name = 'relation.html'

    def get_context_data(self, **kwargs):
        context = super(RelationView, self).get_context_data(**kwargs)
        user = self.request.user

        # 내가 팔로우 하고 있는 사람들을 확인.
        try:
            followers = FollowRelation.objects.get(follower=user).followee.all()
            context['followees'] = followers
            context['followees_ids'] = list(followers.values_list('id', flat=True))
        except FollowRelation.DoesNotExist:
            pass

        # 날 팔로우 하는 사람들을 확인.
        context['followers'] = FollowRelation.objects.select_related('follower').filter(followee__in=[user])

        return context

