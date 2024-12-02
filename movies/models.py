from django.db import models
from moviemakers.models import Produrer, Actor, Director
from account.models import User
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower



class MovieIndustry(models.Model):
    # language = {
    #     "O": "Odia",
    #     "H": "Hindi",
    # }
    language = models.CharField(max_length=20)
    industry_name = models.CharField(max_length=30, unique=True)
    country = models.CharField(max_length=30)

    class Meta:
        db_table = "movie_industry"
        ordering = ["-country"]
        # unique_together = ('language', 'country',)
        constraints = [
            # models.UniqueConstraint(fields=['language', 'country'], name='contry_language')
            models.UniqueConstraint(Lower('country'), Lower('language'), name='contry_language')
            # models.UniqueConstraint(
            #     fields=['language'],
            #     name='unique_language_case_sensitive',
            #     condition=models.Q(language__isnull=False)
            # )
        ]
        indexes = [
            models.Index(fields=["country", "language"], name="combine_idx"),
            models.Index(fields=["language"], name="lang_idx"),
        ]


    def clean(self):
        super().clean()
        if MovieIndustry.objects.filter(language__iexact = self.language, country__iexact=self.country
                                        ).exclude(pk=self.pk).exists():
            raise ValidationError("This country and language combination must be unique (case-insensitive).")

    def save(self, *args, **kwargs):
        self.full_clean()
        # print(self.language)
        super().save(*args, **kwargs)




class ProductionHouse(models.Model):

    pr_name = models.CharField(max_length=100, unique=True, db_column="name")
    owner = models.ForeignKey(User, on_delete= models.PROTECT, related_name="production_house", related_query_name="p_house")
    partners = models.ManyToManyField(User, related_name="prhouse_partner")
    industry = models.ForeignKey(MovieIndustry, on_delete=models.CASCADE, related_name="prod_house")
    start_date = models.DateField()

    class Meta:
        db_table = "production_house"



class Movies(models.Model):

    title = models.CharField(max_length=100, unique=True)
    production = models.ForeignKey(ProductionHouse, on_delete= models.PROTECT, related_name="movie_prod")
    industry = models.ForeignKey(MovieIndustry, on_delete= models.PROTECT, related_name="movie_industry")
    actors = models.ManyToManyField(Actor, related_name="movie_act")
    director = models.ForeignKey(Director,on_delete= models.PROTECT, related_name="movie_dir")
    producer = models.ForeignKey(Produrer, on_delete= models.PROTECT, related_name="movie_producer")
    bugget = models.BigIntegerField()
    total_collection = models.BigIntegerField(null= True, blank=True)
    release_date = models.DateField()

    class Meta:
        db_table = "movies"

