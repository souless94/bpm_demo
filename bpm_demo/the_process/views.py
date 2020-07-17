from django.shortcuts import render, redirect
from .forms import SubmissionForm
from .models import Submission
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import uuid
import json
import boto3

state_machine_arn="arn:aws:states:ap-southeast-1:658793872383:stateMachine:Update_Inspection"
workflow_execution_role = "arn:aws:iam::658793872383:role/service-role/StepFunctions-Update_Inspection-role-08672079"
sfn = boto3.client('stepfunctions')
dynamodb = boto3.client('dynamodb')

# helper functions
def submit_approval(id,status, message):
    # get token from dynamo db 
    task_token = dynamodb.get_item(TableName='Update_Inspection', Key={
        'Key': {'S': id}})['Item']['task_token']['S']
    print("-----------------------------------------")
    print('Key', id,'message' ,message)
    print(task_token)
    print("-----------------------------------------")
    response = sfn.send_task_success(
        taskToken=task_token,
        output=json.dumps({'id':id,'status': status ,'message':message})
    )
    print("sent approval", response)
    return redirect('/')

def start_steps(id,comment):
    response = sfn.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({'id':id,'comments':comment,'mode':'Normal'})
    )
    return response['executionArn']

def get_execution_history(execution_arn):

    response = sfn.get_execution_history(
            executionArn = execution_arn
    )
    result = response.get('events')
    if (result[-1].get('executionFailedEventDetails')):
        error = result[-1]['executionFailedEventDetails']['error']
        if (str(error) == 'States.Timeout'):
            return 'Please resume from resume function'
    result = list(map(lambda d: d.get('stateEnteredEventDetails'), result))
    result = list(filter(lambda d: d != None , result))
    result = list(map(lambda d: d.get('name') , result))
    return result[-1]

# Create your views here.
@never_cache
def index(request):
    the_form = SubmissionForm(initial={
        'state_machine': state_machine_arn,
        'execution_name': "None"
    })
    inbox = Submission.objects.all()
    context = {'the_form':the_form,'inbox': inbox}
    return render(request,'index.html',context)


@never_cache
def get_task(request,id):
    the_task = Submission.objects.get(pk=id)
    the_form = SubmissionForm(instance=the_task)
    execution_arn = the_task.execution_name
    latest_status = get_execution_history(execution_arn)
    context = {'state_form':the_form,'latest_status':latest_status}
    return render(request,'submit.html',context)

@never_cache
@require_POST
def start_execution(request):
    the_form = SubmissionForm(request.POST)
    if the_form.is_valid():
        data = request.POST.dict()
        title= data['title']
        execution_arn = start_steps(title,data['comment'])
        the_form.save()
        the_task = Submission.objects.get(title=title)
        the_task.execution_name = execution_arn
        the_task.save()
    return redirect('/')

@never_cache
@require_POST
def submit(request):
    data = request.POST.dict()
    title = data['title']
    the_task = Submission.objects.get(title=title)
    the_form = SubmissionForm(request.POST, instance=the_task)
    status = data['choice']
    if the_form.is_valid():
        comment = data['comment']
        the_form.save()
        submit_approval(title,status,comment)
    return redirect('/')

@never_cache
@require_POST
def resume(request):
    data = request.POST.dict()
    id = data['id']
    inputs = json.loads(data['inputs'])
    inputs['mode']='Skip'
    state = data['state']
    definition = sfn.describe_state_machine(stateMachineArn=state_machine_arn)['definition']
    definition= json.loads(definition)
    definition["States"]["Mode"]["Default"] = state
    definition = json.dumps(definition)
    response = sfn.create_state_machine(
        name="resume{}".format(str(uuid.uuid4())), definition=definition, roleArn=workflow_execution_role)
    execution_response = sfn.start_execution(
        stateMachineArn=response['stateMachineArn'],
        input=json.dumps(inputs)
    )
    the_task = Submission.objects.get(title=id)
    the_task.state_machine = response['stateMachineArn']
    the_task.current_status = state
    the_task.execution_name = execution_response['executionArn']
    the_task.save()
    return redirect('/')

