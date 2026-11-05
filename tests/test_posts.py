
import unittest

from app import create_app
from app.extensions import db
from app.posts.models import Post


class PostCRUDTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_post(self):
        post = Post(
            title="Тестовий допис",
            content="Текст для перевірки роботи CRUD.",
            category="news",
            is_active=True,
            author="Tester"
        )

        db.session.add(post)
        db.session.commit()

        return post

    def test_create_post(self):
        response = self.client.post(
            "/post/create",
            data={
                "title": "Новий допис",
                "content": "Текст нового допису",
                "category": "news",
                "enabled": "y"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        post = db.session.execute(
            db.select(Post).where(Post.title == "Новий допис")
        ).scalar_one_or_none()

        self.assertIsNotNone(post)
        self.assertEqual(post.content, "Текст нового допису")

    def test_post_list(self):
        self.create_test_post()

        response = self.client.get("/post/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий допис".encode("utf-8"), response.data)

    def test_post_detail(self):
        post = self.create_test_post()

        response = self.client.get(f"/post/{post.id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий допис".encode("utf-8"), response.data)

    def test_update_post(self):
        post = self.create_test_post()

        response = self.client.post(
            f"/post/{post.id}/update",
            data={
                "title": "Оновлений допис",
                "content": "Оновлений текст",
                "category": "tech",
                "enabled": "y"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        updated_post = db.session.get(Post, post.id)

        self.assertEqual(updated_post.title, "Оновлений допис")
        self.assertEqual(updated_post.content, "Оновлений текст")

    def test_delete_post_page(self):
        post = self.create_test_post()

        response = self.client.get(f"/post/{post.id}/delete")

        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        post = self.create_test_post()
        post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Post, post_id))

    def test_post_not_found(self):
        response = self.client.get("/post/999999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
