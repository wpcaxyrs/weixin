from django.shortcuts import render,HttpResponse, redirect
from app01 import models
from django.http import JsonResponse
import requests
import json


def index(request):
    """
    首页
    :param request:
    :return:
    """
    user_id = request.session["userinfo"]['id']

    return render(request, 'index.html')


def login(request):
    '''
    用户登录界面
    :param request:用户输入参数
    :return: 对则跳转index，错则
    '''
    if request.method == 'GET':
        return render(request,'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    obj_user = models.User_info.objects.filter(name=user,pwd=pwd).first()
    if not obj_user:
        return render(request, 'login.html', {'msg': '用户密码错误'})
    request.session['userinfo'] = {'id': obj_user.id, 'name': obj_user.name}
    return redirect('/index/')

# 请求验证：
def get_qrcode(request):
    ret = {"status":True, 'data': None}

    access_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_url}&response_type=code&scope=snsapi_userinfo&state={state}#wechat_redirect"
    url = access_url.format(
        appid='wx12e7f9fe1853727f',
        redirect_url="http://118.24.89.136:8000/get_wx_id/",
        state=request.session['userinfo']['id']

    )
    ret['data'] = url

    return JsonResponse(ret)

def get_wx_id(request):
    """
    获取微信ID，并更新到数据库
    :param request:
    :return:
    """
    code = request.GET.get('code')
    state = request.GET.get('state')

    # 获取该用户openID
    r1 = requests.get(
        url="https://api.weixin.qq.com/sns/oauth2/access_token",
        params={
            "appid": "wx12e7f9fe1853727f",
            "secret": "7b8e78f26fbf096614ed67620f243261",
            "code": code,
            "grant_type": "authorization_code",
        }
    ).json()
    # 获取到openid表示用户授权成功
    wx_id = r1.get("openid")
    user = models.User_info.objects.filter(id=state).first()
    if not user.wx_id:
        user.wx_id = wx_id
        user.save()
    return HttpResponse("授权成功")

def test(request):
    user_list = models.User_info.objects.all()

    return render(request, 'test.html', {'user_list': user_list})


def send_msg(request):
    """
    单条发送消息！

    :param request:
    :return:
    """
    id = request.session['userinfo']['id']
    obj_user = models.User_info.objects.filter(id=id).first()
    # 书写token属性
    r1 = requests.get(
        # 向微信发送get请求
        url="https://api.weixin.qq.com/cgi-bin/token",
        # 包含的信息内容，一般在url后面直接显示？appid=‘’&secret=''
        params={
            'grant_type': 'client_credential',
            'appid': 'wx12e7f9fe1853727f',
            'secret': '7b8e78f26fbf096614ed67620f243261',
        }
    )

    access_token = r1.json().get('access_token')
    #
    wx_id = 'oc-Z10h99zGtS1bvhOLqBS3-fedg'
    body = {
        "touser": wx_id,
        "msgtype": 'text',
        "text": {
            "content": 'hello~~~秋姐减肥了！！！！',
            # "media_id": "2nt4ybZyHhfRJDze3ZqhkbWbff6vuvj7BvoiJMNdUbXQPSiehOjDMvRI83Q7LiR3",
         },
        # {
        # "touser": wx_id,
        # "msgtype": "image",
        # "image":
        #     {
        #         "type": "image",
        #         "media_id": "2nt4ybZyHhfRJDze3ZqhkbWbff6vuvj7BvoiJMNdUbXQPSiehOjDMvRI83Q7LiR3",
        #         "created_at": 1534154207
        #     }
        # },

    }
    r2 = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/custom/send",
        params={
            "access_token": access_token
        },
        data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')
    )
    print(r2.text)
    print(request.body)
    print(request)
    return HttpResponse('ok')


def send_temp(request):
    """
    模板发送
    :param request:
    :return:
    """
    id = request.session['userinfo']['id']
    obj_user = models.User_info.objects.filter(id=id).first()

    r1 = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": 'wx12e7f9fe1853727f',
            "secret": '7b8e78f26fbf096614ed67620f243261',
        }
    )
    access_token = r1.json().get('access_token')
    print(access_token)

    wx_id = 'oc-Z10oNv-bbCSGDdkN3iDAlo2TM'

    body = {
        'touser': wx_id,
        "template_id": 'vCMa02LfLCb0Qyldk-FQmT6lZotHHw9UhGMkj1Irx3Y',
        "data": {
            'user':{
                'value': 'jijijii',
                'color': '#173177'
            }
        }
    }

    r2 = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/template/send",
        params={
            'access_token': access_token
        },
        data=json.dumps(body)
    )

    print(r2.text)

    return HttpResponse('2333333')



