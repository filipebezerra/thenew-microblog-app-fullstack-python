from config import TestConfig
import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='sophia', email='sophiabezerra.820@gmail.com')
        u.set_password('bingo')
        self.assertFalse(u.check_password('pappa'))
        self.assertTrue(u.check_password('bingo'))

    def test_avatar(self):
        u = User(username='filipe', email='filipebzerra@gmail.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         '3d42ef5511e32339960b6bcc75bda78b'
                                         '?s=128&d=retro'))

    def test_follow(self):
        sophia = User(username='sophia', email='sophiabezerra.820@gmail.com')
        filipe = User(username='filipe', email='filipebzerra@gmail.com')
        db.session.add(sophia)
        db.session.add(filipe)
        db.session.commit()
        self.assertListEqual(sophia.followed.all(), [])
        self.assertListEqual(sophia.followers.all(), [])

        sophia.follow(filipe)
        db.session.commit()
        self.assertTrue(sophia.is_following(filipe))
        self.assertEqual(sophia.followed.count(), 1)
        self.assertEqual(sophia.followed.first().username, 'filipe')
        self.assertEqual(filipe.followers.count(), 1)
        self.assertEqual(filipe.followers.first().username, 'sophia')

        sophia.unfollow(filipe)
        db.session.commit()
        self.assertFalse(sophia.is_following(filipe))
        self.assertEqual(sophia.followed.count(), 0)
        self.assertEqual(filipe.followers.count(), 0)

    def test_followed_posts(self):
        # create four us
        sophia = User(username='sophia', email='sophiabezerra.820@gmail.com')
        valentina = User(username='valentina', email='valentina@gmail.com')
        lavinia = User(username='lavinia', email='lavinia@gmail.com')
        antonella = User(username='antonella', email='antonella@gmail.com')
        db.session.add_all([sophia, valentina, lavinia, antonella])

        # create four posts
        now = datetime.utcnow()
        sophia_post = Post(body='post from sophia', author=sophia,
                           timestamp=now + timedelta(seconds=15))
        valentina_post = Post(body='post from valentina', author=valentina,
                              timestamp=now + timedelta(seconds=30))
        lavinia_post = Post(body='post from lavinia', author=lavinia,
                            timestamp=now + timedelta(seconds=45))
        antonella_post = Post(body='post from antonella', author=antonella,
                              timestamp=now + timedelta(seconds=60))
        db.session.add_all([sophia_post, valentina_post,
                            lavinia_post, antonella_post])
        db.session.commit()

        # setup the followers
        sophia.follow(valentina)
        sophia.follow(lavinia)
        valentina.follow(lavinia)
        lavinia.follow(valentina)
        db.session.commit()

        # check the followed posts of each user
        posts_sophia = sophia.followed_posts.all()
        posts_valentina = valentina.followed_posts.all()
        posts_lavinia = lavinia.followed_posts.all()
        posts_antonella = antonella.followed_posts.all()
        self.assertListEqual(
            posts_sophia, [lavinia_post, valentina_post, sophia_post])
        self.assertListEqual(posts_valentina, [lavinia_post, valentina_post])
        self.assertListEqual(posts_lavinia, [lavinia_post, valentina_post])
        self.assertListEqual(posts_antonella, [antonella_post])


if __name__ == '__main__':
    unittest.main(verbosity=2)
