from rest_framework import serializers
from account.models import UserAccount
import re


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserAccount
        fields = fields = ['id', 'email_address', 'first_name', 'last_name', 'account_created','account_updated']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email_address', 'first_name', 'last_name', 'password']

    def save(self):
        account = UserAccount(email_address=self.validated_data['email_address'],
                          first_name=self.validated_data['first_name'],
                          last_name=self.validated_data['last_name'],
                          )
        password = self.validated_data['password']

        is_password_valid = validate_password(password)

        if not is_password_valid:
            raise serializers.ValidationError({'password': 'Password must be strong.'})

        account.set_password(password)
        account.save()
        return account   


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email_address', 'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = self.validated_data['password']

        is_password_valid = validate_password(password)

        if not is_password_valid:
            raise serializers.ValidationError({'password': 'Password must be strong.'})

        instance.set_password(password)
        instance.save()
        return instance


def validate_password(password):

    is_password_valid = True

    while True:
            if len(password) < 8:
                is_password_valid = False
                break
            elif not re.search("[a-z]", password):
                is_password_valid = False
                break
            elif not re.search("[A-Z]", password):
                is_password_valid = False
                break
            elif not re.search("[0-9]", password):
                is_password_valid = False
                break
            elif not re.search("[_@$]", password):
                is_password_valid = False
                break
            elif re.search("\s", password):
                is_password_valid = False
                break
            else:
                is_password_valid = True
                print("Valid Password")
                break

    return is_password_valid        
