# Everyeye
Used to manage users, roles, permissions, resource information, etc

## Intrduction REST API
### 功能：实现用户，角色，用户组，权限，资源的管理
### 需求：
    - 一期
        - 具有 REST API
        - 具有客户端命令行操作
        - 所有操作进行权限控制
        - 提供OpenID、SSO、OAuth2.0 接口
        - 使用redis进行缓存session
        - 后端数据存储支持插件式管理：sqlite3, mysql 和 mongodb
        - 邮件消息订阅（不同层级的错误信息，具有优美的html海报和详细的错误附件）
        - 支持批量导入用户，分别支持excel, json 和txt格式
    - 二期
        - 支持bug列表，用户可以提交系统bug与改进建议
        - 支持系统package下载，一键安装
        - 权限控制，通过后台禁用某项权限，前台页面以及url访问返回404

### URL地址规范
    0. http://www.domain.com/article  展示总的文章
    1. http://www.domain.com/<username>  展示用户的主页，主页包括基本信息，热词，生活等等分类
    2. http://www.domain.com/<username>/article  展示用户文章
    3. http://www.domain.com/<username>/article/<article_uuid>  展示具体某篇文章
    4. http://www.domain.com/<username>/manage/article  用户管理自己的文章
    5. http://www.domain.com/<username>/manage/write-article  用户写文章
    6. http://www.domain.com/<username>/manage/category  用户管理目录分类
    7. http://www.domain.com/<username>/manage/keyword  用户管理关键词
    8. http://www.domain.com/<username>/manage/message  用户管理自己的消息，主要是站内消息
    9. http://www.domain.com/<username>/manage/log  用户查看自己的操作日志
    10. http://www.domain.com/<username>/manage/setting  用户设置
    11. http://www.domain.com/<username>/manage/profile  用户基本信息修改
    12. http://www.domain.com/<username>/manage/change-password    用户修改密码
    > 下面是超级管理员拥有的操作
    13. http://www.domain.com/<username>/manage/comment 管理评论
    14. http://www.domain.com/<username>/manage/language-rule 设置过滤敏感词
    15. http://www.domain.com/<username>/manage/audit-log 审计日志
    16. http://www.domain.com/<username>/manage/article-statistics 文章统计
    17. http://www.domain.com/<username>/manage/global-setting 全局设置

    18. http://www.domain.com/manage/user   管理用户
    19. http://www.domain.com/manage/role   管理角色
    20. http://www.domain.com/manage/right  管理权限
    21. http://www.domain.com/manage/resource   管理资源
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

### 想法
    1. 用户评论会产生一条评论消息，提示作者查看
    2. 评论展示，以文章标题，评论内容，时间，人等，并且可以删除，及时回复，引用，转载等等
    3. 用户个人信息提供pdf,word方式下载，当然需要进行权限控制，日志信息可以导出到excel文件中
    4. 可以支持博客文章归档

### 站内消息实现
    1. 数据结构
        chat_room 房间
            id, name(房间名称), participators(参与者), messages(消息), status(是否被暂停使用), create_at(创建时间)
        participator 参与者
            id, user_id, chat_rooms, messages, status(是否被禁言), create_at
        message 消息
            id, chat_room_id, participator_id, type(消息类型:single, group), content, create_at
        notice 通知（存在于redis处）
            sender_id, receiver_id, message_id, create_at
    2. 表结构关系
        参与者participator 与 房间chat_room 是多对多关系
        参与者participator 与 消息message 是一对多关系
        房间chat_room 与 消息message 是一对多关系

    3. 逻辑实现
        a. 默认创建 系统通知房间system_notice_room, 所有用户默认加入
        b. 用户A给用户B发送消息, 自动创建房间A_B, 消息类型为single,发送的消息通过notice表标记是否已读
        c. 聊天室消息, 用户A可以创建聊天室chat_room_xxx并发送消息, 消息的类型为gourp. 发送的瞬间将当前组的人员取出来按照notice表结构
            存储需要为哪些人发送消息, 消息会自动过期,用户读取之后也会自动删除
    4. 技术实现
        使用flask-socketio, 详情参考http://flask-socketio.readthedocs.io/en/latest/

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

