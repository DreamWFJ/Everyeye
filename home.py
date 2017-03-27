from flask_script import Manager
from app import create_app, sql_db
from app.cmd.cli import init_command

manager = Manager(create_app('default'))
manager = init_command(manager, sql_db)



if __name__ == '__main__':
    manager.run()
