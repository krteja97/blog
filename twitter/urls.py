from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('register/', views.register, name = 'register'),
	path('login/', views.login, name = 'login'),
	path('userhome/', views.userhome, name = 'userhome'),
	path('logout/', views.logout, name = 'logout'),

	#tweets display
	path('postTweet/', views.postTweet, name = 'postTweet'),
	path('tweets/', views.tweets, name = 'tweets'),
	path('users/<str:usernamestring>', views.users, name = 'users'),
	path('tweets/<int:tweetid>', views.individualtweet, name = 'individualtweet'),

]