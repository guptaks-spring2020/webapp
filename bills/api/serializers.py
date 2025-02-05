import os

from rest_framework import serializers
from bills.models import Bills, BillFile
import re
import pdb


class BillFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillFile
        fields = ['file_name', 'id', 'url', 'upload_date']

    def to_representation(self, instance):
        representation = super(BillFileSerializer, self).to_representation(instance)

        full_path = instance.url
        if 'DB_HOST' in os.environ:

            representation['url'] = full_path.url.split('?')[0]
        else:
            representation['url'] = full_path.name
        return representation


class BillSerializer(serializers.ModelSerializer):
    attachment = BillFileSerializer()

    class Meta:
        model = Bills
        fields = ['id', 'created_ts', 'updated_ts', 'owner_id', 'vendor','bill_date', 'due_date','amount_due', 'categories', 'paymentStatus', 'attachment']


class CreateBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = ['vendor', 'bill_date', 'due_date', 'amount_due', 'categories', 'paymentStatus']

    def save(self):
        categories = self.validated_data['categories']

        if len(categories) != len(set(categories)):
            raise serializers.ValidationError({'categories': 'values should not be duplicate'})

        bill = self.context

        bill.vendor = self.validated_data['vendor']
        bill.bill_date = self.validated_data['bill_date']
        bill.due_date = self.validated_data['due_date']
        bill.amount_due = self.validated_data['amount_due']
        bill.paymentStatus = self.validated_data['paymentStatus']
        bill.categories = self.validated_data['categories']
        bill.owner_id = self.context.owner_id

        bill.save()

        return bill


class BillUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = ['vendor', 'bill_date', 'due_date', 'amount_due', 'categories', 'paymentStatus']

    def update(self, instance, validated_data):
        categories = self.validated_data['categories']
        if len(categories) != len(set(categories)):
            raise serializers.ValidationError({'categories': 'values should not be duplicate'})

        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.bill_date = validated_data.get('bill_date', instance.bill_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.amount_due = validated_data.get('amount_due', instance.amount_due)
        instance.categories = validated_data.get('categories', categories)
        instance.paymentStatus = validated_data.get('paymentStatus', instance.paymentStatus)

        instance.save()
        return instance


# class BillAttachmentSerializer(serializers.ModelSerializer):
#     model =
#


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillFile
        fields = ['url']

