"""arsenal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from home import views, models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

urlpatterns = [
 	url(r'^$',views.arsenal_home),
	url(r'^login',views.arsenal_login),
	url(r'^logout',views.arsenal_logout),
	url(r'^contact',views.arsenal_contact),
	url(r'^knowledgebase',views.arsenal_knowledgebase),
	url(r'^inventory',views.arsenal_inventory),	
	url(r'^goto',views.arsenal_count_view, name='goto'),
	url(r'^repository', views.arsenal_repository),
	url(r'^trendingidea', views.arsenal_trendingidea),
	url(r'^globalpolicies', views.arsenal_globalpolicies),	
	]

def add_user_single_time():
	file=open('/production/arsenal/temp_user_list','r')
	list=[]
	for user in file.readlines():
		user=user.rstrip('\n')
		password=user+'@123@'+user
		email=user+'@cisco.com'
		

		cr_user=User.objects.create_user(username=user,email=email)
		cr_user.set_password(password)
		cr_user.save()
	
		test_user=authenticate(username=user,password=password)
		if test_user != None:print('{} created successfull!'.format(test_user))
		else:print('Error creating {}'.format(test_user))
	
	
		
def add_phone_single_time():
	file=open('/lab/arsenal/temp_phone_list','r')
	li=[]
	for i in file.readlines():
		entry=i.rstrip('\n').split(',')
		#print(entry,entry[0],entry[1],entry[2])
		db_en=models.inventory(identifier=entry[2],modelorversion=entry[0],team=entry[1],category=entry[3])
		db_en.save()
		print('success: ',entry[2])

# add_user_single_time()
# add_phone_single_time()


