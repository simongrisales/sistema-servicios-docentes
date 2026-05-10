def test_configuracion_base_importa_correctamente():
    import config.settings.base as settings

    assert settings.ROOT_URLCONF == "config.urls"
    assert "apps.asignacion" in settings.INSTALLED_APPS
