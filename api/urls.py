from django.urls import include, path, re_path
from rest_framework.permissions import AllowAny
from api.views import all_api_list, UserRegisterView, PlaylistCreateView, PartyCreateView, PartyListView, PlaylistView, \
    UserListView, PlaylistDeleteView, PlaylistUpdateView, PlaylistDetailView, SearchTrackView, TrackAddView, \
    TrackListView, SearchAllTracksPlaylistView, LikeTrack
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    # Common
    path('all/', all_api_list, name="api_all"),
    re_path(r'^swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='list'),
    path('', include('rest_framework.urls', namespace='rest_framework')),

    # Party
    path('party/list/', PartyListView.as_view(), name='list_party'),
    path('party/create/', PartyCreateView.as_view(), name='create_party'),

    # Playlist
    path('playlists/', PlaylistView.as_view(), name='playlists'),
    path('playlist/create/', PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/update/<int:pk>/', PlaylistUpdateView.as_view(), name='playlist_update'),
    path('playlist/detail/<int:pk>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlist/delete/<int:pk>/', PlaylistDeleteView.as_view(), name='playlist_delete'),


    path('playlist/<int:pk>/track/search/', SearchTrackView.as_view(), name='track_add'),
    path('track/add/', TrackAddView.as_view(), name='track_add'),
    path('track/list/', TrackListView.as_view(), name='track_add'),
    path('track/list/<int:pk>/', SearchAllTracksPlaylistView.as_view(), name='track_add'),
    path('track/<int:pk>/like/', LikeTrack.as_view(), name='track_add'),
]
