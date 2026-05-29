from pathlib import Path

from django.conf import settings
from django.test import Client, SimpleTestCase
from django.urls import reverse


class FrontendPagesTests(SimpleTestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_home_redirects_to_login(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    def test_login_page_renders_uco_prototype_shell(self) -> None:
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login-card")
        self.assertContains(response, "Sistema de Servicios Docentes")
        self.assertContains(response, reverse("token_obtain_pair"))

    def test_dashboard_page_renders_calendar_and_reservation_form(self) -> None:
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sidebar")
        self.assertContains(response, "Sistema Servicios Docentes")
        self.assertContains(response, 'data-dashboard-panel="calendar"')
        self.assertContains(response, "Informacion de la reserva")

    def test_frontend_static_assets_exist(self) -> None:
        static_dir = Path(settings.BASE_DIR) / "frontend" / "static"

        self.assertTrue((static_dir / "css" / "tailwind.css").is_file())
        self.assertTrue((static_dir / "js" / "frontend-ui.js").is_file())
        self.assertTrue((static_dir / "js" / "ws-notifications.js").is_file())
        self.assertTrue((static_dir / "images" / "logo-uco.png").is_file())
