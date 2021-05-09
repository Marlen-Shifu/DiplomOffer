from django.shortcuts import render, redirect

from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import *
from .forms import *


class OfferListView(ListView):
	model = Offer
	template_name = "index.html"

	def get_queryset(self):
		qs = super().get_queryset()
		
		category = self.request.GET.get('category')
		subcategory = self.request.GET.get('subcategory')
		search = self.request.GET.get('search')

		if category != None:
			qs = qs.filter(category__title__icontains = category)

		if subcategory != None:
			qs = qs.filter(subcategory__title__icontains = subcategory)

		if search != None:
			qs = qs.filter(title__icontains = search)

		return qs


	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)

		context['category_farm'] = Category.objects.filter(title = 'Farm animals')

		context['category_plants'] = Category.objects.filter(title = 'Plants')

		context['category_techniques'] = Category.objects.filter(title = 'Techniques')

		return context



class LoginRegistrtionView(TemplateView):
	template_name = 'login.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['user_form'] = UserForm
		context['profile_form'] = ProfileForm

		context['login_form'] = UserAuthenticationForm

		return context


class UserLoginView(auth_views.LoginView):
	template_name = 'login.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['user_form'] = UserForm
		context['profile_form'] = ProfileForm

		return context



def registration(request):
	if request.method == 'POST':

		user_form = UserForm(request.POST)
		profile_form = ProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			return redirect('auth')
		else:
			return render(request, 'login.html', {'user_form': user_form, 'profile_form': profile_form, 'login_form': UserAuthenticationForm})

	else:
		return render(request, 'login.html', {'user_form': UserForm, 'profile_form': ProfileForm, 'login_form': UserAuthenticationForm})



class OfferCreateView(LoginRequiredMixin, CreateView):
	template_name = "put-an-ad.html"
	model = Offer
	fields = ['title', 'category', 'subcategory', 'price', 'description', 'image']
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user.profile
		self.object.save()
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['for_create'] = True
		return context


class UserOfferListView(LoginRequiredMixin, ListView):
	model = Offer
	template_name = 'my-ads.html'

	def get_queryset(self):
		qs = super().get_queryset()
		qs = qs.filter(user = self.request.user.profile)

		return qs


class UserOfferDetailView(LoginRequiredMixin, DetailView):
	model = Offer
	template_name = 'inside-ad.html'


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		category = self.object.category
		subcategory = self.object.subcategory

		ads = Offer.objects.filter(category = category, subcategory = subcategory).exclude(pk= self.object.pk)

		if ads.count() > 4:
			context['similar_ads'] = ads[:4]

		else:
			context['similar_ads'] = ads


		context['category_farm'] = Category.objects.filter(title = 'Farm animals')

		context['category_plants'] = Category.objects.filter(title = 'Plants')

		context['category_techniques'] = Category.objects.filter(title = 'Techniques')


		return context



class UserOfferUpdateView(LoginRequiredMixin, UpdateView):
	model = Offer
	template_name = 'put-an-ad.html'
	fields = ['title', 'category', 'subcategory', 'price', 'description', 'image']
	success_url = reverse_lazy('my_ads')

	def get_context_data(self):
		context = super().get_context_data()
		context['for_create'] = False
		return context


class UserOfferDeleteView(LoginRequiredMixin, DeleteView):
	model = Offer
	success_url = reverse_lazy('my_ads')


class ProfileView(LoginRequiredMixin, UpdateView):
	model = Profile
	fields = ['name', 'phone_number']
	template_name = 'my-profile.html'
	success_url = reverse_lazy('profile')

	def get_object(self, queryset = None):
		self.kwargs[self.pk_url_kwarg] = self.request.user.profile.pk
		obj = super().get_object(queryset)
		return obj


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
	model = User
	success_url = reverse_lazy('home')

	def get_object(self, queryset = None):
		self.kwargs[self.pk_url_kwarg] = self.request.user.pk
		obj = super().get_object(queryset)
		return obj


def logout_view(request):
	logout(request)
	return redirect('home')

