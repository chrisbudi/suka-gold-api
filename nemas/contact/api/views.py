from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from contact.api.serializers import ContactRequestSerializer
from contact.application.commands.submit_contact_request import (
    SubmitContactRequestCommand,
    SubmitContactRequestHandler,
)
from contact.application.commands.list_contact_queries import (
    ListContactRequestsQuery,
    ListContactRequestsHandler,
)
from contact.application.services.contact_service import ContactService
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import pagination
from contact.infrastucture.repositories.django_contact_repository import (
    DjangoContactRequestRepository,
)


class ContactUsView(APIView):

    @extend_schema(
        request=ContactRequestSerializer,
    )
    def post(self, request):
        serializer = ContactRequestSerializer(data=request.data)
        if serializer.is_valid():
            command = SubmitContactRequestCommand(**serializer.validated_data)
            repo = DjangoContactRequestRepository()
            service = ContactService(repo)
            handler = SubmitContactRequestHandler(service)
            handler.handle(command)
            return Response(
                {"message": "Contact request submitted"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        methods=["GET"],
        summary="List contact requests",
        parameters=[
            OpenApiParameter(
                name="limit", type=int, location=OpenApiParameter.QUERY, required=False
            ),
            OpenApiParameter(
                name="offset", type=int, location=OpenApiParameter.QUERY, required=False
            ),
        ],
        responses=ContactRequestSerializer(many=True),
    )
    def get(self, request):
        repo = DjangoContactRequestRepository()
        handler = ListContactRequestsHandler(repo)
        query = ListContactRequestsQuery()
        contact_requests = handler.handle(query)
        paginator = pagination.LimitOffsetPagination()
        page = paginator.paginate_queryset(contact_requests, request, view=self)
        serializer = ContactRequestSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
