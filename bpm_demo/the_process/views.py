from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .gotostate import *
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import uuid
import json
import boto3

state_machine_arn = "arn:aws:states:ap-southeast-1:658793872383:stateMachine:Update_Inspection"
workflow_execution_role = "arn:aws:iam::764277912183:role/service-role/StepFunctions-MyStateMachine-role-52e618a7"
sfn = boto3.client('stepfunctions')
dynamodb = boto3.client('dynamodb')

# helper functions


def submit_approval(id, status, message):
    # get token from dynamo db
    task_token = dynamodb.get_item(TableName='steps', Key={
        'Key': {'S': id}})['Item']['task_token']['S']
    print("-----------------------------------------")
    print('Key', id, 'message', message)
    print(task_token)
    print("-----------------------------------------")
    response = sfn.send_task_success(
        taskToken=task_token,
        output=json.dumps({'id': id, 'status': status, 'message': message})
    )
    print("sent approval", response)
    return redirect('/')


def start_steps(id, comment):
    response = sfn.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({'id': id, 'comments': comment, 'mode': 'Normal'})
    )
    return response['executionArn']


def get_execution_history(execution_arn):
    response = sfn.get_execution_history(executionArn=execution_arn)
    reply = parseFailureHistory(execution_arn)
    if (reply == 'Execution did not fail'):
        result = response.get('events')
        result = list(map(lambda d: d.get('stateEnteredEventDetails'), result))
        result = list(filter(lambda d: d != None, result))
        result = list(map(lambda d: d.get('name'), result))
        return result[-1]
    else:
        return reply

################################ VIEWS #########################################
# Create your views here.


@never_cache
def index(request):
    inbox = StepStatus.objects.all()
    context = {'inbox': inbox}
    return render(request, 'index.html', context)


@never_cache
def CreateInspectionPage(request):
    inbox = Update_Inspection.objects.all()
    update_InspectionForm = Update_InspectionForm()
    context = {'create_InspectionForm': update_InspectionForm}
    return render(request, 'createInspection.html', context)

@never_cache
@require_POST
def CreateInspection(request):
    inbox = Update_Inspection.objects.all()
    update_InspectionForm = Update_InspectionForm()
    context = {'create_InspectionForm': update_InspectionForm}
    return render(request, 'createInspection.html', context)


@never_cache
def get_task(request, id):
    the_task = Submission.objects.get(pk=id)
    the_form = SubmissionForm(instance=the_task)
    execution_arn = the_task.execution_name
    latest_status = get_execution_history(execution_arn)
    context = {'state_form': the_form, 'latest_status': latest_status}
    return render(request, 'index.html', context)


# 1) create inspection -> step function triggered
# 2) updateinspection -> Update_Inspection details -> send task success after getting task token via id+inspection_detail
# 3) updateinspection -> findings -> send task success after getting task token via id+Findings
# 4) updateinspection -> enforcement -> send task success after getting task token via id+enforcement
# 5) updateinspection -> questionaire -> send task success after getting task token via id+question
# 6)updateinspection -> send task success with the choices approve/Reassign/Clarification to go to approval stage/ update inspection again
# 7) approval stage -> approve /reject
