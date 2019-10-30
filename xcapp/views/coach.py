from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from .coach import Coach

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    """JSON serializer for users

    Arguments:
        serializers.HyperlinkedModelSerializer

    """
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name',
                  'last_name', 'email', 'date_joined', 'is_active')
        depth = 1

class CoachSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for coaches

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Coach
        url = serializers.HyperlinkedIdentityField(
            view_name='coach',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'user_id')


class coaches(ViewSet):
    """Coaches for XC"""

    def retrieve(self, request, pk=None):

        """Handle GET requests for single coach

        Returns:
            Response -- JSON serialized coach instance
        """
        try:
            coach = Coach.objects.get(pk=pk)
            serializer = CoachSerializer(coach, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a coach

            Response -- Empty body with 204 status code
        """
        coach = Coach.objects.get(pk=pk)
        coach.user.is_active = False
        coach.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to coaches resource

        Returns:
            Response -- JSON serialized list of coaches
        """
        coaches = Coach.objects.all()
        serializer = CoachSerializer(
            coaches,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)