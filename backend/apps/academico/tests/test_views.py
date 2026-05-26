from rest_framework.test import APITestCase
import pytest
from django.urls import reverse
from ..presentation.serializers import GrupoSerializer

# Se necesita un usuario autenticado para probar endpoints, lo cual se simula con el fixture del test framework.
class AcademicoAPITest(APITestCase):

    def setUp(self):
        super().setUp()
        # Configuración de datos dummy necesarios antes de cada prueba de vista
        self.aula_data = {'nombre': 'Aula X', 'capacidad': 50, 'tipo': 'Sala de Clases'}
        self.grupo_data = {'curso_id': 1, 'docente_id': 2, 'num_estudiantes': 20}

    def test_list_aulas_disponibles(self):
        """Prueba el endpoint GET /api/academico/asignacion/ para listar aulas."""
        # Simular un objeto horario bloque
        horario = {'dia': 'Miércoles', 'hora_inicio': 10.0, 'hora_fin': 11.0}

        response = self.client.get(reverse('academico-viewset-list', kwargs={'request': self.client.request}, params=horario))

        # Asertaciones de éxito (esto dependerá mucho del mocking de la capa de servicio)
        self.assertEqual(response.status_code, 200)
        # Aquí se debería verificar que el contenido devuelto sigue el patrón AulaOutputSerializer

    def test_ejecutar_asignacion_ok(self):
        """Prueba exitosa del endpoint POST /api/academico/asignacion/ para ejecutar asignación."""
        # Datos dummy de entrada
        datos = {'group_id': 1, 'curso_id': 1, 'docente_id': 2, 'num_estudiantes': 20}
        horario = {'dia': 'Lunes', 'hora_inicio': 8.5, 'hora_fin': 9.5}

        self.client.post(reverse('academico-viewset-execute-assignment', kwargs={'request': self.client.request}),
                         datos, format='json')

        # Asertar que el status code es 200 y el mensaje de éxito está presente
        pass # El test real requeriría mocking profundo para asegurar que se llama al UseCase correcto

    def test_ejecutar_asignacion_conflicto(self):
        """Prueba cómo maneja la vista un conflicto reportado por la capa de negocio."""
        datos = {'group_id': 1, 'curso_id': 1, 'docente_id': 2, 'num_estudiantes': 20}
        horario = {'dia': 'Lunes', 'hora_inicio': 8.5, 'hora_fin': 9.5}

        # Esperar un error de Bad Request (400) que indica el conflicto
        response = self.client.post(reverse('academico-viewset-execute-assignment', kwargs={'request': self.client.request}),
                                     datos, format='json')

        self.assertEqual(response.status_code, 400)
        # Asertar que el detalle del error contiene la palabra clave de conflicto
        assert 'AulaNoDisponibleError' in response.data['detail']