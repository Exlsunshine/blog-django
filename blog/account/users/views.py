#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import QueryDict

from blog.account.users.services import UserService
from blog.common.error import ParamsError
from blog.common.message import ErrorMsg
from blog.common.utils import Response, json_response


@json_response
def user_operate(request, uuid=None):
    if request.method == 'GET':
        if not uuid:
            response = user_list(request)
        else:
            response = user_get(request, uuid)
    elif request.method == 'POST':
        response = user_create(request)
    elif request.method == 'PUT':
        response = user_update(request, uuid)
    elif request.method == 'DELETE':
        response = user_delete(request, uuid)
    else:
        response = Response(code=405, data=ErrorMsg.REQUEST_METHOD_ERROR)
    return response


def user_get(request, uuid):
    """
    @api {get} /account/users/{uuid}/ user get
    @apiVersion 0.1.0
    @apiName user_get
    @apiGroup account
    @apiDescription 获取用户信息详情
    @apiPermission USER_SELECT
    @apiUse Header
    @apiSuccess {string} data 用户信息详情
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "data": {
            "remark": "C'est la vie",
            "gender": false,
            "create_at": "2017-12-06T09:15:49Z",
            "nick": "EternalZZX",
            "role": 1,
            "groups": 1
        }
    }
    @apiUse ErrorData
    @apiErrorExample {json} Error-Response:
    HTTP/1.1 404 Not Found
    {
        "data": "User not found"
    }
    """
    try:
        code, data = UserService(request).get(user_uuid=uuid)
    except Exception as e:
        code, data = getattr(e, 'code', 400), \
                     getattr(e, 'message', ErrorMsg.REQUEST_ERROR)
    return Response(code=code, data=data)


def user_list(request):
    """
    @api {get} /account/users/ user list
    @apiVersion 0.1.0
    @apiName user_list
    @apiGroup account
    @apiDescription 获取用户信息列表
    @apiPermission USER_SELECT
    @apiUse Header
    @apiParam {number} [page=0] 用户信息列表页码, 页码为0时返回所有数据
    @apiParam {number} [page_size=10] 用户信息列表页长
    @apiParam {string} [order_field] 用户信息列表排序字段
    @apiParam {string=desc, asc} [order="desc"] 用户信息列表排序方向
    @apiParam {string} [query] 搜索内容，若无搜索字段则全局搜索nick, role, group, remark
    @apiParam {string=nick, role, group, remark, DjangoFilterParams} [query_field] 搜索字段, 支持Django filter参数
    @apiSuccess {String} total 用户信息列表总数
    @apiSuccess {String} users 用户信息列表
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "data": {
            "total": 1,
            "users": [
                {
                    "nick": "EternalZZX",
                    "remark": "C'est la vie",
                    "role": 1,
                    "create_at": "2017-12-06T09:15:49Z",
                    "groups": 1
                }
            ]
        }
    }
    @apiUse ErrorData
    @apiErrorExample {json} Error-Response:
    HTTP/1.1 403 Forbidden
    {
        "data": "Order field permission denied"
    }
    """
    try:
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        order_field = request.GET.get('order_field')
        order = request.GET.get('order')
        query = request.GET.get('query')
        query_field = request.GET.get('query_field')
        code, data = UserService(request).list(page=page,
                                               page_size=page_size,
                                               order_field=order_field,
                                               order=order,
                                               query=query,
                                               query_field=query_field)
    except Exception as e:
        code, data = getattr(e, 'code', 400), \
                     getattr(e, 'message', ErrorMsg.REQUEST_ERROR)
    return Response(code=code, data=data)


