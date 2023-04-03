from django.conf import settings
from django.db import models
from django.utils import timezone

# チームテーブル
class Team(models.Model):
    # チーム名カラム
    name = models.CharField(max_length=50)
    def publish(self):
        self.save()
    def __str__(self):
        return self.name

# ユーザーテーブル
class User(models.Model):
    # チームテーブルと紐づけるためのカラム
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    # ユーザー名カラム
    name = models.CharField(max_length=50)
