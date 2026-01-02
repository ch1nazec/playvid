from django.urls import include, path
from users import views


urlpatterns = [
    path('', views.UserView.as_view(), name='user-view'),
    path('channel/', views.ChannelView.as_view(), name='channel-view')
]
