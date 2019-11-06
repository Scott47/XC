from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import Team, Runner
from .runner import RunnerSerializer

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Author: Scott Silver
    Purpose: JSON serializer for teams to convert native Python datatypes to
    be rendered into JSON
    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    runnerteam = RunnerSerializer(many=True)

    class Meta:
        model = Team
        url = serializers.HyperlinkedIdentityField(
            view_name='team',
            lookup_field='id'
        )
        fields = ('id', 'url', 'team_name', 'runnerteam')
        depth = 2


class Teams(ViewSet):

    """Teams for xcapp
    Author: Scott Silver
    Purpose: Handle logic for operations performed on the Team model to manage client requests for teams.
    database to GET PUT POST and DELETE entries.
    Methods: GET, PUT, POST, DELETE
    """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Team instance
        """
        newteam = Team()
        newteam.team_name = request.data["team_name"]
        newteam.save()

        serializer = TeamSerializer(newteam, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        """Handle GET requests for single team

        Returns:
            Response -- JSON serialized team instance
        """
        try:
            team = Team.objects.get(pk=pk)
            serializer = TeamSerializer(team, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a team

            Response -- Empty body with 204 status code
        """
        team = Team.objects.get(pk=pk)
        team.team_name = request.data["team_name"]
        team.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to teams resource

        Returns:
            Response -- JSON serialized list of teams
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        teams = Team.objects.filter()

        serializer = TeamSerializer(
            teams,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)