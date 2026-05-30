from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..application.dtos import CrearNotificacionInputDTO, MarcarLeidaInputDTO
from ..application.use_cases import NotificacionService
from .serializers import (
    CrearNotificacionSerializer,
    MarcarLeidaSerializer,
    NotificacionOutputSerializer,
)


class NotificacionesViewSet(viewsets.ViewSet):
    """Endpoints REST para gestionar notificaciones in-app."""

    permission_classes = [IsAuthenticated]

    def get_service(self) -> NotificacionService:
        from ..infrastructure.repositories import NotificacionRepository

        return NotificacionService(repo=NotificacionRepository())

    def list(self, request):
        unread_only = request.query_params.get("unread") == "true"
        service = self.get_service()
        user_id = str(request.user.pk)

        if unread_only:
            notifications = service.listar_notificaciones_no_leidas(user_id)
        else:
            notifications = service.listar_notificaciones(user_id)

        serializer = NotificacionOutputSerializer(notifications, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CrearNotificacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_dto = CrearNotificacionInputDTO(**serializer.validated_data)
        output = self.get_service().enviar_notificacion(input_dto)
        output_serializer = NotificacionOutputSerializer(output)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="marcar-leida")
    def marcar_leida(self, request, pk=None):
        serializer = MarcarLeidaSerializer(data={"notificacion_id": pk})
        serializer.is_valid(raise_exception=True)

        input_dto = MarcarLeidaInputDTO(
            notificacion_id=serializer.validated_data["notificacion_id"],
            user_id=str(request.user.pk),
        )
        was_updated = self.get_service().marcar_leida(input_dto)
        if not was_updated:
            return Response(
                {"detail": "Notificacion no encontrada o ya estaba leida."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="no-leidas")
    def no_leidas(self, request):
        notifications = self.get_service().listar_notificaciones_no_leidas(
            str(request.user.pk)
        )
        serializer = NotificacionOutputSerializer(notifications, many=True)
        return Response(serializer.data)


def campana_notificaciones(request):
    """Fragmento HTMX para renderizar la campana de notificaciones."""

    notifications = []
    if request.user.is_authenticated:
        from ..infrastructure.repositories import NotificacionRepository

        service = NotificacionService(repo=NotificacionRepository())
        notifications = service.listar_notificaciones_no_leidas(str(request.user.pk))

    return render(
        request,
        "notificaciones/partials/campana.html",
        {"notificaciones": notifications, "total_no_leidas": len(notifications)},
    )
