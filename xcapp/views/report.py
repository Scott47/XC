from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import Meet, Coach, Team, Runner, RunnerMeet


class ReportSerializer(serializers.HyperlinkedModelSerializer):

    """
    Author: Scott Silver
    Purpose: JSON serializer for orders to convert native Python datatypes to
    be rendered into JSON

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = RunnerMeet
        url = serializers.HyperlinkedIdentityField(
            view_name='report',
            lookup_field='id'
        )
        fields = ('id', 'meet_time', 'place', 'PR', 'runner',
        'meet', 'pace', 'meet_id', 'meet_year')
        depth = 3


class Reports(ViewSet):

    """

    """

    def list(self, request):

        """Handle GET requests to  resource

        Returns:
            Response -- JSON serialized list of
        """

        coach = Coach.objects.get(user=request.auth.user)
        teams = Team.objects.filter(coach=coach)
        runners = Runner.objects.filter(team__in=teams)
        runner_meet_relationships = RunnerMeet.objects.filter(runner__in=runners)

        serializer = ReportSerializer(
            runner_meet_relationships,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)