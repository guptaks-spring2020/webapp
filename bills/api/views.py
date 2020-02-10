from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
import uuid
from django.http import Http404
from rest_framework.views import APIView

from bills.models import Bills, BillFile
from account.models import UserAccount
from bills.api.serializers import CreateBillSerializer, BillSerializer, BillUpdateSerializer, FileSerializer, BillFileSerializer


import pdb

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

def handle404(request, exception):

    raise Http404("This url does not exist")


def load_bill_data_for_user(bill):
    data = {}
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
    return data


def load_bill_file_data(bill_file):
    data = {}
    data["file_name"] = bill_file.file_name
    data["id"] = bill_file.id
    data["url"] = bill_file.url
    data["upload_date"] = bill_file.upload_date
    return data


@api_view(['GET','DELETE', 'PUT' ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def manage_user_bill_by_id(request, id):

    try:
        bill = Bills.objects.get(id=id)

    except Bills.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("get")
        serializer = BillSerializer(bill)
        return Response(serializer.data)

    if request.method == 'DELETE':
        print("delete")
        Bills.objects.filter(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        serializer = BillUpdateSerializer(bill, data=request.data)
        data = {}
        if serializer.is_valid():
            bill = serializer.save()
            data = load_bill_data_for_user(bill)

            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def create_bill_view(request):
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
            data = load_bill_data_for_user(bill)

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def get_bills_view(request):

    if request.method == 'GET':

        try:

            user = UserAccount.objects.get(email_address=request.user)

        except UserAccount.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:

            bills = Bills.objects.all().filter(owner_id=user.id)
            if not bills:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Bills.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)


# @api_view(['POST', ])
# @authentication_classes([BasicAuthentication, ])
# @permission_classes((IsAuthenticated,))
# def upload_bill(request):
#
#     try:
#         bill = Bills.objects.get(id=id)
#
#
#     except Bills.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if bill.owner_id != request.user:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     bill_file = BillFile(id=bill)


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @authentication_classes([BasicAuthentication, ])
    @permission_classes((IsAuthenticated,))
    def post(self, request, *args, **kwargs):

        try:
            pdb.set_trace()
            bill = Bills.objects.get(id=kwargs['id'])

        except Bills.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if bill.owner_id != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bill_file = BillFile()

        file_serializer = FileSerializer(bill_file, data=request.data)
        if file_serializer.is_valid():
          file = file_serializer.save()

          bill.attachment = file
          bill.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authentication_classes([BasicAuthentication, ])
    @permission_classes((IsAuthenticated,))
    def get(self, request, *args, **kwargs):

        try:
            pdb.set_trace()
            bill = Bills.objects.get(id=kwargs['id'])
            bill_file = BillFile.objects.get(id=kwargs['bill_file_id'])

        except Bills.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if bill.owner_id != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BillFileSerializer(bill_file)
        return Response(serializer.data)

    @authentication_classes([BasicAuthentication, ])
    @permission_classes((IsAuthenticated,))
    def delete(self, request, *args, **kwargs):

        try:
            pdb.set_trace()
            bill = Bills.objects.get(id=kwargs['id'])

            if bill.owner_id != request.user:
                return Response(status=status.HTTP_404_NOT_FOUND)

            BillFile.objects.filter(id=kwargs['bill_file_id']).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Bills.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
