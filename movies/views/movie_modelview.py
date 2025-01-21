from account.models import User
from ..models import Movies
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.movie_serializer import MoviesModelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..custom_pagination import CustomPagination
from django.shortcuts import get_object_or_404, get_list_or_404
from http import HTTPMethod
from rest_framework.views import APIView
from ..serializers.movie_list_serializer import MovieSerializer_list, MovieListSerializer



class MovieModelViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Movies.objects.all()
    serializer_class = MoviesModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    # pagination_class = []
    # filter_backends = []
    # renderer_classes = []
    # parser_classes = []
    # authentication_classes = []
    # throttle_classes = ""
    """
    lookup_field is a Django Rest Framework (DRF) attribute used to specify the model field that should be used to uniquely 
    identify an object when constructing or resolving URLs for API endpoints. By default, DRF uses the pk (primary key) field 
    of a model as the identifier.
    """
    # lookup_field = 'pk'
           ## OR
    # lookup_field = 'title'


    def list(self, request):
        queryset = self.get_queryset().order_by('title')
        # paginator = CustomPagination()
        # paginated_queryset = paginator.paginate_queryset(queryset, request)
        # serializer = MoviesModelSerializer(paginated_queryset, many=True)
        # return paginator.get_paginated_response(serializer.data)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = MoviesModelSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


    def retrieve(self, request, pk=None):
        # queryset = Movies.objects.all()
        # movie_obj = get_object_or_404(queryset, pk=pk)
        movie_obj = get_object_or_404(Movies, pk=pk)
        serializer = MoviesModelSerializer(movie_obj)
        return Response(serializer.data, status= status.HTTP_200_OK)


    def create(self, request):
        serializer = MoviesModelSerializer(data = request.data)

        # # .save() will create a new instance.
        # serializer = MoviesModelSerializer(data=request.data)

        if serializer.is_valid():
            new_instance = serializer.save()
            # new_instance.partners.add(serializer.validated_data['partners'])
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        movie_obj = get_object_or_404(Movies, pk=pk)

        # # .save() will update the existing `comment` instance.
        # serializer = MoviesModelSerializer(movie_obj, data=request.data)
        serializer = MoviesModelSerializer(movie_obj, data = request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

    def partial_update(self, request, pk=None):
        movie_obj = get_object_or_404(Movies, pk=pk)
        serializer = MoviesModelSerializer(movie_obj, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        movie_obj = get_object_or_404(Movies, id=pk)
        # movie_obj.delete()
        # print(movie_obj)
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
    
    """
    detail = False
    Use this when the action applies to the entire collection or is independent of any specific object.
    """
    @action(detail= False, methods=['get'], url_path='my-detail')
    def get_the_req_user_detail(self, request):
        # print("usr => ", request.user)
        if request.user.is_admin:
            return Response({'msg': 'Testing ok.'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': "You don't have testing permission"},
                            status=status.HTTP_400_BAD_REQUEST)



    """
    detail = True
    Use this when the action operates on a single object. The endpoint will include a primary key (pk) in the URL.
    """
    # @action(detail= True, methods=['put', 'patch'])
    @action(detail= True, methods=[HTTPMethod.PUT, HTTPMethod.PATCH], permission_classes=[IsAdminUser],
            name= "no_name")   ## url_path='update-movie'
    def update_data_using_action(self, request, pk=None):
        # pk_object = self.get_object()            # `get_object()` retrieves the queryset object using pk
        movie_obj = get_object_or_404(Movies, pk=pk)
        serializer = self.get_serializer(movie_obj, data=request.data, partial= True if request.method == "PATCH" else False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # # Perform the lookup filtering.
        # print(self.lookup_url_kwarg)
        # print(self.lookup_field)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = get_object_or_404(queryset, **filter_kwargs)
        print("obj => ", obj)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj




class MoviesApiViews(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if not pk:
            queryset = Movies.objects.all()
            serializer = MovieSerializer_list(queryset, many=True)
        else:
            queryset = get_object_or_404(Movies, id=pk)
            serializer = MovieSerializer_list(queryset)
        return Response({"data":serializer.data}, status= status.HTTP_200_OK)


    def post(self, request):
        serializer = MovieSerializer_list(data = request.data, many=True)
        if serializer.is_valid():
            print('ok')
            new_instance = serializer.save()
            return Response({"data":serializer.data}, status= status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status= status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        try:
            requested_data = sorted(request.data, key=lambda item: item['id'])
            movie_ids = [i['id'] for i in requested_data]
        except KeyError:
            return Response({"error": "ID not available in data."}, status=status.HTTP_400_BAD_REQUEST)
        movie_obj = Movies.objects.filter(id__in=movie_ids).order_by('id')
        # movie_obj = get_list_or_404(Movies, id__in=movie_ids)
        
        if len(movie_obj) != len(movie_ids):
            return Response({"error": "Some movie IDs do not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer_list(movie_obj, data=requested_data, many=True)
        # serializer = MovieSerializer_list(movie_obj[0], data=requested_data[0])
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    def patch(self, request, pk=None):
        # Handle patching multiple movies (if pk is None) or a single movie
        if pk is None:
            return self.put(request)  # You can choose to handle bulk updates here

        movie_obj = get_object_or_404(Movies, pk=pk)
        
        serializer = MovieSerializer_list(movie_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_206_PARTIAL_CONTENT)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None):
        movie_obj = get_object_or_404(Movies, id=pk)
        # movie_obj.delete()
        # print(movie_obj)
        return Response({'msg':'Data deleted....'}, status= status.HTTP_400_BAD_REQUEST)


