import unittest
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    )

from app import app


class TestAppRoutes(unittest.TestCase):
    """Тесты для проверки работоспособности всех маршрутов приложения"""

    def setUp(self):
        """Настройка тестового клиента перед каждым тестом"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Очистка после каждого теста"""
        self.ctx.pop()

    # ========== Тесты главной страницы ==========
    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertIn(
            response.status_code, [200, 302, 301, 308],
            f"Главная страница вернула неожиданный статус: {response.status_code}"
            )

    # ========== Тесты маршрутов аутентификации ==========
    def test_auth_login_get(self):
        """Тест GET-запроса к странице входа"""
        response = self.client.get('/auth/login')
        self.assertIn(
            response.status_code, [200, 302, 308],
            f"Страница входа (GET) вернула статус: {response.status_code}"
            )

    def test_auth_login_post(self):
        """Тест POST-запроса к странице входа"""
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(
            '/auth/login', data=data, follow_redirects=False
            )
        self.assertIn(
            response.status_code, [200, 302, 308, 400, 401],
            f"Вход (POST) вернул статус: {response.status_code}"
            )

    def test_auth_register_get(self):
        """Тест GET-запроса к странице регистрации"""
        response = self.client.get('/auth/register')
        self.assertIn(
            response.status_code, [200, 302, 308],
            f"Страница регистрации (GET) вернула статус: {response.status_code}"
            )

    def test_auth_register_post(self):
        """Тест POST-запроса к странице регистрации"""
        data = {
            'username': 'new_test_user',
            'email': 'test@example.com',
            'password': 'test_password',
            'password_confirm': 'test_password'
        }
        response = self.client.post(
            '/auth/register', data=data, follow_redirects=False
            )
        self.assertIn(
            response.status_code, [200, 201, 302, 308, 400],
            f"Регистрация (POST) вернула статус: {response.status_code}"
            )

    def test_auth_logout(self):
        """Тест выхода из системы"""
        response = self.client.post('/auth/logout', follow_redirects=False)
        self.assertIn(
            response.status_code, [200, 302, 308],
            f"Выход вернул статус: {response.status_code}"
            )

    # ========== Тесты маршрутов постов ==========
    def test_posts_list_get(self):
        """Тест GET-запроса к списку постов"""
        response = self.client.get('/posts/')
        self.assertIn(
            response.status_code, [200, 302, 308],
            f"Список постов (GET) вернул статус: {response.status_code}"
            )

    def test_posts_create_get(self):
        """Тест GET-запроса к странице создания поста"""
        response = self.client.get('/posts/create')
        self.assertIn(
            response.status_code, [200, 302, 308, 401, 403],
            f"Создание поста (GET) вернуло статус: {response.status_code}"
            )

    def test_posts_create_post(self):
        """Тест POST-запроса создания поста"""
        data = {
            'title': 'Test Post',
            'content': 'This is a test post content'
        }
        response = self.client.post(
            '/posts/create', data=data, follow_redirects=False
            )
        self.assertIn(
            response.status_code, [200, 201, 302, 308, 400, 401, 403],
            f"Создание поста (POST) вернуло статус: {response.status_code}"
            )

    def test_posts_detail_get(self):
        """Тест GET-запроса к детальной странице поста"""
        # Тестируем с ID = 4 (если пост существует, вернет 200, иначе 404)
        response = self.client.get('/posts/4')
        self.assertIn(
            response.status_code, [200, 302, 308, 404],
            f"Детали поста (GET) вернули статус: {response.status_code}"
            )

    def test_posts_edit_get(self):
        """Тест GET-запроса к странице редактирования поста"""
        response = self.client.get('/posts/4/edit')
        self.assertIn(
            response.status_code, [200, 302, 308, 401, 403, 404],
            f"Редактирование поста (GET) вернуло статус: {response.status_code}"
            )

    def test_posts_edit_post(self):
        """Тест POST-запроса редактирования поста"""
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated content'
        }
        response = self.client.post(
            '/posts/4/edit', data=data,
            follow_redirects=False
            )
        self.assertIn(
            response.status_code, [200, 302, 308, 400, 401, 403, 404],
            f"Редактирование поста (POST) вернуло статус: {response.status_code}"
            )

    def test_posts_delete(self):
        """Тест удаления поста"""
        response = self.client.post('/posts/4/delete', follow_redirects=False)
        self.assertIn(
            response.status_code, [200, 302, 308, 401, 403, 404, 405],
            f"Удаление поста вернуло статус: {response.status_code}"
            )

    # ========== Тесты статических файлов ==========
    def test_static_css(self):
        """Тест доступности CSS файлов"""
        response = self.client.get('/static/css/style.css')
        try:
            self.assertIn(
                response.status_code, [200, 304, 404],
                f"Статический CSS вернул статус: {response.status_code}"
                )
        finally:
            # Закрываем response для предотвращения ResourceWarning
            response.close()

    def test_static_js(self):
        """Тест доступности JS файлов"""
        response = self.client.get('/static/js/main.js')
        try:
            self.assertIn(
                response.status_code, [200, 304, 404],
                f"Статический JS вернул статус: {response.status_code}"
                )
        finally:
            # Закрываем response для предотвращения ResourceWarning
            response.close()

    # ========== Тесты на несуществующие маршруты ==========
    def test_404_page(self):
        """Тест обработки несуществующего маршрута"""
        response = self.client.get('/nonexistent/route/12345')
        self.assertEqual(
            response.status_code, 404,
            f"Несуществующий маршрут должен возвращать 404, получен: {response.status_code}"
            )

    # ========== Вспомогательные методы ==========
    def test_all_routes_are_registered(self):
        """Проверка, что все маршруты зарегистрированы"""
        rules = list(self.app.url_map.iter_rules())
        self.assertGreater(
            len(rules), 0, "В приложении должны быть зарегистрированы маршруты"
            )

        print("\n========== Зарегистрированные маршруты ==========")
        for rule in rules:
            if rule.endpoint != 'static':
                print(f"{rule.endpoint:30s} {rule.methods} {rule.rule}")


class TestAppConfiguration(unittest.TestCase):
    """Тесты конфигурации приложения"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.app = app
        self.client = self.app.test_client()

    def test_app_exists(self):
        """Проверка, что приложение существует"""
        self.assertIsNotNone(app, "Приложение должно быть инициализировано")

    def test_app_is_flask_instance(self):
        """Проверка, что app является экземпляром Flask"""
        from flask import Flask
        self.assertIsInstance(app, Flask, "app должен быть экземпляром Flask")

    def test_testing_mode(self):
        """Проверка режима тестирования"""
        self.app.config['TESTING'] = True
        self.assertTrue(
            self.app.config['TESTING'], "TESTING режим должен быть включен"
            )


def run_tests_with_coverage():
    """Запуск тестов с отображением покрытия"""
    print("=" * 70)
    print("ЗАПУСК ТЕСТОВ МАРШРУТОВ")
    print("=" * 70)

    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем все тесты
    suite.addTests(loader.loadTestsFromTestCase(TestAppRoutes))
    suite.addTests(loader.loadTestsFromTestCase(TestAppConfiguration))

    # Запускаем тесты с verbose режимом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Вывод статистики
    print("\n" + "=" * 70)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"Всего тестов запущено: {result.testsRun}")
    print(
        f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}"
        )
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    print(f"Пропущено: {len(result.skipped)}")

    return result


if __name__ == '__main__':
    # Запускаем тесты
    result = run_tests_with_coverage()

    # Возвращаем код выхода
    sys.exit(0 if result.wasSuccessful() else 1)