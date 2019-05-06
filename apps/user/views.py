from django.shortcuts import render,redirect
import re

from django.urls import reverse

from user.models import User
import time


# Create your views here.
#/user/register
def register(request):
    '''注册'''
    if request.method == 'GET':
        ''''显示注册页面'''
        return render(request, 'register.html')
    else:
        # 进行注册处理

        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg':'必填项不能为空'})

        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg':'邮箱格式不正确'})

        # 校验是否勾选用户协议
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请勾选用户协议'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理: 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答，跳转到首页（反向映射）
        return redirect(reverse('goods:index'))




            




