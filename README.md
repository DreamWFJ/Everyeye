# Everyeye
Used to manage users, roles, permissions, resource information, etc

## Intrduction REST API
### 功能：实现用户，角色，用户组，权限，资源的管理
### 需求：
    具有 REST API
    具有客户端命令行操作
    所有操作进行权限控制
    提供OpenID、SSO、OAuth2.0 接口
    使用redis进行缓存session
    后端数据存储支持插件式管理：sqlite3, mysql 和 mongodb
    邮件消息订阅（不同层级的错误信息，具有优美的html海报和详细的错误附件）

### 注意点：
    用户的界面只有在登录成功后自动生成的，包括URL，也是在登录成功后生成
    所有的接口调用，命令行操作都有日志记录
    日志记录要求有统一的格式，详细的说明，频率等记录
    快速权限判定如何实现，基于异或操作？位操作？
    角色，用户，用户组的关系，权限资源的关系，角色与权限的关系，是否可以重叠

### 疑问
    1. 为什么需要在蓝图所在py导入视图，比如下面这样，否则会无法运行
        resource_blueprint = Blueprint('resource', __name__)
        from . import views
        from .logs import views
        from .persons import views
    2. 还有模板和静态文件的路径为什么是app目录下
        也可以在蓝图中直接指明位置
        admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

### 需求实现思路：
    1、插件式数据库支持
        通过公共配置ini或者conf等类似的配置文件，默认值数据库使用sqlite3，可选项有mysql, mongodb, sqlalchemy, redis, memory
        在配置解析的时候，根据参数值，选择数据库对象，将其初始化
        每个对象都有统一的接口，只是底层实现方法不一样
    2、session缓存同样也支持redis和memcached或者内存
    3、具备命令行初始化数据库，创建超级用户默认配置，以及备份，删除数据库，表等
    4、实现统一的CRUD基础对象，其它如用户，角色，权限等具体实现自己的功能
    5、基于celery异步任务队列的邮件消息通知
    6、参数配置最终加载为一个对象，或者将所有的配置变成实例的属性
    7、日志库切换的时候：比如每天一个表名，在更换名称的时候，需要暂时阻塞所有的写该表的操作，等表创建成功后再放行。可以在API写数据库处做一层队列，就celery任务队列

### 数据结构：
    用户（user）
        id, name, email, telephone, enabled, create_at, last_active_at, extra
    角色（role）
        id, enabled, create_at, name, extra, last_active_at
    用户组（user_group）
        id, name, description, enabled, last_active_at, create_at, extra
    权限（right）
        id, name, description, enabled,  create_at, extra, last_active_at
    资源（resource）
        id, name, description, create_at, extra, enabled, last_active_at
    id映射图
        id, user_id, role_id, right_id, resource_id, extra, create_at, last_update_at
    密码（password）
        id, user_id, password, create_at, expires_at, extra

### 用户，角色，权限，资源关系
    1、用户关联角色
    2、权限只分为：增0x01, 删0x02, 改0x04, 查0x08
    3、资源与权限进行组合，在为角色分配能够访问的资源的时候，进行设置资源权限组合
        权限控制：用户级别，普通用户只能操作自身，管理员可以操作所有
    4、权限实现：
        每个用户登陆的时候，自动创建一个对象，该对象中会加载所具有的资源以及访问该资源的权限，通过相应的属性或者方法就可以获取到权限列表或者是否具有该资源的访问权限
        在html渲染的时候，同样根据资源权限信息，生成渲染好的页面再返回浏览器，可以为登陆的用户保持已经渲染的页面，直到超时，或者内存不够时，自动对其清理



### 大型程序结构
```
.
├── app
│   ├── email.py
│   ├── __init__.py
│   ├── main
│   │   ├── errors.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── models.py
│   ├── static
│   │   └── favicon.ico
│   └── templates
│       ├── 404.html
│       ├── 500.html
│       ├── base.html
│       ├── index.html
│       ├── mail
│       │   ├── new_user.html
│       │   └── new_user.txt
│       └── user.html
├── config.py
├── manage.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── readme.md
├── requirements.txt
├── sqlite-example.png
└── tests
    ├── __init__.py
    └── test_basics.py
```
    调用关系图
### 扩展包安装
    pip install Flask-HTTPAuth

