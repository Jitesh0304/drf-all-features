from rest_framework import filters
import django_filters
from .models import MovieIndustry
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q



class MovieIndustryFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_class = self.get_filterset_class(view, queryset)
        if filter_class:
            filterset = filter_class(data=request.query_params, queryset=queryset, request=request)
            if filterset.is_valid():
                return filterset.qs
            # else:
            #     raise ValueError(f"Filter errors: {filterset.errors}")
        return queryset


class MovieIndustryModelFilter(django_filters.FilterSet):
    # language = django_filters.CharFilter(lookup_expr="icontains")
    # country = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = MovieIndustry
        fields = ['language', 'country']


class CountrySearchFilter(filters.SearchFilter):

    def get_search_fields(self, view, request):
        if request.query_params.get('country'):
            return ['country']
        return super().get_search_fields(view, request)

    # def filter_queryset(self, request, queryset, view):
    #     filter_backends = [filters.SearchFilter]
    #     for backend in list(filter_backends):
    #         queryset = backend().filter_queryset(request, queryset, view=self)
    #     return queryset
    
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get(self.search_param, "")  # Default is 'search'

        if not search_param:
            return queryset

        # Customize the search logic
        search_terms = search_param.split()  # Split search terms by spaces
        query = Q()
        for term in search_terms:
            query |= Q(language__icontains=term) | Q(country__icontains=term) | Q(industry_name__icontains=term)

                    ### OR
            # # Search in multiple fields with complex conditions
            # query |= (
            #     Q(language__icontains=term) |
            #     Q(country__icontains=term) |
            #     Q(industry_name__icontains=term)
            # )
        return queryset.filter(query).distinct()



class LanguageSearchFilter(filters.SearchFilter):

    def get_search_fields(self, view, request):
        if request.query_params.get('language'):
            return ['language']
        return super().get_search_fields(view, request)



class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)