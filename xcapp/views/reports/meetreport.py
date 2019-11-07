from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import RunnerMeet, Team



class MeetReportSerializer(serializers.HyperlinkedModelSerializer):
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
            view_name='runnermeet',
            lookup_field='id'
        )
        fields = ('id', 'url', 'meet', 'runnermeet', 'meetrunner',
        'number_of_runners', 'runnerteam', 'meet_time', 'pace')
        depth = 3


class MeetReports(ViewSet):
    """Meets for xcapp
    Author: Scott Silver
    Purpose: Handle logic for operations performed on the
    RunnerMeet model to manage client requests for meet reports.
    database to GET PUT POST and DELETE entries.
    Methods: GET
    """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Runner instance
        """
        newmeetreport = RunnerMeet()
        newmeet.name = request.data["name"]
        newmeet.course = request.data["course"]
        newmeet.url = request.data["url"]
        newmeet.address = request.data["address"]
        newmeet.date = request.data["date"]
        newmeet.distance = request.data["distance"]
        newmeetreport.save()

        serializer = MeetReportSerializer(newmeetreport, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        """Handle GET requests for single meet

        Returns:
            Response -- JSON serialized meet instance
        """
        try:
            meetreport = RunnerMeet.objects.get(pk=pk)
            serializer = MeetReportSerializer(meetreport, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        meetreports = RunnerMeet.objects.all()
        meetteams = Team.objects.all()
        meetdates = RunnerMeet.objects.order_by('date')
        serializer = MeetReportSerializer(
            meetteams,
            meetdates,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
