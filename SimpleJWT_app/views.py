from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse, FileResponse, HttpResponse
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .encryption import key_save
from .encryption.encryption_rsa import decrypt_data_on_private
from .seralizers import MyTokenObtainPairSerializer
import traceback

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RSABackend(ModelBackend):  # 重写了JWT验证的过程，先RSA密钥解密后再发token
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(username)
            print(password)
            decrypt_username = decrypt_data_on_private(username)
            decrypt_password = decrypt_data_on_private(password)
            print('解密username：' + decrypt_username)
            print('解密password：' + decrypt_password)
            user = User.objects.get(username=decrypt_username)
            if user.check_password(decrypt_password):
                return user
            else:
                return None

        except Exception as err:
            print('用户验证错误：' + str(err.args))
            print(traceback.format_exc())
            return None


def return_key(request):
    try:
        pub_key = key_save.public_key
        print('redis公钥：')
        print(pub_key)
        return JsonResponse({'request_status': 'success', 'pub_key': pub_key})
    except Exception as err:
        print('公匙获取错误：' + str(err.args))
        print(traceback.format_exc())
        return JsonResponse({'request_status': 'failed'})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def test_login(request):
    try:
        return JsonResponse({'request_status': 'success', 'err_msg': ''})
    except Exception as err:
        print('测试登录错误：' + str(err.args))
        print(traceback.format_exc())
        return JsonResponse({'request_status': 'failed'})


def index(request):
    try:
        return render(request, 'index.html')
    except Exception as err:
        print('首页错误：' + str(err.args))
        print(traceback.format_exc())
        return JsonResponse({'request_status': 'failed'})

