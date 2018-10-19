import hashlib
import os
import uuid
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Python1807AXF import settings
from app.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart, Order,OrderGoods


# 首页
def home(request):
    # 轮播图数据
    wheels = Wheel.objects.all()

    # 导航 数据
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    # 商品主体
    mainshows = MainShow.objects.all()

    data = {
        'title': '首页',
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptab':shoptab,
        'shopclass':shopclass,
        'shopcommend':shopcommend,
        'mainshows': mainshows
    }

    return render(request, 'home/home.html', context=data)

# 闪购超市
def market(request, categoryid, childid, sortid):
    # 分类数据
    foodtypes = Foodtypes.objects.all()

    # 获取点击 历史 [typeIndex]
    # 有typeIndex
    # 无typeIndex，默认0
    typeIndex = int(request.COOKIES.get('typeIndex',0))
    print(foodtypes[typeIndex])
    categoryid = foodtypes[typeIndex].typeid


    # 子类
    childtypenames = foodtypes.get(typeid=categoryid).childtypenames # 对应分类下 子类字符串
    childlist = []
    for item in childtypenames.split('#'):
        arr = item.split(':')
        obj = {'childname':arr[0], 'childid':arr[1]}
        childlist.append(obj)

    # 商品数据
    # goodslist = Goods.objects.all()[1:10]

    # 根据商品分类 数据过滤
    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else:   # 对应分类
        goodslist = Goods.objects.filter(categoryid=categoryid, childcid=childid)

    # 排序处理
    if sortid == '1':   # 销量排序
        goodslist= goodslist.order_by('productnum')
    elif sortid == '2': # 价格最低
        goodslist= goodslist.order_by('price')
    elif sortid == '3': # 价格最高
        goodslist= goodslist.order_by('-price')


    # 购物车数量问题
    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

    data = {
        'title': '闪购超市',
        'foodtypes':foodtypes,
        'goodslist':goodslist,
        'childlist':childlist,
        'categoryid':categoryid,
        'childid':childid,
        'carts': carts
    }

    return render(request, 'market/market.html', context=data)

# 购物车
def cart(request):
    token = request.session.get('token')
    carts = []
    if token:   # 已登录
        # 根据token获取对应用户
        user = User.objects.get(token=token)
        # 根据用户，获取对应购物车 数据
        carts = Cart.objects.filter(user=user).exclude(number=0)

    # 一个班级 对应 多个学生
    # 班级主表
    # 学生从表 【声明关系】

    responseDatra = {
        'title': '购物车',
        'carts': carts
    }


    return render(request, 'cart/cart.html', context=responseDatra)

# 我的
def mine(request):
    token = request.session.get('token')

    responseData = {
        'title': '我的',
        'payed': 0,
        'wait_pay': 0
    }

    if token:   # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = True

        # 获取订单信息
        orders = Order.objects.filter(user=user)
        payed = 0   # 已付款
        wait_pay = 0    # 待付款
        for order in orders:
            if order.status == 1:
                wait_pay += 1
            elif order.status == 2:
                payed += 1

        responseData['payed'] = payed
        responseData['wait_pay'] = wait_pay


    else:       # 未登录
        responseData['name'] = '未登录'
        responseData['rank'] = '无等级(未登录)'
        responseData['img'] = '/static/uploads/axf.png'
        responseData['islogin'] = False

    return render(request, 'mine/mine.html', context=responseData)

