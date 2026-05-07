from rest_framework import generics
from rest_framework.response import Response
from django.utils import timezone
from ..models import Sport, Team, CustomUser, Competition, Event, EventPhoto
from .serializers import SportSerializer, TeamSerializer, CustomUserSerializer, CompetitionSerializer, EventSerializer, EventPhotoSerializer, TeamDetailSerializer, TeamUpdateSerializer
from rest_framework.permissions import IsAuthenticated

class CompetitionAPIView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [IsAuthenticated]

class SportAPIView(generics.ListAPIView):
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    permission_classes = [IsAuthenticated]

class TeamAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

class UserAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_superuser=False, is_staff=False)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class EventAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(end_date_time__gte=timezone.now())
    
    
class CompetitorsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sport_id = self.request.query_params.get('sport_id')
        if not sport_id:
            return Team.objects.none()
        try:
            sport = Sport.objects.get(id=sport_id)
        except Sport.DoesNotExist:
            return Team.objects.none()
        if sport.sport_type == 'Single-Player':
            return CustomUser.objects.filter(is_superuser=False, is_staff=False)
        return Team.objects.filter(sport=sport)

    def get_serializer_class(self):
        sport_id = self.request.query_params.get('sport_id')
        if not sport_id:
            return TeamSerializer
        try:
            sport = Sport.objects.get(id=sport_id)
        except Sport.DoesNotExist:
            return TeamSerializer
        if sport.sport_type == 'Single-Player':
            return CustomUserSerializer
        return TeamSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    

class CustomUserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer


class TeamUpdate(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class EventPhotosAPIView(generics.ListAPIView):
    serializer_class = EventPhotoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        return EventPhoto.objects.filter(event_id=event_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context