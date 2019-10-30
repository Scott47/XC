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
        meet.user.is_active = False
        meet.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        # objects.all() is an abstraction that the Object Relational Mapper
        # (ORM) in Django provides that queries the table holding
        # all the meets, and returns every row.
        meets = Meet.objects.all()
        serializer = MeetSerializer(
            meets,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
