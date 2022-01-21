from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import UserRegisterSerializer, PlaylistSerializer, PartySerializer, TrackSerializer, UserSerializer
from api.models import Playlist, Party, Track


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

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetailView(APIView):
    """Редактирование плейлиста"""

    def get_object(self, pk):
        try:
            return Playlist.objects.filter(pk=pk)
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


class SearchTrackView(APIView):
    """Поиск трека"""
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]


class TrackAddView(CreateAPIView):
    """Добавление трека"""
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
