from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import UserRegisterSerializer, PlaylistSerializer, PartySerializer, UserSerializer, \
    TrackSearchSerializer, TrackSerializer
from api.models import Playlist, Party, Track
from api.services import search_track
import django_filters.rest_framework


@api_view(['GET'])
def all_api_list(request):
    """ Все доступные в API адреса"""
    api_url = {
        'API_LIST': 'all/',
        'SWAGGER': 'swagger/',
        'USER_REGISTER': 'register/',
        'USERS_LIST': 'list/',
        'USER_LOGIN': 'login/',
        'USER_LOGOUT': 'logout/',
        '*': '******************',
        'PARTY_LIST': 'party/list/',
        'PARTY_CREATE': 'party/create/',
        '**': '******************',
        'PLAYLISTS': 'playlists/',
        'PLAYLIST_CREATE': 'playlist/create/',
        'PLAYLIST_UPDATE': 'playlist/update/<int:pk>/',
        'PLAYLIST_DETAIL': 'playlist/detail/<int:pk>/',
        'PLAYLIST_DELETE': 'playlist/delete/<int:pk>/',
        '***': '******************',
        'TRACK_SEARCH': 'track/search/',
        'TRACK_ADD_PLAYLIST': 'track/add/<int:pk>/',

    }
    return JsonResponse(api_url, safe=False)


class UserListView(APIView):
    """ Просмотр зарегистрированных пользователей"""

    def get(self, request, format=None):
        party = User.objects.all()
        serializer = UserSerializer(party, many=True)
        return Response(serializer.data)


class UserRegisterView(CreateAPIView):
    """ Регистрация пользователя"""

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class PartyListView(ListAPIView):
    """Список доступных мероприятий"""

    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = [IsAuthenticated]


class PartyCreateView(CreateAPIView):
    """Создание Мероприятия"""

    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = [IsAuthenticated]


class PlaylistView(ListAPIView):
    """Список доступных плейлистов"""

    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]


class PlaylistCreateView(CreateAPIView):
    """Создание плейлиста"""

    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]


class PlaylistUpdateView(APIView):
    """Редактирование плейлиста"""

    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetailView(APIView):
    """Просмотр плейлиста"""

    # TODO сделать
    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet)
        return Response(serializer.data)


class PlaylistDeleteView(APIView):
    """Удаление плейлиста"""

    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistTrackView(APIView):
    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = Track.objects.filter(pk=pk)
        serializer = TrackSerializer(snippet, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        playlist_name = self.get_object(pk=pk)
        serializer = TrackSerializer(playlist_name, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchTrackView(APIView):
    """Поиск трека"""

    def get(self, request, pk, format=None):
        track_name = request.GET.get("track", "")
        result = search_track(track_name)
        serializer = TrackSearchSerializer(result, many=True)
        return Response(serializer.data)


class TrackAddView(CreateAPIView):
    """Добавление трека, с привязкой к плейлисту"""

    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]


class TrackListView(ListAPIView):
    """Просмотр всех треков"""

    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]


class SearchAllTracksPlaylistView(APIView):
    """Поиск трека по плейлисту"""

    def get(self, request, pk, format=None):
        party = Track.objects.filter(playlist_name=pk)
        serializer = TrackSerializer(party, many=True)
        return Response(serializer.data)


class LikeTrack(APIView):
    """Like track"""

    def post(self, request, pk):
        serializer = Track.objects.get(pk)
        serializer.track_rate = 1
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=400)
