from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import uuid
from django.http import Http404
from bills.models import Bills
from account.models import UserAccount
from bills.api.serializers import CreateBillSerializer, BillSerializer, BillUpdateSerializer

import pdb

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

def handle404(request, exception):

    raise Http404("This url does not exist")


@api_view(['GET','DELETE', 'PUT' ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def manage_user_bill_by_id(request, id):
    #pdb.set_trace()

    try:
        #identity = uuid.UUID(uuid_id)
        bill = Bills.objects.get(id=id)

    except Bills.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        # identity = uuid.UUID(uuid_id)
        user = UserAccount.objects.get(email_address=request.user)

    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("get")
        # data = {}
        # data['id'] = id
        serializer = BillSerializer(bill)
        return Response(serializer.data)

    if request.method == 'DELETE':
        print("delete")
        # data = {}
        # data['uuid_id'] = id
        # serializer = BillSerializer(bill)
        Bills.objects.filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #return Response(uuid_id, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = BillUpdateSerializer(bill, data=request.data)
        data = {}
        if serializer.is_valid():
            bill = serializer.save()
            data["id"] = bill.id
            data["created_ts"] = bill.created_ts
            data["updated_ts"] = bill.updated_ts
            data["owner_id"] = bill.owner_id.id
            data["vendor"] = bill.vendor
            data["bill_date"] = bill.bill_date
            data["due_date"] = bill.due_date
            data["amount_due"] = bill.amount_due
            data["categories"] = bill.categories
            data["paymentStatus"] = bill.paymentStatus
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def create_bill_view(request):
    #pdb.set_trace()
    try:
        account = UserAccount.objects.get(email_address=request.user)

        bill = Bills(owner_id=account)

    except Bills.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CreateBillSerializer(context=bill, data=request.data)
        data = {}
        if serializer.is_valid():
            bill = serializer.save()
            data["id"] = bill.id
            data["created_ts"] = bill.created_ts
            data["updated_ts"] = bill.updated_ts
            data["owner_id"] = bill.owner_id.id
            data["vendor"] = bill.vendor
            data["bill_date"] = bill.bill_date
            data["due_date"] = bill.due_date
            data["amount_due"] = bill.amount_due
            data["categories"] = bill.categories
            data["paymentStatus"] = bill.paymentStatus

            #serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def get_bills_view(request):
    #pdb.set_trace()
    try:
        account = UserAccount.objects.get(email_address=request.user)

        #bill = Bills(owner_id=account)

    # except Bills.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        #pdb.set_trace()
        try:
            # identity = uuid.UUID(uuid_id)
            user = UserAccount.objects.get(email_address=request.user)

        except UserAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            # identity = uuid.UUID(uuid_id)

            bills = Bills.objects.all().filter(owner_id=user.id)
            if not bills:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Bills.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # # if bill.owner_id != request.user:
        # #     return Response(status=status.HTTP_401_UNAUTHORIZED)
        #
        # print("hi")
        # data = {}
        # data['uuid_id'] = id
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
