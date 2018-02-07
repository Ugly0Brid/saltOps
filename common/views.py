from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def login(request):
    if request.method == 'POST':
        params = request.body.decode()
        params = json.loads(params)
        name = params.get('username')
        pwd = params.get('password')
        user = authenticate(username=name, password=pwd)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({"status": 0, "username": name})
        else:
            return JsonResponse({'status': -1, "error": "用户名或密码失败"})
    else:
        return JsonResponse({'status': -1, "error": "用户名或密码失败"})


def logout(request):
    try:
        auth_logout(request)
        return JsonResponse({"status": 0})
    except Exception as e:
        auth_logout(request)
        return JsonResponse({"status": -1})
