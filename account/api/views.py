from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from account.models import UserAccount
from account.api.serializers import RegistrationSerializer, UserUpdateSerializer, UserSerializer
from rest_framework import status
import pdb


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'User has been successfull registered'
            data['uuid_id'] = account.id
            data['email_address'] = account.email_address
            data['first_name']= account.first_name
            data['last_name'] = account.last_name
            data['account_created'] = account.account_created
            data['account_updated'] = account.account_updated
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', ])
# @authentication_classes([BasicAuthentication, ])
# @permission_classes((IsAuthenticated,))
# def get_user_detail_view(request):
#     try:
#         #pdb.set_trace()
#         account = UserAccount.objects.get(email_address=request.user)
#         print("inside try")
#     except UserAccount.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = UserSerializer(account)
#         #print("Valid Password")
#         return Response(serializer.data)


@api_view(['GET', 'PUT' ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def update_user_view(request):
    try:
        account = UserAccount.objects.get(email_address=request.user)
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'successfully updated.'
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        print(account)
        serializer = UserSerializer(account)
        #print("Valid Password")
        return Response(serializer.data)
