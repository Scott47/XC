from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import Runner, Team


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
        fields = ('id', 'url', 'grade', 'first_name', 'last_name', 'phone',
        'email', 'address', 'parent', 'team', 'runnermeet', 'roster')
        depth = 2


class Runners(ViewSet):
    """Runners for xcapp
    Author: Scott Silver
    Purpose: Handle logic for operations performed on the Runner model to manage client requests for runners.
    database to GET, PUT, POST, and DELETE entries.
    Methods: GET, PUT, POST, DELETE
    """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Runner instance
        """
        newrunner = Runner()
        newrunner.grade = request.data["grade"]
        newrunner.first_name = request.data["first_name"]
        newrunner.last_name = request.data["last_name"]
        newrunner.phone = request.data["phone"]
        newrunner.email = request.data["email"]
        newrunner.address = request.data["address"]
        newrunner.parent = request.data["parent"]
        newrunner.team = Team.objects.get(pk=request.data["team"])
        newrunner.save()

        serializer = RunnerSerializer(newrunner, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single runner

        Returns:
            Response -- JSON serialized runner instance
        """
        try:
            runner = Runner.objects.get(pk=pk)
            serializer = RunnerSerializer(runner, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        runner= Runner.objects.get(pk=pk)
        runner.grade = request.data["grade"]
        runner.first_name = request.data["first_name"]
        runner.last_name = request.data["last_name"]
        runner.phone = request.data["phone"]
        runner.email = request.data["email"]
        runner.address = request.data["address"]
        runner.parent = request.data["parent"]
        runner.team = Team.objects.get(pk=request.data["team"])
        runner.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single runner

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            runner = Runner.objects.get(pk=pk)
            runner.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Runner.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to runners resource

        Returns:
            Response -- JSON serialized list of runners
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        runners = Runner.objects.all()


        serializer = RunnerSerializer(
            runners, many=True, context={'request': request})

        return Response(serializer.data)

