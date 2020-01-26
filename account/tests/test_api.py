from rest_framework.test import APITestCase
from account.models import UserAccount
from account.api.serializers import validate_password


class RestAPITestCase(APITestCase):

    def test_if_password_is_valid(self):
        test_password = "@Kshitiz11"
        self.assertEqual(validate_password(test_password), True)
