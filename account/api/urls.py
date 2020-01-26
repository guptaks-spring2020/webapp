from django.urls import path
from account.api.views import(
	registration_view,
	#get_user_detail_view,
	update_user_view,

)

app_name = 'account'

urlpatterns = [
	path('user', registration_view, name="register"),
	path('user/self', update_user_view, name="get")
]
