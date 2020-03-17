from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from account.models import UserAccount
from account.api.serializers import RegistrationSerializer, UserUpdateSerializer, UserSerializer
from rest_framework import status
from django_statsd.clients import statsd
import pdb


@api_view(['POST'])
def registration_view(request):
    statsd.incr('api.register.user')
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['id'] = account.id
            data['first_name']= account.first_name
            data['last_name'] = account.last_name
            data['email_address'] = account.email_address
            data['account_created'] = account.account_created
            data['account_updated'] = account.account_updated
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT' ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def update_user_view(request):
    try:
        account = UserAccount.objects.get(email_address=request.user)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        statsd.incr('api.update.user')
        serializer = UserUpdateSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        statsd.incr('api.get.user')
        print(account)
        serializer = UserSerializer(account)
        return Response(serializer.data)
