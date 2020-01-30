from rest_framework import serializers
from bills.models import Bills
import re
import pdb


# {
#   "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
#   "created_ts": "2016-08-29T09:12:33.001Z",
#   "updated_ts": "2016-08-29T09:12:33.001Z",
#   "owner_id": "a460a1ef-6d54-4b01-90e6-d7017sad851",
#   "vendor": "Northeastern University",
#   "bill_date": "2020-01-06",
#   "due_date": "2020-01-12",
#   "amount_due": 7000.51,
#   "categories": [
#     "college",
#     "tuition",
#     "spring2020"
#   ],
#   "paymentStatus": "paid"
# }

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = ['id', 'created_ts', 'updated_ts', 'owner_id', 'vendor','bill_date', 'due_date','amount_due', 'categories', 'paymentStatus']


class CreateBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = ['vendor', 'bill_date', 'due_date', 'amount_due', 'categories', 'paymentStatus']

    def save(self):
        categories = self.validated_data['categories']

        if len(categories) != len(set(categories)):
            raise serializers.ValidationError({'categories': 'values should not be duplicate'})

        #pdb.set_trace()
        bill = self.context
        # bill = Bills(vendor=self.validated_data['vendor'],
        #                   bill_date=self.validated_data['bill_date'],
        #                   due_date=self.validated_data['due_date'],
        #                   amount_due=self.validated_data['amount_due'],
        #                   paymentStatus=self.validated_data['paymentStatus'],
        #                   categories=self.validated_data['categories'],
        #                   owner_id=self.context.owner_id
        #                   )

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
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.bill_date = validated_data.get('bill_date', instance.bill_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.amount_due = validated_data.get('amount_due', instance.amount_due)
        instance.categories = validated_data.get('categories', instance.categories)
        instance.paymentStatus = validated_data.get('paymentStatus', instance.paymentStatus)

        instance.save()
        return instance



