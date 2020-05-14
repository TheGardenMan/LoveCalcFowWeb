import random
from . import db_handle
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect

# response=render(request,"feed.html",context)
# response.set_cookie('isLocationAvailable',value=True,max_age=None,path='/',httponly=True)

def register(request):
	if request.method=="GET":
		hash_from_cookie=request.COOKIES.get('owner_key')
		if not hash_from_cookie or not if_hash_exists(hash_from_cookie) :
			return render(request,"register.html")
		else:
			return redirect("/dashboard/")
	else:
		owner_name=request.POST.get('owner_name')
		isError,secret_hash_of_owner,owner_id=db_handle.register_owner(owner_name)
		if isError==None:
			# response=HttpResponseRedirect(''.join(["/dashboard/",str(secret_hash_of_owner)]))
			# we show / with dashboard.html..When he refreshes,it'll go to /dashboard
			response=render(request,"dashboard.html",{'owner_id':owner_id,'owner_name':owner_name,'secret_hash_of_owner':secret_hash_of_owner})
			response.set_cookie('owner_key',value=secret_hash_of_owner,max_age=31536000,path='/',httponly=True)
			return response
		else:
			return HttpResponse("Error occured")

def if_hash_exists(secret_hash_of_owner):
	if secret_hash_of_owner==None:
		return False
	if len(secret_hash_of_owner)==16:
		if db_handle.if_hash_exists(secret_hash_of_owner):
			return True
		return False
	return False 


def dashboard(request,secret_hash_of_owner=None):
	if secret_hash_of_owner!=None and if_hash_exists(secret_hash_of_owner):
		owner_id,owner_name=db_handle.get_owner_id_name(secret_hash_of_owner)
		users_and_crushes=db_handle.get_crush(owner_id)
		return render(request,"dashboard.html",{'owner_id':owner_id,'owner_name':owner_name,'secret_hash_of_owner':secret_hash_of_owner,'users_and_crushes':users_and_crushes})

	hash_from_cookie=request.COOKIES.get('owner_key')
	if hash_from_cookie!=None and if_hash_exists(hash_from_cookie):
		owner_id,owner_name=db_handle.get_owner_id_name(hash_from_cookie)
		users_and_crushes=db_handle.get_crush(owner_id)
		return render(request,"dashboard.html",{'owner_id':owner_id,'owner_name':owner_name,'secret_hash_of_owner':hash_from_cookie,'users_and_crushes':users_and_crushes})
	return redirect("/")


def calculate(request,owner_id=None):
	hash_from_cookie=request.COOKIES.get('owner_key')
	if if_hash_exists(hash_from_cookie):
		return redirect("/dashboard/")

	if request.method=="GET":
		if owner_id==None:
			return redirect("/")
		else:
			return render(request,"calculate.html")
	else:
		print(owner_id,"oioi")
		if owner_id==None:
			return redirect("/")
		else:
			user_name=request.POST.get('user_name')
			crush_name=request.POST.get('crush_name')
			db_handle.add_crush(owner_id,user_name,crush_name)
			owner_name=db_handle.get_owner_name(owner_id)
			return render(request,"pranked.html",{'user_name':user_name,'owner_name':owner_name})

# def pranked(request):
# def hash(request):
	