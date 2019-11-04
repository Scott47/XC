from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from xcapp.models import Meet



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
        fields = ('id', 'url', 'name', 'course', 'url', 'address',
        'latitude', 'longitude', 'date', 'distance', 'number_of_runners')
        depth = 1


class Meets(ViewSet):
    """Meets for xcapp
    Author: Scott Silver
    Purpose: Handle logic for operations performed on the Meet model to manage client requests for meets.
    database to GET PUT POST and DELETE entries.
    Methods: GET, PUT, POST, DELETE
    """

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Runner instance
        """
        newmeet = Meet()
        newmeet.name = request.data["name"]
        newmeet.course = request.data["course"]
        newmeet.url = request.data["url"]
        newmeet.address = request.data["address"]
        newmeet.latitude = request.data["latitude"]
        newmeet.longitude = request.data["longitude"]
        newmeet.date = request.data["date"]
        newmeet.distance = request.data["distance"]
        newmeet.number_of_runners = request.data["number_of_runners"]
        newmeet.save()

        serializer = MeetSerializer(newmeet, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        """Handle GET requests for single meet

        Returns:
            Response -- JSON serialized meet instance
        """
        try:
            meet = Meet.objects.get(pk=pk)
            serializer = MeetSerializer(meet, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a meet

            Response -- Empty body with 204 status code
        """
        meet = Meet.objects.get(pk=pk)
        meet.name = request.data["name"]
        meet.course = request.data["course"]
        meet.url = request.data["url"]
        meet.address = request.data["address"]
        meet.latitude = request.data["latitude"]
        meet.longitude = request.data["longitude"]
        meet.date = request.data["date"]
        meet.distance = request.data["distance"]
        meet.number_of_runners = request.data["number_of_runners"]
        meet.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single meet

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            meet = Meet.objects.get(pk=pk)
            meet.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Meet.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        meets = Meet.objects.all()
        meetdates = Meet.objects.order_by('date')
        serializer = MeetSerializer(
            meetdates,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
