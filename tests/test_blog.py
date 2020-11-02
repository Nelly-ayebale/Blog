import unittest
from app.models import Blog, User
from app import db


class TestBlog(unittest.TestCase):

    def setUp(self):
        self.user_James = User(username= 'James', email='ayebalenelly1606@gmail.com', bio= 'Hello I am James', profile_pic_path='app/static/photos', pass_secure= 'potato' )
        self.new_blog = Blog(user= self.user_James, title= 'BLM', blog= 'Our Dear Lives Matter')
    
    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.user, self.user_James)
        self.assertEquals(self.new_blog.title,'BLM')
        self.assertEquals(self.new_blog.blog,'Our Dear Lives Matter')
       
    
    def test_save_blog(self):
        self.new_blog.save_blogs()
        self.assertTrue(len(Blog.query.all())>0)
