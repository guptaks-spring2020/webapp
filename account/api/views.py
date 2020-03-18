import statsd
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from account.models import UserAccount
from account.api.serializers import RegistrationSerializer, UserUpdateSerializer, UserSerializer
from rest_framework import status
import logging
import pdb

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        statsd.increment('api.register.user.count')

        statsd.start('api.register.user.time.taken')
        # Do something fun.

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
            logger.info("User has been created with the id: %s", account.id)
            statsd.stop()
            return Response(data, status=status.HTTP_201_CREATED)
        logger.error("Something bad has happened: %s", serializer.errors)
        statsd.stop('api.register.user.time.taken')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT' ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def update_user_view(request):
    api_timer = statsd.timer.Timer()

    try:
        account = UserAccount.objects.get(email_address=request.user)
    except UserAccount.DoesNotExist:
        logger.error("User with the account id: %s does not exists", account.id)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        statsd.start('api.update.user.time.taken')
        statsd.increment('api.update.user')
        serializer = UserUpdateSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            api_timer.stop('api.update.user.time.taken')
            logger.info("User has been updated with the id: %s", account.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        statsd.stop('api.update.user.time.taken')
        logger.error("Something bad has happened: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        statsd.increment('api.get.user')
        statsd.start('api.get.user.time.taken')
        print(account)
        serializer = UserSerializer(account)
        logger.info("User has been retrieved with the id: %s", account.id)
        statsd.stop('api.get.user.time.taken')
        return Response(serializer.data)
