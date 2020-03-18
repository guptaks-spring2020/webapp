import os
import statsd
from django_file_md5 import calculate_md5
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404
from rest_framework.views import APIView
import logging
from bills.models import Bills, BillFile
from account.models import UserAccount
from bills.api.serializers import CreateBillSerializer, BillSerializer, BillUpdateSerializer, FileSerializer, BillFileSerializer


import pdb

from webapp import settings

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

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
    data["attachment"] = bill.attachment
    return data


def load_bill_file_data(bill_file):
    #pdb.set_trace()
    data = {}
    data["file_name"] = bill_file.file_name
    data["id"] = bill_file.id
    if 'DB_HOST' in os.environ:
        data["url"] = str(bill_file.url.url.split('?')[0])
    else:
        data["url"] = str(bill_file.url)

    data["upload_date"] = bill_file.upload_date
    return data


@api_view(['GET','DELETE', 'PUT' ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def manage_user_bill_by_id(request, id):

    try:
        bill = Bills.objects.get(id=id)

    except Bills.DoesNotExist:
        logger.error("bill with the id: %s does not exists", bill.id)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if bill.owner_id != request.user:
        logger.error("bill for the owner with id: %s does not exists", bill.owner_id)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        statsd.start('api.get.bill.by.id.time.taken')
        statsd.increment('api.get.bill.by.id.count')
        serializer = BillSerializer(bill)
        statsd.stop('api.get.bill.by.id.time.taken')
        logger.info("bill has been created with the id: %s", bill.id)
        return Response(serializer.data)

    if request.method == 'DELETE':
        statsd.increment('api.delete.bill.by.id.count')
        statsd.start('api.get.bill.by.id.time.taken')
        #pdb.set_trace()
        try:

            bill_file = bill.attachment
            if 'DB_HOST' in os.environ:
                bill_file.url.delete(save=False)
            else:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, bill_file.url.name.split('/')[1]))
                except FileNotFoundError:
                    logger.error("bill with id: %s has been manually deleted", bill.id)
                    statsd.stop('api.delete.bill.by.id.time.taken')
                    return Response("File not found or has been manually deleted", status=status.HTTP_400_BAD_REQUEST)

            BillFile.objects.filter(id=bill_file.id).delete()

        except:
            statsd.stop('api.delete.bill.by.id.time.taken')
            logger.error("bad data in db",)
            return Response("bad data in db", status=status.HTTP_400_BAD_REQUEST)

        Bills.objects.filter(id=id).delete()
        logger.info("bill with the id: %s has been deleted", bill.id)
        statsd.stop('api.delete.bill.by.id.time.taken')
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        statsd.start('api.update.bill.by.id.time.taken')
        statsd.increment('api.update.bill.by.id.count')
        serializer = BillUpdateSerializer(bill, data=request.data)
        data = {}
        if serializer.is_valid():
            bill = serializer.save()
            data = load_bill_data_for_user(bill)
            statsd.stop('api.update.bill.by.id.time.taken')
            logger.info("bill with the id: %s has been updated", bill.id)
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)
        statsd.stop('api.update.bill.by.id.time.taken')
        logger.error("Something bad has happened: ", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def create_bill_view(request):
    try:
        account = UserAccount.objects.get(email_address=request.user)

        bill = Bills(owner_id=account)

    except Bills.DoesNotExist:
        logger.error("bill with the id: %s does not exists", bill.id)
        return Response(status=status.HTTP_404_NOT_FOUND)

    except UserAccount.DoesNotExist:
        logger.error("user with the id: %s does not exists", account.id)
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        statsd.start('api.create.bill.time.taken')
        statsd.increment('api.create.bill.for.user')
        serializer = CreateBillSerializer(context=bill, data=request.data)
        data = {}
        if serializer.is_valid():
            bill = serializer.save()
            data = load_bill_data_for_user(bill)
            statsd.stop('api.create.bill.time.taken')
            logger.info("bill with the id: %s has been created", bill.id)
            return Response(data, status=status.HTTP_201_CREATED)
        logger.error("Something bad has happened: ", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@authentication_classes([BasicAuthentication, ])
@permission_classes((IsAuthenticated,))
def get_bills_view(request):

    if request.method == 'GET':
        statsd.increment('api.get.bills.for.user')
        statsd.start('api.get.bills.time.taken')
        try:

            user = UserAccount.objects.get(email_address=request.user)

        except UserAccount.DoesNotExist:
            statsd.stop('api.get.bills.time.taken')
            logger.error("user with the id: %s doesn't exist", user.id)
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:

            bills = Bills.objects.all().filter(owner_id=user.id)

            if not bills:
                statsd.stop('api.get.bills.time.taken')
                logger.error("bills for the user id: %s has been created", user.id)
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Bills.DoesNotExist:
            logger.error("bills for the user id: %s has been created", user.id)
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bills, many=True)
        logger.info("bills for the user id: %s has been retrieved", user.id)
        statsd.stop('api.get.bills.time.taken')
        return Response(serializer.data)


def check_file_type(value):

    arr = ['pdf', 'png', 'jpg', 'jpeg']

    if not any(c in value for c in arr):
        return "invalid"


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @authentication_classes([BasicAuthentication, ])
    @permission_classes((IsAuthenticated,))
    def post(self, request, *args, **kwargs):
        statsd.increment('api.upload.bill.file.for.user')
        statsd.start('api.post.bill.file.time.taken')
        try:
            #pdb.set_trace()
            value = check_file_type(request.data['url'].content_type)
            size = request.data['url'].size
            md5_hash = str(calculate_md5(request.data['url']))
            #pdb.set_trace()
            if value == "invalid":
                statsd.stop('api.upload.bill.file.time.taken')
                logger.error("Allowed file types pdf, png, jpg or jpeg")
                return Response("Allowed file types pdf, png, jpg or jpeg", status=status.HTTP_400_BAD_REQUEST)

            bill = Bills.objects.get(id=kwargs['id'])

        except Bills.DoesNotExist:
            statsd.stop('api.upload.bill.file.time.taken')
            logger.error("bill with the id: %s does not exists", bill.id)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if bill.owner_id != request.user:
            statsd.stop('api.upload.bill.file.time.taken')
            logger.error("bill for the user id: %s does not exists", bill.owner_id)
            return Response(status=status.HTTP_404_NOT_FOUND)

        if bill.attachment is not None:
            statsd.stop('api.upload.bill.file.time.taken')
            logger.error("Bill  %s already exists, please delete it first", bill.id)
            return Response("Bill already exists, please delete it first", status=status.HTTP_400_BAD_REQUEST)

        bill_file = BillFile()

        file_serializer = FileSerializer(bill_file, data=request.data)
        if file_serializer.is_valid():
            file = file_serializer.save()
            file.size = size
            file.file_name = request.data['url'].name
            file.md5_hash = md5_hash

            file.save()

            data = load_bill_file_data(file)
            bill.attachment = file
            bill.save()
            logger.info("Bill file with the id: %s has been uploaded", file.id)
            statsd.stop('api.upload.bill.file.time.taken')
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            statsd.stop('api.upload.bill.file.time.taken')
            logger.error("something bad has happened", file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @authentication_classes([BasicAuthentication, ])
    @permission_classes((IsAuthenticated,))
    def get(self, request, *args, **kwargs):
        statsd.increment('api.get.bill.file.for.user')
        statsd.start('api.get.uploaded.bill.file.time.taken')
        try:

            bill = Bills.objects.get(id=kwargs['id'])
            bill_file = BillFile.objects.get(id=kwargs['bill_file_id'])

        except Bills.DoesNotExist:
            statsd.stop('api.get.uploaded.bill.file.time.taken')
            logger.error("bill with the id: %s does not exists", bill.id)
            return Response(status=status.HTTP_404_NOT_FOUND)

        except BillFile.DoesNotExist:
            logger.error("bill file with the id: %s does not exists", bill_file.id)
            statsd.stop('api.get.uploaded.bill.file.time.taken')
            return Response(status=status.HTTP_404_NOT_FOUND)

        if bill.owner_id != request.user:
            logger.error("bill for the user id: %s does not exists", bill.owner_id)
            statsd.stop('api.get.uploaded.bill.file.time.taken')
            return Response(status=status.HTTP_404_NOT_FOUND)

        #serializer = BillFileSerializer(bill_file)
        data = load_bill_file_data(bill_file)
        logger.info("bill file with the id: %s has been retrieved", bill_file.id)
        statsd.stop('api.get.uploaded.bill.file.time.taken')
        return Response(data)

    @authentication_classes([BasicAuthentication, ])
    @permission_classes((IsAuthenticated,))
    def delete(self, request, *args, **kwargs):

        try:
            #pdb.set_trace()
            statsd.start('api.delete.uploaded.bill.file.time.taken')
            statsd.increment('api.delete.bill.file.for.user')

            bill = Bills.objects.get(id=kwargs['id'])
            bill_file = BillFile.objects.get(id=kwargs['bill_file_id'])

            if bill.owner_id != request.user:
                logger.error("bill for the user id: %s does not exists", bill.owner_id)
                statsd.stop('api.delete.uploaded.bill.file.time.taken')
                return Response(status=status.HTTP_404_NOT_FOUND)
            BillFile.objects.filter(id=kwargs['bill_file_id']).delete()
            if 'DB_HOST' in os.environ:
                bill_file.url.delete(save=False)
            else:
                try:
                    os.remove(os.path.join(settings.MEDIA_ROOT, bill_file.url.name.split('/')[1]))
                except FileNotFoundError:
                    statsd.stop('api.delete.uploaded.bill.file.time.taken')
                    return Response("File not found or has been manually deleted", status=status.HTTP_400_BAD_REQUEST)
            statsd.stop('api.delete.uploaded.bill.file.time.taken')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FileNotFoundError:
            statsd.stop('api.delete.uploaded.bill.file.time.taken')
            logger.error("bill file with the id: %s does not exists", bill_file.id)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Bills.DoesNotExist:
            logger.error("bill with the id: %s does not exists", bill.id)
            statsd.stop('api.delete.uploaded.bill.file.time.taken')
            return Response(status=status.HTTP_404_NOT_FOUND)

        except BillFile.DoesNotExist:
            logger.error("bill with the id: %s does not exists", bill_file.id)
            statsd.stop('api.delete.uploaded.bill.file.time.taken')
            return Response("File not found", status=status.HTTP_400_BAD_REQUEST)

