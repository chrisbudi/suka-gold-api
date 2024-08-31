from rest_framework.decorators import api_view
from core.information.serializers import InformationCustomerServiceSerializer as infoSerializer
from rest_framework.response import Response
from rest_framework import status
from core.models import information_customer_service as modelInfo


serializer_class = infoSerializer


@api_view(['GET'])
def fetch_customer_service(request):
    try:
        info = modelInfo.objects.all()
        serializer = infoSerializer(info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except info.DoesNotExist:
        return Response("Information Customer Service does not exist", status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def post_customer_service(request):
    serializer = infoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def patch_customer_service(request, id):
    try:
        info = modelInfo.objects.get(pk=id)
        
    except info.DoesNotExist:
        return Response({'error': 'Information Customer Service not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = infoSerializer(info, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_customer_service(request, id):
    try:
        info = modelInfo.objects.get(pk=id)
        info.delete()
        return Response({
            'message': 'Information Customer Service deleted successfully',
            }, status=status.HTTP_204_NO_CONTENT)
    
    except info.DoesNotExist:
        return Response({
            "error": "Information Customer Service not found"
        }, status=status.HTTP_404_NOT_FOUND)