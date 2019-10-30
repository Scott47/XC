from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import Team, Runner



class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Author: Scott Silver
    Purpose: JSON serializer for orders to convert native Python datatypes to
    be rendered into JSON
    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Team
        url = serializers.HyperlinkedIdentityField(
            view_name='team',
            lookup_field='id'
        )
        fields = ('id', 'url', 'team_name')
        depth = 1


class Meets(ViewSet):
    """Teams for xcapp
    Author: Scott Silver
    Purpose: Handle logic for operations performed on the Team model to manage client requests for teams.
    database to GET PUT POST and DELETE entries.
    Methods: GET, PUT, POST, DELETE
    """
    def retrieve(self, request, pk=None):

        """Handle GET requests for single team

        Returns:
            Response -- JSON serialized meet instance
        """
        try:
            team = Team.objects.get(pk=pk)
            serializer = TeamSerializer(runner, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a meet

            Response -- Empty body with 204 status code
        """
        team = Team.objects.get(pk=pk)
        team.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        teams = Team.objects.all()
        serializer = TeamSerializer(
            teams,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)