from django.contrib import admin
from .models import Actor, Produrer, Director

@admin.register(Actor)
class ActorModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'famous_name', 'income', 'career_start', 'career_end', 'total_movies')


@admin.register(Produrer)
class ProducerModelAdmin(admin.ModelAdmin):
    # list_display = ['id', 'user', 'famous_name', 'income', 'career_start','career_end','total_movies']
    # list_display = ['id', 'display_user_name', 'famous_name', 'income', 'career_start','career_end','total_movies']
    list_display = ['id', 'display_user_name', 'famous_name', 'income', 'career_start','career_end','total_movies', 'combined_name']
    empty_value_display = "-empty-"
    # fields = ['famous_name']
    # fields = [("income", "famous_name"), "career_start"]
    list_display_links = ["famous_name",]
    list_select_related = ["user",]

    fieldsets = [
        (
            None,
            {
                "fields": ["famous_name", "income", "user", ],
            },
        ),
        (
            "Advanced options",
            {
                # "classes": ["collapse"],
                "classes": ["wide", "collapse"],
                "fields": ["career_start", "total_movies"],
            },
        ),
    ]

    # @admin.display(empty_value="???", description="Name")
    # def display_user_name(self, obj):
    #     return obj.user.name

    # def display_user_name(self, obj):
    #     return obj.user.name



@admin.register(Director)
class DirectorModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'famous_name', 'income', 'career_start','career_end','total_movies']




class ActorAdminSite(admin.AdminSite):
    site_header = "Actor Administration"
    site_title = "Actor Admin"
    index_title = "Actor Database"

    def has_permission(self, request):
        return request.user.is_active #and request.user.groups.filter(name="Actor Group").exists()
actor_site = ActorAdminSite(name= "ActorAdmin")
actor_site.register(Actor, ActorModelAdmin)



class DirectorAdminSite(admin.AdminSite):
    site_header = "Director Administration"
    site_title = "Director Admin"
    index_title = "Director Database"

    def has_permission(self, request):
        # return request.user.is_active and request.user.groups.filter(name="Director Group").exists()
        return request.user.is_active and request.user.is_admin
director_site = DirectorAdminSite(name= "DirectorAdmin")
director_site.register(Director, DirectorModelAdmin)


class ProducerAdminSite(admin.AdminSite):
    site_header = "Producer Administration"
    site_title = "Producer Admin"
    index_title = "Producer Database"

    def has_permission(self, request):
        # return request.user.is_active and request.user.groups.filter(name="Producer Group").exists()
        return request.user.is_active and not request.user.is_admin
producer_site = ProducerAdminSite(name= "ProducerAdmin")
producer_site.register(Produrer, ProducerModelAdmin)
