# coding=utf-8

from bookmark.app import create_app
from flask_script import Manager, Server

app = create_app()
manager = Manager(app)
manager.add_command('runserver', Server(
    use_reloader=True,
    use_debugger=True,
    host='127.0.0.1',
    port=5000
))

if __name__ == '__main__':
    manager.run()
