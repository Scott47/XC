"""View module for handling requests about orderproducts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import RunnerMeet, Runner, Meet, Team
from .meet import MeetSerializer

class RunnerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for runners

    Arguments:
        serializers
    """

    class Meta:
        model = Runner
        url = serializers.HyperlinkedIdentityField(
            view_name='runner',
            lookup_field='id'
        )
        fields = ('id', 'url')
        depth = 2

class MeetSerializer(serializers.HyperlinkedModelSerializer):
    """
    Author: Scott Silver
    Purpose: JSON serializer for orders to convert native Python datatypes to
    be rendered into JSON
    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Meet
        url = serializers.HyperlinkedIdentityField(
            view_name='meet',
            lookup_field='id'
        )
        fields = ('id', 'url', 'date', 'name', 'distance', 'number_of_runners')
        depth = 1

class RunnerMeetSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for RunnerMeets

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    meet = MeetSerializer(many=False)
    class Meta:
        model = RunnerMeet
        url = serializers.HyperlinkedIdentityField(
            view_name='runnermeet',
            lookup_field='id'
        )
        fields = ('id', 'meet_time', 'place', 'PR', 'runner',
        'meet', 'pace', 'meet_id', 'meet_year')
        depth = 2

class RunnerMeets(ViewSet):
    """RunnerMeets for XC app"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized runner meets instance
        """
        new_runner_meet = RunnerMeet()
        new_runner_meet.runner = Runner.objects.get(pk=request.data["runner_id"])
        new_runner_meet.meet = Meet.objects.get(pk=request.data["meet_id"])
        new_runner_meet.meet_time = 11.25
        new_runner_meet.place = 2
        new_runner_meet.save()


        serializer = RunnerMeetSerializer(new_runner_meet, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        """Handle GET requests for single runner meet

        Returns:
            Response -- JSON serialized runnermeet instance
        """
        try:
            single_runner_meet = RunnerMeet.objects.get(pk=pk)
            serializer = RunnerMeetSerializer(single_runner_meet, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a runnermeet

        Returns:
            Response -- Empty body with 204 status code
        """
        runner_meet = RunnerMeet.objects.get(pk=pk)
        runner_meet.meet_time = request.data["meet_time"]
        runner_meet.place = request.data["place"]
        runner_meet.PR = request.data["PR"]
        runner_meet.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single runner meet

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            runner_meet = RunnerMeet.objects.get(pk=pk)
            runner_meet.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RunnerMeet.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to RunnerMeets resource

        Returns:
            Response -- JSON serialized list of runnermeets
        """
        runner_meets = RunnerMeet.objects.all()

        meet_year = self.request.query_params.get('meet_year', None)
        print("FLAG", meet_year)

        if meet_year is not None:
            print('meetmonkeytonail saying')
            runner_meets = runner_meets.filter(meet__date__iso_year=meet_year)


        serializer = RunnerMeetSerializer(
            runner_meets,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)