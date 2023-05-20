import random

from rest_framework.response import Response
from rest_framework.views import APIView
from .serial import QuestSerializator
from . import models
from django.http import Http404

class RandomQuest(APIView):
    def get(self, *args, **kwargs):
        all_quest = models.question.objects.all()
        random_quest = random.choice(all_quest)
        serialized_random_quest = QuestSerializator(random_quest, many=False)
        return Response(serialized_random_quest.data)

class NextQuest(APIView):
    def get(self, request, pk, format=None):
        quest = models.question.objects.filter(pk__gt=pk).first()
        if not quest:
            return Http404()
        serialized_next_quest = QuestSerializator(quest, many=False)
        return Response(serialized_next_quest.data)