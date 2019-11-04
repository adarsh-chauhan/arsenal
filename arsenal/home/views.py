from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import * 		#import all tables
import os

# Create your views here.

aul=[str(user) for user in User.objects.all()]			#returns a List called aul (arsenaluserlist) from the default user database of django

def arsenal_home(request):			#this function caters request for home page
	return render(request,'home/home.html',{'arsenal_user':request.user})	#serves home.html page along with the name of the user(default:AnonymousUser) logged in


def arsenal_knowledgebase(request):
	kb=list(knowledge_base.objects.values())				#equivalent to select * from knowledge_base. this would be list and dictionary objects
	return render(request,'home/knowledgebase.html',{'kb':kb,'arsenal_user':request.user})		#passing dictionary to the template


def arsenal_repository(request):
	rp=list(repository.objects.values())
	return render(request,'home/repository.html',{'arsenal_user':request.user,'rp':rp})



def arsenal_inventory(request):
	if str(request.user) != 'AnonymousUser':
		query_inven_dict={}
		category=list(inventory._meta.get_field('category').choices)
		modorver=list(inventory._meta.get_field('modelorversion').choices)
		query_inven_dict['category']=category
		query_inven_dict['modorver']=modorver
			
		if request.method == 'GET':	
			return render(request,'home/inventory.html',{'arsenal_user':request.user,'query_inven_dict':query_inven_dict})
		else:
			category=request.POST['category']
			modorver=request.POST['modorver']
			db_res=list(inventory.objects.filter(modelorversion=modorver).values('category','identifier','modelorversion','checkedoutdate','checkedoutby__username','team'))
			return render(request,'home/inventory.html',{'arsenal_user':request.user,'query_inven_dict':query_inven_dict,'query_inven_res':db_res})	
	else:
		return render(request,'home/unauth.html',{'arsenal_user':request.user})

def arsenal_globalpolicies(request):
	gp_loc='/production/arsenal/home/static/home/documents/globalpolicies'
	gp=os.listdir(gp_loc)
	return render(request,'home/globalpolicies.html',{'arsenal_user':request.user,'gp':gp})


def arsenal_trendingidea(request):
	if str(request.user) != 'AnonymousUser':
		if request.method =='GET':
			ti=list(trendingidea.objects.values('readbyadmin','id','iname','idea','submittedon','readbyadmin','feasibilitycheck','submittedby__username','assignedto__username','hits'))
			return render(request,'home/trendingidea.html',{'arsenal_user':request.user,'ti':ti})
		elif request.method == 'POST':
			iname=request.POST['iname']
			description=request.POST['description']
			db_ti=trendingidea(iname=iname, idea=description, submittedby=request.user)
			db_ti.save()
			db_ti.support.add(request.user)
			ti=list(trendingidea.objects.values('readbyadmin','id','iname','idea','submittedon','support','readbyadmin','feasibilitycheck','submittedby__username','assignedto__username'))
			return render(request,'home/trendingidea.html',{'arsenal_user':request.user,'ti':ti})
	else:
		return render(request,'home/unauth.html',{'arsenal_user':request.user})

def arsenal_contact(request):
	upointer=list(user_extension.objects.select_related('user').filter(user__is_staff=True) .values('user__first_name','user__last_name','user__email','description','mobile','shift'))
	print(upointer)	
	return render(request,'home/contact.html',{'arsenal_user':str(request.user),'contact_info':upointer})


def arsenal_login(request):			#this function caters the request for the login page
	aul=[str(user) for user in User.objects.all()]

	if request.method=='get' or request.method=='GET':	#serves login page alaong with List aul to fill the username dropdown 
		return render(request,'home/login.html',{'arsenal_user':request.user,'arsenal_user_list':aul})	

	elif request.method=='post' or request.method=='POST':		#POST request is handled  when the user tries to authenticate with its credentials on login page
		arsenal_user=request.POST['username']
		arsenal_pass=request.POST['password']			#extracting username and password from POST request

		user=authenticate(request,username=arsenal_user,password=arsenal_pass)	#authenticating against the default django user database, which returns an user object if successful
		if user is not None:
			login(request,user)		#making a sessionid for the user after successful login, sessionkey is created which the client sends with every request.
			return render(request,'home/home.html',{'arsenal_user':user})		#redirects the users to to the home page as authentication was successful
		else:
			message="""<div class="alert alert-danger" role="alert">
				   <strong>Incorrect Password, try again !!</strong>
					</div>"""
			return render(request,'home/login.html',{'arsenal_user':request.user,'login_message':message,'arsenal_user_list':aul})	#when authentication fails the user is returned to the login page along with a message



def arsenal_count_view(request):						#this functions counts the view on a particular external link (for now links on knowledge base)
	page_id=request.GET.get('page_id',False)				#extracting the page id of from the url and setting default value as False
	page=request.GET.get('page',False)
	if page=='ti':
		db_ti=trendingidea.objects.get(id=page_id)
		db_ti.support.add(request.user)
		db_ti.hits=db_ti.support.count()
		db_ti.save()
		return redirect('/trendingidea')	
	elif page=='inven':
		db_inven=inventory.objects.get(identifier=page_id)
		prev_user_id=inventory.objects.filter(identifier=page_id).values('checkedoutby__id')
	
		if prev_user_id[0]["checkedoutby__id"]==request.user.id:
			return redirect('/inventory')
		else:
			db_inven.checkedoutby.clear()
			db_inven.checkedoutby.add(request.user)
			db_inven.save()
			return redirect('/inventory')
	elif page=='kb':
		i=knowledge_base.objects.get(id=page_id)				#equivalent to Select ... from knowledge_base where id = page_id
		i.hits=i.hits+1								#incrementing the hits/views
		i.save()								#saving the count in database
		url=list(knowledge_base.objects.filter(id=page_id).values('link'))	#equivalent to select link from knowledge_base where id = page_id and then converting to list as it would be queryset
	elif page=='rp':
		i=repository.objects.get(id=page_id)
		i.hits=i.hits+1
		i.save()
		url=list(repository.objects.filter(id=page_id).values('link'))
	print(url)							#extracting from above list which has one dictionary object
	return redirect(url[0]['link'])						#redirecting the user to external link



def arsenal_logout(request):	#this functions gets executed when the user clicks on logout
	aul=[str(user) for user in User.objects.all()]

	logout(request)		#destroying the sessionid for the user
	return render(request,'home/login.html',{'arsenal_user':request.user,'arsenal_user_list':aul})


