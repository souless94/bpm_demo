from django.shortcuts import render, redirect
from .forms import TaskForm, StateForm
from .models import Task , state
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import uuid

# Create your views here.
@never_cache
def index(request):
    the_inbox = Task.objects.all()
    the_form = TaskForm(initial={'submission_id': str(uuid.uuid4())})
    context = {'the_form':the_form ,'inbox':the_inbox}
    return render(request,'index.html',context)

@never_cache
@require_POST
def submit(request):
    the_form = TaskForm(request.POST)
    data = request.POST.dict()
    print(data)
    if the_form.is_valid():
        the_form.save()
    return redirect('/')


@never_cache
def get_task(request,taskId):
    the_task = Task.objects.get(pk=taskId)
    username = the_task.username
    the_state_exists = state.objects.filter(submission=the_task).exists()
    state_form = StateForm(initial={'submission': taskId })
    the_state = 'start'
    if the_state_exists:
        the_state = state.objects.filter(submission=the_task).order_by('-submit_time')
        the_state = the_state[0]
        the_state.submit_time = now
        state_form = StateForm(instance=the_state)
        the_state = the_state.status
        
    diagram = ['start','verify','reassign','approve']
    context = {'state_form':state_form, 'diagram':diagram ,'the_state':the_state,'username':username}
    return render(request,'submit.html',context)

@never_cache
@require_POST
def start_execution(request):
    the_form = StateForm(request.POST)
    if the_form.is_valid():
        data = request.POST.dict()
        the_task = Task.objects.get(pk=data.get("submission"))
        the_task.status = data.get('status')
        the_task.save()
        the_form.save()
    return redirect('/')