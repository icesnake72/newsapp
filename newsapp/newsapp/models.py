# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Articles(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    url_to_image = models.CharField(max_length=2000, blank=True, null=True)
    published_at = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    category = models.ForeignKey('Category', models.DO_NOTHING, db_column='category')
    source = models.ForeignKey('Sources', models.DO_NOTHING, db_column='source')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'articles'


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    memo = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'category'


class Sources(models.Model):
    id = models.BigAutoField(primary_key=True)
    source_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(unique=True, max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sources'
