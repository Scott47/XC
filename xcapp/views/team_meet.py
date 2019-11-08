"""View module for handling requests about orderproducts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import TeamMeet, Team, Meet


class TeamMeetSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for TeamMeets

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = TeamMeet
        url = serializers.HyperlinkedIdentityField(
            view_name='teammeet',
            lookup_field='id'
        )
        fields = ('id', 'total_time', 'points', 'team', 'meet', 'meet_id', 'meet_year')
        depth = 1

class TeamMeets(ViewSet):
    """TeamMeets for XC app"""

    def create(self, request):

        """
        Handle POST operations

        Returns:
            Response -- JSON serialized team meets instance
        """

        team_meet = TeamMeet()
        team_meet.team = Team.objects.get(pk=request.data["team"])
        team_meet.meet = Meet.objects.get(pk=request.data["meet"])
        team_meet.save()

        serializer = TeamMeetSerializer(team_meet, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single team meet

        Returns:
            Response -- JSON serialized teammeet instance
        """
        try:
            single_team_meet = TeamMeet.objects.get(pk=pk)
            serializer = TeamMeetSerializer(single_team_meet, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a teammeet

        Returns:
            Response -- Empty body with 204 status code
        """
        team_meet = TeamMeet.objects.get(pk=pk)
        team_meet.total_time = request.data["total_time"]
        team_meet.points = request.data["points"]
        team_meet.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        """Handle DELETE requests for a single team meet

        Returns:
            Response -- 200, 404, or 500 status code
        """

        try:
            team_meet = TeamMeet.objects.get(pk=pk)
            team_meet.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except TeamMeet.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        """Handle GET requests to TeamMeets resource

        Returns:
            Response -- JSON serialized list of teammeets
        """

        team_meets = TeamMeet.objects.all()
        meet_year = self.request.query_params.get('meet_year', None)
        print("FLAG", meet_year)

        if meet_year is not None:
            print('meetmonkeytonail saying')
            team_meets = team_meets.filter(meet__date__iso_year=meet_year)

        serializer = TeamMeetSerializer(
            team_meets,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)