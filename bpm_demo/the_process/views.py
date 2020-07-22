from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .gotostate import *
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
import uuid
import json
from django.core.serializers.json import DjangoJSONEncoder
import boto3

state_machine_arn = "arn:aws:states:ap-southeast-1:658793872383:stateMachine:Main_Steps"
workflow_execution_role = "arn:aws:iam::658793872383:role/service-role/StepFunctions-Main_Steps-role-b6d9e573"
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


def start_steps(id):
    response = sfn.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({'id': id})
    )
    return response['executionArn']


def get_execution_history(execution_arn):
    response = sfn.get_execution_history(executionArn=execution_arn)
    reply = parseFailureHistory(execution_arn)
    if (reply == 'Execution did not fail'):
        return json.dumps(response,cls=DjangoJSONEncoder)
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
    update_InspectionForm = Update_InspectionForm()
    context = {'create_InspectionForm': update_InspectionForm}
    return render(request, 'createInspection.html', context)

@never_cache
@require_POST
def CreateInspection(request):
    update_InspectionForm = Update_InspectionForm(request.POST)
    if update_InspectionForm.is_valid():
        print('-------------ok------------------')
        # create inspection here and update stepstatus
        stepStatus = StepStatus(title='sampleWorkflow',state_machine=state_machine_arn,execution_arn=execution_arn)
        stepStatus.save()
        # launch stepfunction
        execution_arn = start_steps(str(stepStatus.id))
        update_Inspection = update_InspectionForm.save(commit=False)
        update_Inspection.stepStatus = stepStatus
        update_Inspection.save()
        update_InspectionForm.save()
    return redirect('/')

# update inspection
@never_cache
def get_task(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    stepStatus.current_status = 'Update Inspection'
    stepStatus.assignee = 'OSHD1'
    stepStatus.save()
    update_Inspection = Update_Inspection.objects.get(stepStatus=stepStatus)
    the_form = Update_InspectionForm(instance=update_Inspection)
    latest_status = get_execution_history(stepStatus.execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=stepStatus.state_machine)['definition']
    context = { 'stateId': id, 'create_InspectionForm': the_form, 'latest_status': latest_status , 'definition': definition}
    return render(request, 'updateInspection.html', context)
#####################################################################

# finding
@never_cache
def get_finding(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    the_form = FindingsForm(initial={"stepStatus": stepStatus})
    latest_status = get_execution_history(execution_arn)
    # definition = get_execution_history(execution_arn)
    context = { 'stateId': id, 'finding_form': the_form, 'latest_status': latest_status}
    return render(request, 'Findings.html', context)

#####################################################################

# questionaire
@never_cache
def get_questionaire(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    the_form = Risk_AssessmentForm(initial={"stepStatus": stepStatus})
    latest_status = get_execution_history(execution_arn)
    context = { 'stateId': id, 'finding_form': the_form, 'latest_status': latest_status}
    return render(request, 'riskAssessment.html', context)
    
#####################################################################

# enforcement
@never_cache
def get_enforcement(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    the_form = FindingsForm(initial={"stepStatus": stepStatus})
    latest_status = """get_execution_history(execution_arn)"""
    context = { 'stateId': id, 'finding_form': the_form, 'latest_status': latest_status}
    return render(request, 'Findings.html', context)
#####################################################################


# vet approve
@never_cache
def get_vetApproveAction(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    the_form = FindingsForm(initial={"stepStatus": stepStatus})
    latest_status = """get_execution_history(execution_arn)"""
    context = { 'stateId': id, 'finding_form': the_form, 'latest_status': latest_status}
    return render(request, 'Findings.html', context)
#####################################################################


# 1) create inspection -> step function triggered
# 2) updateinspection -> Update_Inspection details -> send task success after getting task token via id+inspection_detail
# 3) updateinspection -> findings -> send task success after getting task token via id+Findings
# 4) updateinspection -> enforcement -> send task success after getting task token via id+enforcement
# 5) updateinspection -> questionaire -> send task success after getting task token via id+question
# 6)updateinspection -> send task success with the choices approve/Reassign/Clarification to go to approval stage/ update inspection again
# 7) approval stage -> approve /reject
