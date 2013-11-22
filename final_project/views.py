from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
#from django.contrib.auth.forms import UserCreationForm
from forms import SkraningarForm
from django.core.context_processors import csrf
from django.views.generic.base import View

class register(View):
	def get(self, request):
		args = {}
		args.update(csrf(request))

		args['form'] = SkraningarForm()
		return render_to_response('accounts/register.html', args)

	def post(self, request):
		form = SkraningarForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/account/success/')

class success(View):
	def get(self, request):
		return render_to_response('accounts/success.html')

class login(View):
	def get(self, request):
		c = {}
		c.update(csrf(request))
		return render_to_response('accounts/login.html', c)

class logout(View):
	def get(self, request):
		auth.logout(request)
		return render_to_response('accounts/logout.html')


def auth_view(request):
	# Ef notendanafn eda lykilord finnast ekki i forminu, faer tilsvarandi
	# breyta gildid tomi strengurinn.
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is None:
		return HttpResponseRedirect('/account/invalid/')
	auth.login(request, user)
	return HttpResponseRedirect('/account/logged/')
	
class logged(View):
	def get(self, request):
		return render_to_response('accounts/logged.html', {'nafn': request.user.username})

class invalid(View):
	def get(self, request):
		return render_to_response('accounts/invalid.html')	