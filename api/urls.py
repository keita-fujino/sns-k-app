from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user' #名前空間の設定

#
router = DefaultRouter()
router.register('profile',views.ProfileViewSet) # profileの登録
router.register('post', views.PostViewSet) # postの登録
router.register('comment', views.CommentViewSet) # commentの登録

urlpatterns = [
  path('register/', views.CreateUserView.as_view(), name='register'),
  path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
  path('',include(router.urls))
]
