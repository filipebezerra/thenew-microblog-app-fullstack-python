from app import app
from app.models import db, User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
        use_debugger=False,
        passthrough_errors=True
    )