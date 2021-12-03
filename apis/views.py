from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from contents.models import Content, Image, FollowRelation


# Create your views here.

# CBV 기반의 api 구현
@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):

    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,

        }
        return JsonResponse(result, status=status)

    # 유저 생성 및 예외처리 구현


# 회원가입
class UserCreateView(BaseView):
    # post 입력 처리 및 검증 구현
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해 주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해 주세요.', status=400)
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            return self.response(message='이메일을 입력해 주세요.', status=400)

        # 예외 처리
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디 입니다.', status=400)

        return self.response({'user.id': user.id})


# 로그인 뷰
class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해 주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해 주세요.', status=400)

        # authenticate 함수는 username, password이 일치하지 않을경우, None을 반환.
        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.response(message='아이디 또는 비밀번호가 일치하지 않습니다.', status=400)
        login(request, user)

        return self.response()


# 로그아웃
class UserLogoutView(BaseView):
    def get(self, request):
        logout(request)
        return self.response()


# 게시글 생성
class ContentCreateView(BaseView):
    def post(self, request):
        text = request.POST.get('text', '').strip()
        content = Content.objects.create(user=request.user, text=text)

        for idx, file in enumerate(request.FILES.values()):
            Image.objects.create(content=content, image=file, order=idx)

        return self.response({})


# 팔로우
@method_decorator(login_required, name='dispatch')
class RelationCreateView(BaseView):
    def post(self, request):
        # 팔로우 버튼을 눌렀을 때, 발생하는 api
        try:
            user_id = request.POST.get('id', '')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        # 팔로우 관계가 있는지 확인하는 api
        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            relation = FollowRelation.objects.create(follower=request.user)

        # followee에 저장 api
        try:
            if user_id == request.user.id:
                raise IntegrityError

            relation.followee.add(user_id)
            relation.save()
        except IntegrityError:
            return self.response(message='잘못된 요청입니다.', status=400)

        return self.response({})


# 언팔로우
@method_decorator(login_required, name='dispatch')
class RelationDeleteView(BaseView):
    def post(self, request):
        # 언팔로우 버튼을 눌렀을 때, 사용자가 있는지 확인하는 api
        try:
            user_id = request.POST.get('id', '')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        # 언팔로우 할수있는 관계가 형성되어있는지 확인하는 api
        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)

        # 자기자신을 언팔로우 하는지 확인하는 api
        try:
            if user_id == request.user.id:
                raise IntegrityError

            relation.followee.remove(user_id)
            relation.save()
        except IntegrityError:
            return self.response(message='잘못된 요청입니다.', status=400)

        return self.response({})


class UserInfoGetView(BaseView):
    def get(self, request):
        username = request.GET.get('username','').strip()
        try:
            user = User.objects.get(username = username)
        except user.DoesNotExist:
            self.response(message = "사용자를 찾을 수 없습니다.", status = 404)

        return self.response({'username': username, 'email': user.email, 'id': user.id})




