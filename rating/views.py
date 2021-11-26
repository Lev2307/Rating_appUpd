from django.shortcuts import render
from django.views import View
from .forms import SimpleForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView
from .models import Rating, Subject
from django.views.generic.edit import FormMixin
from .forms import RateForm
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin

class RatingsDetailView(FormMixin, DetailView):
    model = Subject
    form_class = RateForm
    template_name = 'rating/rating_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RateForm()
        return context

    def get_success_url(self):
        return reverse('main')


class RatingsDetailFormView(SingleObjectMixin, FormView):
    model = Subject
    form_class = RateForm
    template_name = 'rating/rating_detail.html'
    
    def get_success_url(self):
        return reverse('main')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            user = request.user
            rating = Rating(user=user, rate=form.data['rate'])
            rating.save()
            self.object.rating.add(rating)
            self.object.save()
            return self.form_valid(form)
        else:
            self.form_invalid(form)

class RatingsListView(ListView):
    model = Subject
    paginate_by = 5
    template_name = 'rating/rating_list.html'
    context_object_name = 'rating_objects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_context'] = 'Foo'
        return context

class RatingsEntryListView(ListView):
    template_name = 'rating/rating_by_name.html'
    context_object_name = 'rating_name_objects'

    def get_queryset(self):
        return Subject.objects.filter(name=self.kwargs['name'])


class RatingView(View):

    def get(self, request, *args, **kwargs):
        view = RatingsDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = RatingsDetailFormView.as_view()
        return view(request, *args, **kwargs)

class SimpleFormView(View):
    form_class = SimpleForm
    initial = {'foo': 'pel`meni'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("")
        
        return render(request, self.template_name, {'form': form})