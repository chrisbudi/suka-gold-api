from rest_framework.decorators import api_view
from core.information.serializers import (
    InformationEducationalSerializer as infoSerializer,
    InformationEducationalServiceFilter as educationFilter
    )
from rest_framework import status, viewsets, filters, pagination, response
from core.models import information_educational as modelInfo
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
# from rest_framework.pagination import LimitOffsetPagination

class InformationEducationViewSet(viewsets.ModelViewSet):
    queryset = modelInfo.objects.all()
    serializer_class = infoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class  = educationFilter
    search_fields = ['information_name',]
    pagination_class = pagination.LimitOffsetPagination  # Adjust pagination class as needed


    def list(self, request):
        queryset = modelInfo.objects.all()
        filter_queryset = self.filter_queryset(queryset)
        paginated_queryset = self.paginate_queryset(filter_queryset)
        serializer = infoSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
    def get(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = infoSerializer(info)
        return response.Response(serializer.data)

    def create(self, request):
        serializer = infoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        serializer = infoSerializer(info, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        queryset = modelInfo.objects.all()
        info = get_object_or_404(queryset, pk=pk)
        info.delete()
        return response.Response({
            'message': 'Information Educational deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)
                        
# class GetApiView(ListAPIView):
#     def get(self, request):
#         # try:
#         serializer_class = infoSerializer
#         queryset = modelInfo.objects.all()
            # return Response(serializer.data, status=status.HTTP_200_OK)
        
        # except info.DoesNotExist:
        #     return Response("Information Educational does not exist", status=status.HTTP_404_NOT_FOUND)
    
# class EducationalAPIView(APIView):
#     @api_view(['POST'])
#     def post_educational(request):
#         serializer = infoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
# class EducationalAPIView(APIView):
#     @api_view(['PATCH'])
#     def patch_educational(request, id):
#         try:
#             info = modelInfo.objects.get(pk=id)
            
#         except info.DoesNotExist:
#             return Response({'error': 'Information Educational not found'}, status=status.HTTP_404_NOT_FOUND)
    
#         serializer = infoSerializer(info, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
            
#             return Response(serializer.data)
        
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     class EducationalAPIView(APIView):
#         @api_view(['DELETE'])
#         def delete_educational(request, id):
#             try:
#                 info = modelInfo.objects.get(pk=id)
#                 info.delete()
#                 return Response({
#                     'message': 'Information Educational deleted successfully',
#                     }, status=status.HTTP_204_NO_CONTENT)
            
#             except info.DoesNotExist:
#                 return Response({
#                     "error": "Information Educational not found"
#                 }, status=status.HTTP_404_NOT_FOUND)