from rest_framework import serializers
from ..models import Sport, Team, CustomUser, Competition, Event, EventPhoto

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name', 'sport_type')

class TeamSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'sport', 'avatar', 'rating_points', 'wins', 'losses')


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email')


class TeamDetailSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='members')
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'sport', 'avatar', 'rating_points', 'wins', 'losses', 'members', 'member_ids')


class TeamUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.filter(is_superuser=False, is_staff=False), required=False)
    
    class Meta:
        model = Team
        fields = ('name', 'members')

class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'avatar', 'rating_points', 'wins', 'losses')
    
    def get_avatar(self, obj):
        if obj.avatar:
            try:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.avatar.url)
                return obj.avatar.url
            except:
                return None
        return None
        
class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name']
        
class EventSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    event_type = serializers.CharField(default='Event')
    
    creator = CreatorSerializer()
    participants_count = serializers.IntegerField(source='participants.count')
    declined_participants_count = serializers.IntegerField(source='declined_participants.count')

    class Meta:
        model = Event
        fields = ('id', 'name', 'sport', 'start_date_time', 'end_date_time', 'location', 'description', 'participants_count', 'declined_participants_count', 'creator', 'event_type')
            
        
class CompetitionSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    event_type = serializers.CharField(default='Competition')

    class Meta:
        model = Competition
        fields = ('id', 'name', 'sport', 'start_date_time', 'end_date_time', 'side_a', 'side_b', 'side_a_score', 'side_b_score', 'location', 'description', 'status', 'event_type')

class EventPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = EventPhoto
        fields = ('id', 'event', 'photo', 'photo_url', 'uploaded_at', 'description')
    
    def get_photo_url(self, obj):
        if obj.photo:
            try:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.photo.url)
                return obj.photo.url
            except:
                return None
        return None