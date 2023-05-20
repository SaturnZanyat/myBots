import random

from rest_framework.response import Response
from rest_framework.views import APIView
from appDjango.postgresTest.testdb.serializers import QuestSerializator
from . import models

class RandomQuest(APIView):
    def get(self, *args, **kwargs):
        all_quest = models.question.objects.all()
        random_quest = random.choice(all_quest)
        serialized_random_quest = QuestSerializator(random_quest, many=False)
        return Response(serialized_random_quest.data)
