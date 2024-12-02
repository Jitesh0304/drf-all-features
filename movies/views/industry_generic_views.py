from account.models import User
from ..models import MovieIndustry
from ..serializers.industry_serializers import MovieIndustryModelSerializer, DummyMovieIndustryModelSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from ..custom_filters import MovieIndustryFilter, MovieIndustryModelFilter, LanguageSearchFilter, CountrySearchFilter, \
    IsOwnerFilterBackend
from rest_framework import filters
from rest_framework import pagination
from ..custom_pagination import CustomPagination
from django.shortcuts import get_object_or_404



"""
    Custom Django filter and pagination
"""
class MovieIndustryListCreateView(generics.ListCreateAPIView):
    queryset = MovieIndustry.objects.all()
    # serializer_class = MovieIndustryModelSerializer
    # lookup_field = "id"
    permission_classes = [IsAuthenticated]
    filter_backends = [MovieIndustryFilter]
    filterset_fields = ['language', 'country']
    pagination_class = CustomPagination
    

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        return queryset


    def list(self, request):
        """
            Note the use of `get_queryset()` instead of `self.queryset`
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer_cls =self.get_serializer_class()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_cls(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = self.perform_create(serializer)
        if res != "success":
            return Response({'msg': res}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_serializer_class(self):
        if self.request.user.is_admin:
            return MovieIndustryModelSerializer
        return DummyMovieIndustryModelSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
            return "success"
        except Exception as e:
            return str(e)
        






class MovieIndustryUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieIndustryModelSerializer
    queryset = MovieIndustry.objects.all()
    # serializer_class = MovieIndustryModelSerializer
    # lookup_field = "id"
    permission_classes = [IsAuthenticated]
    filter_backends = [MovieIndustryFilter]
    filterset_fields = ['language', 'country']
    pagination_class = CustomPagination


    def retrieve(self, request, *args, **kwargs):
        # print(request)
        # print(args)
        # print(kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data= {'msg': 'Item deleted ...'}, status=status.HTTP_204_NO_CONTENT)


    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # # Perform the lookup filtering.
        # print(self.lookup_url_kwarg)
        # print(self.lookup_field)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(country__startswith = "I")
        return queryset

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return MovieIndustryModelSerializer
        return DummyMovieIndustryModelSerializer

    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()





"""
    Default Django filter and pagination
"""
# class MovieIndustryListView(generics.ListCreateAPIView):
#     queryset = MovieIndustry.objects.all()
#     # serializer_class = MovieIndustryModelSerializer
#     # lookup_field = "id"
#     permission_classes = [IsAuthenticated]
#     # filter_backends = [DjangoFilterBackend]
#     filter_backends = [MovieIndustryFilter]
#     filterset_fields = ['language', 'country']
#     pagination_class = CustomPagination


#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         return queryset


#     def list(self, request):
#         """
#             Note the use of `get_queryset()` instead of `self.queryset`
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer_cls =self.get_serializer_class()

#         page = self.paginate_queryset(queryset)

#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = serializer_cls(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         res = self.perform_create(serializer)
#         if res != "success":
#             return Response({'msg': res}, status=status.HTTP_400_BAD_REQUEST)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#     def get_serializer_class(self):
#         if self.request.user.is_admin:
#             return MovieIndustryModelSerializer
#         return DummyMovieIndustryModelSerializer

#     def perform_create(self, serializer):
#         try:
#             serializer.save()
#             return "success"
#         except Exception as e:
#             return str(e)

#     def filter_queryset(self, queryset):
#         filter_backends = [DjangoFilterBackend]
#         if 'language' in self.request.query_params:
#             print('ok')
#             filter_backends = ["other django filter"]
#         elif 'country' in self.request.query_params:
#             filter_backends = ["other django filter"]
#         for backend in list(filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset




"""
    Custom Search filter and pagination
    ^   Starts-with search.
    =   Exact matches.
    @   Full-text search. ( for Django’s PostgreSQL backend)
    $   Regex search
"""
# class MovieIndustryListView(generics.ListCreateAPIView):
#     queryset = MovieIndustry.objects.all()
#     permission_classes = [IsAuthenticated]
#     filter_backends = [CountrySearchFilter, DjangoFilterBackend]
#     filterset_fields = ['language', 'country','industry_name']
#     search_fields = ['language', 'country', 'industry_name']
#     pagination_class = CustomPagination


#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         return queryset

#     def list(self, request):
#         """
#             Note the use of `get_queryset()` instead of `self.queryset`
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         # queryset = self.get_queryset()
#         serializer_cls =self.get_serializer_class()

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = serializer_cls(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         res = self.perform_create(serializer)
#         if res != "success":
#             return Response({'msg': res}, status=status.HTTP_400_BAD_REQUEST)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def get_serializer_class(self):
#         if self.request.user.is_admin:
#             return MovieIndustryModelSerializer
#         return DummyMovieIndustryModelSerializer

#     def perform_create(self, serializer):
#         try:
#             serializer.save()
#             return "success"
#         except Exception as e:
#             return str(e)




"""
    Default Search filter and pagination
"""
# class MovieIndustryListView(generics.ListCreateAPIView):
#     queryset = MovieIndustry.objects.all()
#     permission_classes = [IsAuthenticated]
#     filter_backends = [CountrySearchFilter]
#     search_fields = ['country', 'language']
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         return queryset

#     def list(self, request):
#         """
#             Note the use of `get_queryset()` instead of `self.queryset`
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer_cls =self.get_serializer_class()

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = serializer_cls(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         res = self.perform_create(serializer)
#         if res != "success":
#             return Response({'msg': res}, status=status.HTTP_400_BAD_REQUEST)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def get_serializer_class(self):
#         if self.request.user.is_admin:
#             return MovieIndustryModelSerializer
#         return DummyMovieIndustryModelSerializer

#     def perform_create(self, serializer):
#         try:
#             serializer.save()
#             return "success"
#         except Exception as e:
#             return str(e)

#     def filter_queryset(self, queryset):
#         filter_backends = [filters.SearchFilter]
#         if 'language' in self.request.query_params:
#             print('ok')
#             filter_backends = [LanguageSearchFilter]
#         elif 'country' in self.request.query_params:
#             filter_backends = [CountrySearchFilter]
#         for backend in list(filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset



