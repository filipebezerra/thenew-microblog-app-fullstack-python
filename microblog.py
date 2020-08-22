from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Task': Task,
            'Message': Message, 'Notification': Notification}


if __name__ == "__main__":
    app.run(
        use_reloader=False,
        use_debugger=False,
        passthrough_errors=True,
        host='0.0.0.0'
    )
