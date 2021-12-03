from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogoutView, ContentCreateView, RelationCreateView, RelationDeleteView, UserInfoGetView


urlpatterns = [
    # 인증 api
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),
    path('v1/users/login/', UserLoginView.as_view(), name='apis_v1_user_login'),
    path('v1/users/logout/', UserLogoutView.as_view(), name='apis_v1_user_logout'),
    path('v1/users/get/', UserInfoGetView.as_view(), name='apis_v1_user_get'),

    # 게시물 api
    path('v1/contents/create/', ContentCreateView.as_view(), name='apis_v1_content_create'),

    # 팔로우 api
    path('v1/relations/create/', RelationCreateView.as_view(), name='apis_v1_relation_create'),
    path('v1/relations/delete/', RelationDeleteView.as_view(), name='apis_v1_relation_delete'),
]