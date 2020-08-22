import time
import sys
import json
from flask import render_template
from rq import get_current_job
from app import create_app, db
from app.models import Post, Task, User
from app.email import send_email


app = create_app()
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()

        task = Task.query.get(job.get_id())
        task.user.add_notification(
            'task_progress', {'task_id': job.get_id(), 'progress': progress})

        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        data = []
        i = 0
        user = User.query.get(user_id)
        total_posts = user.posts.count()
        _set_task_progress(0)
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                         'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)

        text_template = render_template('email/export_posts.txt', user=user)
        html_template = render_template('email/export_posts.html', user=user)
        send_email(sender=app.config['ADMINS'][0], recipients=[user.email],
                   subject='[Microblog] Your blog posts',
                   text_body=text_template,
                   html_body=html_template,
                   attachments=[('posts.json', 'application/json',
                                 json.dumps({'posts': data}, indent=4))],
                   sync=True)
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
