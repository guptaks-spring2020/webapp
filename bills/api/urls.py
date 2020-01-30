# from django.urls import path
# from bills.api.views import(
# 	bill_view,
# 	get_user_bill,
# )
# import uuid
#
# app_name = 'bills'
#
# urlpatterns = [
# 	path('', bill_view, name="register"),
# 	#path('/abc', get_user_bill, name="get"),
# 	path('<uuid:id>', get_user_bill, name='article-section')
# 	#path('posts/<int:post_id>')
#
# #url(r'^users/(?P<user_id>\d+)/$', 'viewname', name='urlname')
# ]
from bills.api.views import handle404

handler404 = handle404