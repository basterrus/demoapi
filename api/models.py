import pytz
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()


class Party(models.Model):
    party_name = models.CharField(max_length=50, verbose_name='Название мероприятия')


class Playlist(models.Model):
    party_name = models.ForeignKey(Party, verbose_name='Название мероприятия', on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=50, verbose_name='Название плейлиста')
    max_count_track = models.IntegerField(verbose_name='Максимальное количество записей')
    start_time = models.DateField(auto_now=True, verbose_name='Время открытия')
    time_expired = models.DateTimeField(blank=True, null=True, verbose_name='Время закрытия')
    is_active = models.BooleanField(default=True)

    def is_time_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.time_expired + timedelta(hours=6):
            return True
        return False


class Track(models.Model):
    playlist_name = models.ForeignKey(Playlist, verbose_name='Название трека', on_delete=models.CASCADE)
    track_name = models.CharField(max_length=100, verbose_name='Название трека')
    track_url = models.URLField(verbose_name='Ссылка на трек')
    track_rate = models.IntegerField(verbose_name='Рейтинг трека')
