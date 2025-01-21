from .views.industry_generic_views import MovieIndustryListCreateView, MovieIndustryUpdateDeleteView, MovieIndustryAPIView
from .views.pr_house_viewset import ProductionHouseViewSet, ProductionHouseHyperlinkedViewSet
from django.urls import path
from .models import MovieIndustry
from .serializers.industry_serializers import MovieIndustryModelSerializer
from .views.movie_modelview import MovieModelViewSet, MoviesApiViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'mv', MovieModelViewSet, basename='movie')


prod_list = ProductionHouseViewSet.as_view({'get': 'list'})
prod_detail = ProductionHouseViewSet.as_view({'get': 'retrieve', 'post':'create', 'put':'update', 'patch':'partial_update',
                                              'delete': 'destroy'})

urlpatterns = [
    path('industry/', MovieIndustryListCreateView.as_view(queryset=MovieIndustry.objects.all(), 
                                                 serializer_class=MovieIndustryModelSerializer), name='industry-list'),
    path('industry-update-delete/<int:pk>/', MovieIndustryUpdateDeleteView.as_view(queryset=MovieIndustry.objects.all(), 
                                                 serializer_class=MovieIndustryModelSerializer), name='industry-get-update-delete'),
    path('movie-industries/<int:pk>/', MovieIndustryAPIView.as_view(), name='movieindustry-detail'),
    path('movie-industries/', MovieIndustryAPIView.as_view(), name='movieindustry-api'),
    path('prod-house-list/', prod_list, name='production_list'),
    path('prod-house/', prod_detail, name='production_retrieve'),
    path('prod-house/<int:pk>/', prod_detail, name='production_crud'),
    path('prod-house-hyperlink/', ProductionHouseHyperlinkedViewSet.as_view(), name='productionhouse-list'),
    path('prod-house-hyperlink/<int:pk>/', ProductionHouseHyperlinkedViewSet.as_view(), name='productionhouse-detail'),
    path('movies/', MoviesApiViews.as_view(), name='movie-detail'),
    path('movies/<int:pk>/', MoviesApiViews.as_view(), name='movie-details'),
]+ router.urls



