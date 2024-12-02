from django.db import models
from account.models import User
from django.contrib import admin
from django.utils.html import format_html




class CommonInfo(models.Model):

    id = models.BigAutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="%(class)s_user")
    famous_name = models.CharField(max_length=50, null=True, blank=True)
    income = models.PositiveBigIntegerField()
    career_start = models.DateField()
    career_end = models.DateField(null=True, blank=True)
    total_movies = models.IntegerField(null=True, blank=True)

    class Meta:
        """
        This model will then not be used to create any database table. Instead, 
        when it is used as a base class for other models, its fields will be added to those of the child class.
        """
        abstract = True


class Actor(CommonInfo):

    class Meta(CommonInfo.Meta):
        db_table = "actor_info"


class Director(CommonInfo):

    class Meta(CommonInfo.Meta):
        db_table = "director_info"


class Produrer(CommonInfo):
    
    class Meta(CommonInfo.Meta):
        db_table = "producer_info"

    @admin.display(empty_value="???", description="Username")
    def display_user_name(self):
        return self.user.name

    @admin.display
    def combined_name(self):
        return format_html(
            '<span style="color: #{};">{} {}</span>',
            self.user.name,
            self.income,
            self.famous_name,
        )
