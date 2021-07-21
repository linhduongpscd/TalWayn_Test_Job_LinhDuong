from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from django.template.loader import render_to_string
from subprocess import Popen, PIPE, STDOUT

from .models import *
from .forms import *

# Create your views here.
class ListJobView(View):
    def getlist(self, request):
        list_job = Job.objects.all()
        status = request.GET.get('status', None)
        if status == 'running':
            list_job = list_job.filter(status=True)
        elif status == 'stop':
            list_job = list_job.filter(status=False)
            
        page = request.GET.get('page', 1)
        paginator = Paginator(list_job, settings.NUMBER_PAGINATION)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        except:
            data = None
        context = {
            'list_job' : data,
            'parameter' : status
        }
        return context
    
    def get(self, request):
        if request.is_ajax() and 'auto_refresh' in request.GET:
            try:
                context = self.getlist(request)
                html = render_to_string('refresh_resutl.html',context=context)
                return HttpResponse(json.dumps({'status': "success", 'html' : html}), content_type='application/json')  
            except:
                return HttpResponse(json.dumps({'status': "false"}), content_type='application/json')  
        elif request.is_ajax() and 'refresh_status' in request.GET:
            try:
                process = Popen(['python',settings.BASE_DIR +'/project/refresh_statuses.py'], stdout=PIPE, stderr=STDOUT)
                output = process.stdout.read()
                exitstatus = process.poll()
                return HttpResponse(json.dumps({'status': "success"}), content_type='application/json')  
            except:
                return HttpResponse(json.dumps({'status': "false"}), content_type='application/json')  
        else:
            context = self.getlist(request)
            return render(request, 'index.html', context=context)
    
class CreateJobView(View):
    __doc__ = """
        Create Job view
    """
                
    def get(self, request):
        form = JobForm()
        context = {
            'form' : form,
            'title' : 'Create New Job'
        }
        return render(request, 'job.html', context=context)

    def post(self, request):
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        context = {
            'form' : form,
            'title' : 'Create New Job'
        }
        return render(request, 'job.html', context=context)
    
class UpdateJobView(View):
    __doc__ = """
       Update  Job view
    """
            
    def get(self, request, pk):
        instance = Job.objects.get(pk=pk)
        form = JobForm(instance = instance)
        context = {
            'form' : form,
            'title' : 'Update Job'
        }
        return render(request, 'job.html', context=context)
    
    def post(self, request, pk):
        instance = Job.objects.get(pk=pk)
        form = JobForm(request.POST, request.FILES, instance = instance)
        if form.is_valid():
            form.save()
            return redirect('index')
        context = {
            'form' : form,
            'title' : 'Update Job'
        }
        return render(request, 'job.html', context=context)

class DeleteJobView(View):
    __doc__ = """
       Delete Job view
    """
    def get(self, request, pk):
        instance = Job.objects.get(pk=pk)
        instance.delete()
        return redirect('index')
