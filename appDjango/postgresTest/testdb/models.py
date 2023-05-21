from django.db import models

class question(models.Model):
    quest = models.CharField(verbose_name="Вопрос", max_length=250)
    answer = models.CharField(verbose_name="Ответ", max_length=50)

    def str(self):
        return self.title