# 注册
def register(request):
    if request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.tel = request.POST.get('tel')
        user.address = request.POST.get('address')

        # 头像
        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDIA_ROOT, imgName)
        print(imgPath)
        file = request.FILES.get('file')
        print(file)
        with open(imgPath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        # token
        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

        # 保存到数据库
        user.save()

        # 状态保持
        request.session['token'] = user.token

        # 重定向
        return redirect('axf:mine')

    elif request.method == 'GET':
        return render(request, 'mine/register.html')


# 密码
def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()

# 退出登录
def quit(request):
    # request.session.flush()
    logout(request)
    return redirect('axf:mine')

# 登录
def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)
            if user.password != generate_password(password):    # 密码错误
                return render(request, 'mine/login.html', context={'error': '密码错误!'})
            else:   # 登录成功
                # 更新token
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()
                # 状态保持
                request.session['token'] = user.token
                return redirect('axf:mine')
        except:
            return render(request, 'mine/login.html', context={'error':'用户名有误，请检查后输入!'})

    elif request.method == 'GET':
        return render(request, 'mine/login.html')

# 用户验证
def checkuser(request):
    account = request.GET.get('account')
    try:
        user = User.objects.get(account=account)
        return JsonResponse({'msg':'用户名存在!', 'status':'-1'})
    except:
        return JsonResponse({'msg':'用户名可用!', 'status':'1'})

# 添加购物车
def addtocart(request):
    # goodsid
    goodsid = request.GET.get('goodsid')
    token = request.session.get('token')

    responseData = {
        'msg':'',
        'status':''
    }

    if token:   # 登录
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(goods=goods).filter(user=user)
        if carts.exists():  # 存在
            cart = carts.first()
            cart.number = cart.number + 1
            if goods.storenums < cart.number:
                cart.number = goods.storenums
            cart.save()
            responseData['msg'] = '添加购物车成功'
            responseData['status'] = 1
            responseData['number'] = cart.number
            return JsonResponse(responseData)
        else:           # 不在
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

            responseData['msg'] = '添加购物车成功'
            responseData['status'] = 1
            responseData['number'] = cart.number
            return JsonResponse(responseData)
    else:       # 未登录
        # ajax请求操作，是重定向不了的！
        # return redirect('axf:login')

        responseData['msg'] = '请登录后操作'
        responseData['status'] = '-1'

        return JsonResponse(responseData)

# 购物车删减
def subtocart(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    # 删减操作
    carts = Cart.objects.filter(user=user).filter(goods=goods)
    cart = carts.first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg': '删减成功',
        'status': '1',
        'number': cart.number
    }

    return JsonResponse(responseData)

# 修改选中状态
def changecartstatus(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    responseData = {
        'msg':'修改状态成功',
        'status':'1',
        'isselect': cart.isselect
    }

    return JsonResponse(responseData)

# 全选/取消全选
def changecartselect(request):
    isall = request.GET.get('isall')
    if isall == 'true':
        isall = True
    else:
        isall = False

    token = request.session.get('token')
    user = User.objects.get(token=token)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        cart.isselect = isall
        cart.save()

    responseData = {
        'status': '1',
        'msg':'全选/取消全选 操作成功'
    }

    return JsonResponse(responseData)

# 下单
def generateorder(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        # 生成订单
        order = Order()
        order.user = user
        order.number = str(uuid.uuid5(uuid.uuid4(), 'order'))
        order.save()

        carts = Cart.objects.filter(user=user).filter(isselect=True)
        for cart in carts:
            # 订单商品
            orderGoods = OrderGoods()
            orderGoods.order = order
            orderGoods.goods = cart.goods
            orderGoods.number = cart.number
            orderGoods.save()

            # 移除购物车
            cart.delete()

        responseData = {
            'status': '1',
            'msg': '订单生成成功(未付款)!',
            'orderid': order.id
         }

        return JsonResponse(responseData)

    else:
        return  JsonResponse({'msg':'用户登录后再操作'})

# 订单详情
def orderinfo(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)

    data = {
        'title':'订单详情',
        'order': order,
    }

    return render(request,'order/orderinfo.html', context=data)

# 订单处理
def changeorderstatusm(request):
    orderid = request.GET.get('orderid')
    status = request.GET.get('status')

    order = Order.objects.get(pk=orderid)
    order.status = status
    order.save()

    responseData = {
        'msg':'付款成功',
        'status':1
    }

    return JsonResponse(responseData)