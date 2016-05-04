from django.shortcuts import render
from .models import JobOpenings
from django.utils import timezone

# Create your views here.

def job_list(request):
    job_list = JobOpenings.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'general/job_list.html', {'job_list': job_list})