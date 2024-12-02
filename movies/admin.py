from django.contrib import admin
from .models import ProductionHouse, MovieIndustry, Movies


@admin.register(Movies)
class MoviesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_production_name', 'display_industry_name', 'display_actors','display_director_name',
                    'display_producer_name','bugget', 'total_collection', 'release_date']

    def display_production_name(self, obj):
        return obj.production.pr_name

    def display_industry_name(self, obj):
        return obj.industry.industry_name

    def display_director_name(self, obj):
        return obj.director.famous_name

    def display_producer_name(self, obj):
        return obj.producer.famous_name

    def display_actors(self, obj):
        # Display partners as a comma-separated string
        return ", ".join([act.famous_name for act in obj.actors.all()])

    display_actors.short_description = "All Actors"  # Label for the column


@admin.register(ProductionHouse)
class ProductionHouseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'pr_name', 'display_owner_name', 'display_partners', 'display_industry_name','start_date',]
    empty_value_display = "-empty-"

    def display_industry_name(self, obj):
        return obj.industry.industry_name

    def display_owner_name(self, obj):
        return obj.owner.name

    def display_partners(self, obj):
        # Display partners as a comma-separated string
        return ", ".join([partner.name for partner in obj.partners.all()])

    display_partners.short_description = "Partners"  # Label for the column



@admin.register(MovieIndustry)
class MovieIndustryModelAdmin(admin.ModelAdmin):
    list_display = tuple(field.name for field in MovieIndustry._meta.fields)