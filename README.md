# Everyeye
Used to manage users, roles, permissions, resource information, etc

## Intrduction
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

### 需求实现思路：
    1、插件式数据库支持
        通过公共配置ini或者conf等类似的配置文件，默认值数据库使用sqlite3，可选项有mysql, mongodb, sqlalchemy, redis, memory
        在配置解析的时候，根据参数值，选择数据库对象，将其初始化
        每个对象都有统一的接口，只是底层实现方法不一样
    2、session缓存同样也支持redis和memcached或者内存
    3、具备命令行初始化数据库，创建超级用户默认配置，以及备份，删除数据库，表等
    4、实现统一的CRUD基础对象，其它如用户，角色，权限等具体实现自己的功能
    5、基于celery异步任务队列的邮件消息通知

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

### 大型程序结构

    调用关系图
### 扩展包安装
    pip install Flask-HTTPAuth

