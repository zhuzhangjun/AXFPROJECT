## 一、项目结构
- 首页
- 闪购超市
- 购物车
    ```
    订单系统
    支付系统
    评价系统
    物流系统
    ...
    ```
- 我的
    ```
    用户系统
    ```

## 二、布局
- 百分比布局
    相对于父元素.


- rem
    相对于body节点 字体大小的比例。

## 三、基础模板
`base.html`头部、尾部是一致的，先完成基本结构，以及相关文件导入;

`首页home.html、闪购超市maket.html、购物车cart.html、我的mine.html` 四个页面都是继承自基础模板;

## 四、首页 -- 轮播图(导航、每日必购买)
- 数据分析
    ```
    insert into axf_wheel(img,name,trackid) values("http://img01.bqstatic.com//upload/activity/2017031716035274.jpg@90Q.jpg","酸奶女王","21870"),("http://img01.bqstatic.com//upload/activity/2017031710450787.jpg@90Q.jpg","优选圣女果","21869"),("http://img01.bqstatic.com//upload/activity/2017030714522982.jpg@90Q.jpg","伊利酸奶大放价","21862"),("http://img01.bqstatic.com//upload/activity/2017032116081698.jpg@90Q.jpg","鲜货直供－窝夫小子","21770"),("http://img01.bqstatic.com//upload/activity/2017032117283348.jpg@90Q.jpg","鲜货直供－狼博森食品","21874");


    img 商品图片地址
    name 商品名称
    trackid 商品id
    ```

- 模型类
    ```
    # 基础 类
    class Base(models.Model):
        img = models.CharField(max_length=100)
        name = models.CharField(max_length=100)
        trackid = models.CharField(max_length=20)

        class Meta:
            abstract = True

        def __str__(self):
            return self.name


    # 轮播图 模型类
    class Wheel(Base):
        class Meta:
            db_table = 'axf_wheel'


    # 导航 模型类
    class Nav(Base):
        class Meta:
            db_table = 'axf_nav'

    # 每日必购 模型类
    class Mustbuy(Base):
        class Meta:
            db_table = 'axf_mustbuy'

    # 商品部分内容
    class Shop(Base):
        class Meta:
            db_table = 'axf_shop'
    ```


## 五、首页 -- 主体商品
- 数据分析
    ```
    # 主体内容数据
    # 模型名称 Mainshow
    # 模型属性
    insert into axf_mainshow
    (trackid,name,img,categoryid,brandname,
    img1,childcid1,productid1,longname1,price1,marketprice1,
    img2,childcid2,productid2,longname2,price2,marketprice2,
    img3,childcid3,productid3,longname3,price3,marketprice3)

    values
    ("21782","优选水果","http://img01.bqstatic.com//upload/activity/2017031018205492.jpg@90Q.jpg","103532","爱鲜蜂","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164159_996462.jpg@200w_200h_90Q","103533","118824","爱鲜蜂·特小凤西瓜1.5-2.5kg/粒","25.80","25.8","http://img01.bqstatic.com/upload/goods/201/611/1617/20161116173544_219028.jpg@200w_200h_90Q","103534","116950","蜂觅·越南直采红心火龙果350-450g/盒","15.3","15.8","http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164119_550363.jpg@200w_200h_90Q","103533","118826","爱鲜蜂·海南千禧果400-450g/盒","9.9","13.8");

    trackid 跳转页面ID
    name    商品分类名称
    img     分类图片
    categoryid  分类ID        【例如  优选水果】
    brandname   品牌名

    img1 商品图片
    childcid1   子类ID        【例如  国产水果、进口水果】
    productid1  商品ID
    longname1   商品名名称
    price1      商品折扣价格
    marketprice1    商品原价
    ```


# 六、闪购超市
```
insert into axf_goods
(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum) values
("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);

    productid  商品ID
    productimg 商品图片
    productname 商品名称(有些可能不存在)
    productlongname 商品长名字
    isxf 精选
    pmdesc 买一送一
    specifics 规格
    price 价格
    marketprice 超市价格
    categoryid 分类ID
    childcid   子类ID
    childcidname 子类名字
    dealerid 详情id
    storenums 库存量
    productnum 销售量
```

- 元素获取
```
    $('.type-slider.type-item')  同一个元素包含的别名

    $('.type-slider .type-item') 包含(父子....)

    $('.type-slider>.type-item') 子元素(父子)
```

- js中cookie操作
```
# 设置cookie
# {exprires:3, path:'/'}
# exprires 过期时间
# path 路径
$.cookie(key, value, option)
$.cookie('typeIndex', $(this).index(),{exprires:3, path:'/'})


# 获取cookie
$.cookie(key)

# 删除cookie
$.cookie(key, null)
```

- 分类业务处理
```
点击(分类): 将typeIndex下标保存

页面刷新: 先获取typeIndex ==> 根据下标设置对应的分类样式

数据处理: typeIndex是存在cookie中(每次请求时，会自动带入到服务器) ==> 服务器中获取cookie中typeIndex  ==> 根据typeIndex获取categoryid  ==> 根据categoryid过滤数据
```

# 七、我的
```
# 用户模型类
class User(models.Model):
    # 账号
    account = models.CharField(max_length=20, unique=True)
    # 密码
    password = models.CharField(max_length=256)
    # 名字
    name = models.CharField(max_length=100)
    # 电话
    tel = models.CharField(max_length=20)
    # 地址
    address = models.CharField(max_length=256)
    # 头像
    img = models.CharField(max_length=100)
    # 等级
    rank = models.IntegerField(default=1)
    # token
    token = models.CharField(max_length=100)

- 注册
- 登录
- 退出
```

## 八、购物车
- 购物车 模型类
```
用户id
商品id
数量number
选中isselect
```

- 商品的添加删减
```

```


## 其他
```
git add *
git commit -m ''
git remote add origin git@github.com:iphone3/Python1807AXF.git
git push -u origin master


https://github.com/iphone3/Python1807AXF
```


## 集成第三方SDK
```
- 注册账号
- 创建应用
    APP_ID
    APP_KEY
- 下载SDK包
    导入项目中
- 查看官方文档
    示例代码
```