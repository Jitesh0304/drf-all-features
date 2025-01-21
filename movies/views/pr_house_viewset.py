from account.models import User
from ..models import ProductionHouse
from ..serializers.pr_house_serializers import ProductionHouseModelSerializer, DummyProductionHouseModelSerializer
from ..serializers.pr_house_hyperlink import ProductionHouseHypelinkedSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import pagination
from ..custom_pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import transaction




class ProductionHouseViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = [IsAuthenticated]

    # renderer_classes = []
    # parser_classes = []
    # authentication_classes = []
    # throttle_classes = ""


    # def list(self, request):
    #     queryset = ProductionHouse.objects.all()
    #     serializer = ProductionHouseModelSerializer(queryset, many=True)
    #     return Response(serializer.data, status= status.HTTP_200_OK)


    def list(self, request):
        queryset = ProductionHouse.objects.all().order_by('pr_name')
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        # serializer_response = ProductionHouseModelSerializer(paginated_queryset, many=True)
        serializer = self.get_serializer_class()
        serializer_response = serializer(paginated_queryset, many=True, context = {'request':request})
        return paginator.get_paginated_response(serializer_response.data)


    def retrieve(self, request, pk=None):
        # queryset = ProductionHouse.objects.all()
        # pr_house = get_object_or_404(queryset, pk=pk)
        pr_house = get_object_or_404(ProductionHouse, pk=pk)
        serializer = ProductionHouseModelSerializer(pr_house)
        return Response(serializer.data, status= status.HTTP_200_OK)


    # def create(self, request):
    #     serializer = ProductionHouseModelSerializer(data = request.data)
    #     if serializer.is_valid():
    #         new_instance = serializer.save()
    #         # new_instance.partners.add(serializer.validated_data['partners'])
    #         return Response(serializer.data, status= status.HTTP_201_CREATED)
    #     return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def create(self, request):
        serializer = DummyProductionHouseModelSerializer(data = request.data)
        if serializer.is_valid():
            new_instance = serializer.save()
            # new_instance.partners.add(serializer.validated_data['partners'])
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        pr_house = get_object_or_404(ProductionHouse, pk=pk)
        serializer = ProductionHouseModelSerializer(pr_house, data = request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    

    # def partial_update(self, request, pk=None):
    #     pr_house = get_object_or_404(ProductionHouse, pk=pk)
    #     serializer = ProductionHouseModelSerializer(pr_house, data = request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status= status.HTTP_206_PARTIAL_CONTENT)
    #     return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pr_house = get_object_or_404(ProductionHouse, pk=pk)
        # pr_house.owner = User.objects.get(id=pr_house.owner.id)
        serializer = DummyProductionHouseModelSerializer(pr_house, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_206_PARTIAL_CONTENT)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        pr_house = get_object_or_404(ProductionHouse, id=pk)
        # pr_house.delete()
        # print(pr_house)
        return Response({'msg':'Data deleted....'}, status= status.HTTP_400_BAD_REQUEST)


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            # print(self.action)
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        if self.request.user.is_admin:
            return ProductionHouseModelSerializer
        return DummyProductionHouseModelSerializer
    



class ProductionHouseHyperlinkedViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if not pk:
            queryset = ProductionHouse.objects.all()
            serializer = ProductionHouseHypelinkedSerializer(queryset, many=True, context = {'request':request})
        else:
            queryset = get_object_or_404(ProductionHouse, id=pk)
            serializer = ProductionHouseHypelinkedSerializer(queryset, context = {'request':request})
        return Response(serializer.data, status= status.HTTP_200_OK)


    def post(self, request):
        serializer = ProductionHouseHypelinkedSerializer(data = request.data)
        if serializer.is_valid():
            new_instance = serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        pr_house = get_object_or_404(ProductionHouse, pk=pk)
        serializer = ProductionHouseHypelinkedSerializer(pr_house, data = request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request, pk=None):
        pr_house = get_object_or_404(ProductionHouse, pk=pk)
        serializer = ProductionHouseHypelinkedSerializer(pr_house, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_206_PARTIAL_CONTENT)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk=None):
        pr_house = get_object_or_404(ProductionHouse, id=pk)
        pr_house.delete()
        return Response({'msg':'Data deleted....'}, status= status.HTTP_400_BAD_REQUEST)



