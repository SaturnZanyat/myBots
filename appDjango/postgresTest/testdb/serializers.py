import random

from django.shortcuts import render
from requests import Response
from rest_framework import serializers

from appDjango.postgresTest.testdb import models

class QuestSerializator(serializers.ModelSerializer):
    class Meta:
        models = models.question
        fields = ("pk", "quest", "answer")
