import unittest
from app.models import Comment,Blog, User
from app import db

class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_blog = Blog(title= 'BLM', blog= 'Our Dear Lives Matter')
        self.new_comment= Comment(comment='Good one',blog= self.new_blog)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Good one')
        self.assertEquals(self.new_comment.blog, self.new_blog)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_blog_id(self):
        self.new_comment.save_comment()
        got_comments = Comment.get_comments(self.new_blog.id)
        self.assertTrue(len(got_comments)==1)

    
    
    
