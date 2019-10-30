from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import Runner, Team



class RunnerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Author: Scott Silver
    Purpose: JSON serializer for orders to convert native Python datatypes to
    be rendered into JSON
    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Runner
        url = serializers.HyperlinkedIdentityField(
            view_name='runner',
            lookup_field='id'
        )
        fields = ('id', 'url', 'grade', 'first_name', 'last_name', 'phone',
        'email', 'address', 'parent', 'team')
        depth = 1


class Meets(ViewSet):
    """Runners for xcapp
    Author: Scott Silver
    Purpose: Handle logic for operations performed on the Runner model to manage client requests for runners.
    database to GET PUT POST and DELETE entries.
    Methods: GET, PUT, POST, DELETE
    """
    def retrieve(self, request, pk=None):

        """Handle GET requests for single runner

        Returns:
            Response -- JSON serialized meet instance
        """
        try:
            runner = Runner.objects.get(pk=pk)
            serializer = RunnerSerializer(runner, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a meet

            Response -- Empty body with 204 status code
        """
        runner = Runner.objects.get(pk=pk)
        runner.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        runners = Runner.objects.all()
        serializer = RunnerSerializer(
            runners,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)