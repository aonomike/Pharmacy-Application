from django.shortcuts import render, render_to_response,get_object_or_404,redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import LoginForm
from django.contrib import messages

def LoginRequest(request):
    template_name = 'accounts/login.html'

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method=='POST':
        form=LoginForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            siteuser=authenticate(username=username,password=password)

            if siteuser is not None:
                """set a session id for this session"""
                login(request,siteuser)
                messages.info(request,'Welcome, {0}'.format(
                  siteuser.last_name + ' ' + siteuser.first_name))
                return HttpResponseRedirect('/')

            else:
                messages.warning(request,
                  "Sorry, the login credentials you've provided don't match any user account!")
                return render_to_response(template_name,{'form':form},
                  context_instance=RequestContext(request))
        else:
             messages.warning(request, "Ooops! Please correct the highlighted fields, then try again.")
             return render_to_response(template_name,{'form':form},context_instance=RequestContext(request))
                
            
    else:
        '''user is not submitting the form,show it'''
        form=LoginForm()
        context={'form':form}
        return render_to_response(template_name,context,
          context_instance=RequestContext(request))

def LogoutRequest(request):
  '''expires the session'''
  logout(request)
  return HttpResponseRedirect('/login/')