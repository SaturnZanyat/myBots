import random

from django.shortcuts import render
from requests import Response
from rest_framework import serializers

from . import models

class QuestSerializator(serializers.ModelSerializer):
    class Meta:
        model = models.question
        fields = ["pk", "quest", "answer"]
