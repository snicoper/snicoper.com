from blog.models import Article, Tag
from tests.unit.base_test import BaseTestCase


class BaseBlogTest(BaseTestCase):

    BaseTestCase.fixtures.append('blog')

    def setUp(self):
        super().setUp()
        self.article_model = Article
        self.tag_model = Tag