def user_create(request):
    """
    @api {post} /account/users/ user create
    @apiVersion 0.1.0
    @apiName user_create
    @apiGroup account
    @apiDescription 创建用户
    @apiPermission USER_CREATE
    @apiUse Header
    @apiParam {string} username 用户名
    @apiParam {string} password 密码
    @apiParam {string} [nick={username}] 昵称
    @apiParam {number} [role_id] 用户角色ID
    @apiParam {string} [group_ids] 用户组ID列表，e.g.'2;9;32;43'
    @apiParam {number=0, 1} [gender] 性别, male=0, female=1
    @apiParam {string} [email] 电子邮箱地址
    @apiParam {string} [phone] 电话号码
    @apiParam {string} [qq] QQ号码
    @apiParam {string} [address] 收货地址
    @apiParam {number=0, 1} [status=1] 账号状态, Cancel=0, Active=1
    @apiParam {string} [remark] 备注
    @apiParam {number=0, 1, 2} [kwargs] 隐私设置, Private=0, Protected=1, Public=2
                                        参数名'gender_privacy', 'email_privacy',
                                        'phone_privacy', 'qq_privacy', 'address_privacy'
    @apiSuccess {string} data 创建用户信息详情
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "data": {
            "email_privacy": 0,
            "username": "user",
            "remark": null,
            "phone_privacy": 0,
            "uuid": "19890105-81dd-55fc-a202-914fbf1e88a1",
            "nick": "user",
            "qq": null,
            "address": null,
            "qq_privacy": 0,
            "create_at": "2017-12-15T03:18:25.564Z",
            "phone": null,
            "role": 2,
            "user": 33,
            "groups": [],
            "gender": null,
            "id": 33,
            "gender_privacy": 2,
            "address_privacy": 0,
            "email": null
        }
    }
    @apiUse ErrorData
    @apiErrorExample {json} Error-Response:
    HTTP/1.1 400 Bad Request
    {
        "data": "Duplicate identity field"
    }
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    nick = request.POST.get('nick')
    role_id = request.POST.get('role_id')
    group_ids = request.POST.get('group_ids')
    gender = request.POST.get('gender')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    qq = request.POST.get('qq')
    address = request.POST.get('address')
    status = request.POST.get('status')
    remark = request.POST.get('remark')
    kwargs = {}
    for key in UserService.USER_PRIVACY_FIELD:
        value = request.POST.get(key)
        if value is not None:
            kwargs[key] = value
    try:
        if isinstance(group_ids, (unicode, str)):
            group_ids = [group_id for group_id in group_ids.split(';') if group_id]
        else:
            group_ids = []
        code, data = UserService(request).create(username=username,
                                                 password=password,
                                                 nick=nick,
                                                 role_id=role_id,
                                                 group_ids=group_ids,
                                                 gender=gender,
                                                 email=email, phone=phone,
                                                 qq=qq, address=address,
                                                 status=status,
                                                 remark=remark, **kwargs)
    except Exception as e:
        code, data = getattr(e, 'code', 400), \
                     getattr(e, 'message', ErrorMsg.REQUEST_ERROR)
    return Response(code=code, data=data)


def user_update(request, uuid):
    """
    @api {put} /account/users/{uuid}/ user update
    @apiVersion 0.1.0
    @apiName user_update
    @apiGroup account
    @apiDescription 编辑用户
    @apiPermission USER_UPDATE
    @apiUse Header
    @apiParam {string} [username] 用户名
    @apiParam {string} [old_password] 旧密码
    @apiParam {string} [new_password] 新密码
    @apiParam {string} [nick] 昵称
    @apiParam {number} [role_id] 用户角色ID
    @apiParam {string} [group_ids] 用户组ID列表，e.g.'2;9;32;43'
    @apiParam {number=0, 1} [gender] 性别, male=0, female=1
    @apiParam {string} [email] 电子邮箱地址
    @apiParam {string} [phone] 电话号码
    @apiParam {string} [qq] QQ号码
    @apiParam {string} [address] 收货地址
    @apiParam {string} [remark] 备注
    @apiParam {number=0, 1, 2} [kwargs] 隐私设置, Private=0, Protected=1, Public=2
                                        参数名'gender_privacy', 'email_privacy',
                                        'phone_privacy', 'qq_privacy', 'address_privacy'
    @apiSuccess {string} data 编辑用户信息详情
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "data": {
            "email_privacy": 0,
            "username": "user",
            "remark": null,
            "phone_privacy": 0,
            "uuid": "19890105-81dd-55fc-a202-914fbf1e88a1",
            "nick": "user",
            "qq": null,
            "address": null,
            "qq_privacy": 0,
            "create_at": "2017-12-15T03:18:25.564Z",
            "phone": null,
            "role": 2,
            "user": 33,
            "groups": [],
            "gender": null,
            "id": 33,
            "gender_privacy": 2,
            "address_privacy": 0,
            "email": null
        }
    }
    @apiUse ErrorData
    @apiErrorExample {json} Error-Response:
    HTTP/1.1 404 Not Found
    {
        "data": "User not found"
    }
    """
    data = QueryDict(request.body)
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    nick = data.get('nick')
    role_id = data.get('role_id')
    group_ids = data.get('group_ids')
    gender = data.get('gender')
    email = data.get('email')
    phone = data.get('phone')
    qq = data.get('qq')
    address = data.get('address')
    remark = data.get('remark')
    kwargs = {}
    for key in UserService.USER_PRIVACY_FIELD:
        value = data.get(key)
        if value is not None:
            kwargs[key] = value
    try:
        if isinstance(group_ids, (unicode, str)):
            group_ids = [group_id for group_id in group_ids.split(';') if group_id]
        else:
            group_ids = None
        code, data = UserService(request).update(user_uuid=uuid,
                                                 username=username,
                                                 old_password=old_password,
                                                 new_password=new_password,
                                                 nick=nick,
                                                 role_id=role_id,
                                                 group_ids=group_ids,
                                                 gender=gender,
                                                 email=email, phone=phone,
                                                 qq=qq, address=address,
                                                 remark=remark, **kwargs)
    except Exception as e:
        code, data = getattr(e, 'code', 400), \
                     getattr(e, 'message', ErrorMsg.REQUEST_ERROR)
    return Response(code=code, data=data)


def user_delete(request, uuid):
    """
    @api {delete} /account/users/[uuid]/ user delete
    @apiVersion 0.1.0
    @apiName user_delete
    @apiGroup account
    @apiDescription 删除用户
    @apiPermission USER_DELETE
    @apiUse Header
    @apiParam {string} [id_list] 删除用户uuid列表，e.g.'7357d28a-a611-5efd-ae6e-a550a5b95487;
                                 3cd43d89-ab0b-54ac-811c-1f4bb9b3fab6', 当使用URL参数uuid时
                                 该参数忽略
    @apiParam {bool=true, false} [force=false] 强制删除
    @apiSuccess {string} data 用户删除信息详情
    @apiSuccessExample {json} Success-Response:
    HTTP/1.1 200 OK
    {
        "data": [
            {
                "status": "SUCCESS",
                "id": "7357d28a-a611-5efd-ae6e-a550a5b95487",
                "name": "test"
            }
        ]
    }
    @apiUse ErrorData
    @apiErrorExample {json} Error-Response:
    HTTP/1.1 403 Forbidden
    {
        "data": "Permission denied"
    }
    """
    data = QueryDict(request.body)
    force = data.get('force') == 'true'
    try:
        if uuid:
            id_list = [{'delete_id': uuid, 'force': force}]
        else:
            id_list = data.get('id_list')
            if not isinstance(id_list, (unicode, str)):
                raise ParamsError()
            id_list = [{'delete_id': delete_id, 'force': force} for delete_id in id_list.split(';') if delete_id]
        code, data = 400, map(lambda params: UserService(request).delete(**params), id_list)
        for result in data:
            if result['status'] == 'SUCCESS':
                code = 200
                break
    except Exception as e:
        code, data = getattr(e, 'code', 400), \
                     getattr(e, 'message', ErrorMsg.REQUEST_ERROR)
    return Response(code=code, data=data)