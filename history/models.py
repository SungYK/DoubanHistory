from django.db import models

class Subject(models.Model):
    title = models.CharField(max_length=70)
    original_title = models.CharField(max_length=70)
    sub_id = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    history_rating = models.CharField(max_length=1000)
    playing = models.IntegerField()
    pub_date = models.DateTimeField()
    created_date = models.DateTimeField()
    update_date = models.DateTimeField()
    daily_rank = models.IntegerField()
    poster = models.CharField(max_length=200)