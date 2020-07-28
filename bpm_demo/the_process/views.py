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
from django.http import HttpResponse
import boto3
import time

state_machine_arn = "arn:aws:states:ap-southeast-1:764277912183:stateMachine:MyStateMachine"
workflow_execution_role = "arn:aws:iam::764277912183:role/service-role/StepFunctions-MyStateMachine-role-ce3aeb8f"
sfn = boto3.client('stepfunctions')
dynamodb = boto3.client('dynamodb')

# helper functions

def get_final_task_token(id):
    task_token = dynamodb.get_item(TableName='steps', Key={
            'id': {'S': id}})['Item']['final_task_token']['S']
    return task_token

def get_finding_arn(id):
    arn = dynamodb.get_item(TableName='steps', Key={
            'id': {'S': id}})['Item']['executionArn']['S']
    return arn

def resume_steps(id,value="Approve",mode="Normal"):
    # get token from dynamo db
    print(id)
    task_token = dynamodb.get_item(TableName='steps', Key={
        'id': {'S': id}})['Item']['task_token']['S']
    if (mode == "Finding"):
        print('finished the finding workflow')
        task_token = get_final_task_token(id)
    print("-----------------------------------------")
    print('id', id)
    print(task_token)
    print("-----------------------------------------")
    response = sfn.send_task_success(
        taskToken=task_token,
        output=json.dumps({'id': id,'value':value})
    )
    time.sleep(1.4)
    print("sent approval", response)


def start_steps(id,state_machine_arn=state_machine_arn):
    response = sfn.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({'id': id,'resuming':True})
    )
    return response['executionArn']

def get_current_status(execution_arn):
    response = sfn.get_execution_history(executionArn=execution_arn)
    reply = parseFailureHistory(execution_arn)
    print(reply)
    if (reply == 'Execution did not fail'):
        result = json.loads(json.dumps(response,cls=DjangoJSONEncoder)).get('events')
        check = list(map(lambda d: d.get('type'), result))
        if 'ParallelStateEntered' in check and 'ParallelStateSucceeded' not in check :
            result = list(filter(lambda d: d.get('type') == 'ParallelStateEntered', result))
            result = result[-1]['stateEnteredEventDetails']['name']
            return result
        else:
            result = list(map(lambda d: d.get('stateEnteredEventDetails'), result))
            result = list(filter(lambda d: d != None, result))
            result = list(map(lambda d: d.get('name'), result))
            return result[-1]
    else:
        # resume_failed_steps(execution_arn,reply)
        return 'Failed'

def get_execution_history(execution_arn):
    response = sfn.get_execution_history(executionArn=execution_arn)
    return json.dumps(response,cls=DjangoJSONEncoder)

def resume_failed_steps(execution_arn,failed_step,id):
    # first check if parallel
    stateMachineArn = smArnFromExecutionArn(execution_arn)
    delete_state_machine(stateMachineArn)
    newStateMachineArn = attachGoToState(failed_step,stateMachineArn,id)
    response = sfn.get_execution_history(executionArn=execution_arn)
    result = json.loads(json.dumps(response,cls=DjangoJSONEncoder)).get('events')
    result = list(filter(lambda d: d.get('type') == 'TaskStateExited', result))
    result = list(filter(lambda d: json.loads(d.get('stateExitedEventDetails').get('output')).get('Status') == 'SUCCEEDED', result))
    names = list(map(lambda d: d.get('stateExitedEventDetails').get('name'),result))
    global newStateMachineArn = newStateMachineArn.get('stateMachineArn')
    newExecutionArn = start_steps(str(id),state_machine_arn=newStateMachineArn)
    return [newStateMachineArn,newExecutionArn]
    # lookup = {'Update Inspection Details':'-inspection_details','Findings':'-findings','Questionaire':'-question'}
    # for name in names:
    #     resume_steps(str(stateId) +lookup[name] )

def delete_state_machine(stateMachineArn):
    # check if go to state machine still exist
    try:
        response = sfn.describe_state_machine(stateMachineArn)
    except StateMachineDoesNotExist:
        return
    except:
        print('The provided Amazon Resource Name (ARN) is invalid.')
    if (response['stateMachineArn'] == stateMachineArn):
        sfn.delete_state_machine(stateMachineArn)    



################################ VIEWS #########################################
# Create your views here.


@never_cache
def index(request):
    inbox = StepStatus.objects.all()
    context = {'inbox': inbox}
    return render(request, 'index.html', context)


@never_cache
def CreateInspectionPage(request):
    create_InspectionForm = Create_InspectionForm()
    context = {'create_InspectionForm': create_InspectionForm}
    return render(request, 'createInspection.html', context)

@never_cache
@require_POST
def CreateInspection(request):
    create_InspectionForm = Create_InspectionForm(request.POST)
    if create_InspectionForm.is_valid():
        print('-------------valid form------------------')
        # create inspection here and update stepstatus
        stepStatus = StepStatus(title='sampleWorkflow',state_machine=state_machine_arn,execution_arn='none')
        # launch stepfunction
        stepStatus.save()
        print('-------------stepstatus Id '+str(stepStatus.id)+'------------------')
        stepStatus.execution_arn = start_steps(str(stepStatus.id))
        stepStatus.save()
        create_InspectionForm = create_InspectionForm.save(commit=False)
        create_InspectionForm.stepStatus = stepStatus
        create_InspectionForm.save()
    return redirect('/')

# update inspection
@never_cache
def get_task(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    stepStatus.current_status = get_current_status(stepStatus.execution_arn)
    stepStatus.assignee = 'OSHD1'
    stepStatus.save()
    update_Inspection = Update_Inspection.objects.get(stepStatus=stepStatus)
    the_form = Update_InspectionForm(instance=update_Inspection)
    
    status_diagram = get_execution_history(stepStatus.execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=stepStatus.state_machine)['definition']
    context = { 'stateId': id, 'create_InspectionForm': the_form, 'status_diagram': status_diagram , 'definition': definition}
    return render(request, 'updateInspection.html', context)

@never_cache
@require_POST
def updateInspection(request):
    update_InspectionForm = Update_InspectionForm(request.POST)
    if update_InspectionForm.is_valid():
        print('-------------inspection------------------')
        stateId = request.POST.dict()['stepStatus']
        # resume stepfunction
        print('resumed inspection_details')
        stepStatus = StepStatus.objects.get(pk=stateId)
        stepStatus.current_status = get_current_status(stepStatus.execution_arn)
        stepStatus.save()
        update_Inspection = Update_Inspection.objects.get(stepStatus=stepStatus)
        update_InspectionForm = Update_InspectionForm(request.POST,instance=update_Inspection)
        update_InspectionForm.save()
        # resume stepfunction
        resume_steps(str(stateId) + '-inspection_details')
    return redirect('/update_inspection/'+stateId)

#####################################################################

# finding
@never_cache
def get_finding(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    execution_arn = get_finding_arn(str(id)+'-findings')
    stepStatus.current_status = get_current_status(stepStatus.execution_arn)
    stepStatus.save()
    the_form = FindingsForm(initial={"stepStatus": stepStatus})
    findings = Findings.objects.filter(stepStatus=stepStatus)
    if (findings.exists()):
        findings = Findings.objects.get(stepStatus=stepStatus)
        the_form = FindingsForm(instance=findings)
    status_diagram = get_execution_history(execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=smArnFromExecutionArn(execution_arn))['definition']
    context = { 'stateId': id, 'finding_form': the_form, 'status_diagram': status_diagram , 'definition': definition}
    return render(request, 'Findings.html', context)

@never_cache
@require_POST
def post_finding(request):
    findingForm = FindingsForm(request.POST)
    if findingForm.is_valid():
        print('-------------finding------------------')
        stateId = request.POST.dict()['stepStatus']
        print('resumed Findings')
        stepStatus = StepStatus.objects.get(pk =stateId)
        stepStatus.current_status = get_current_status(stepStatus.execution_arn)
        stepStatus.save()
        findingForm.save()
        # resume stepfunction
        resume_steps(str(stateId) + '-findings')
        resume_steps(str(stateId) + '-findings',mode="Finding")
    return redirect('/finding/'+stateId)

#####################################################################

# questionaire
@never_cache
def get_questionaire(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    stepStatus.current_status = get_current_status(stepStatus.execution_arn)
    stepStatus.save()
    the_form = Risk_AssessmentForm(initial={"stepStatus": stepStatus})
    risk_Assessment = Risk_Assessment.objects.filter(stepStatus=stepStatus)
    if (risk_Assessment.exists()):
        risk_Assessment = Risk_Assessment.objects.get(stepStatus=stepStatus)
        the_form = Risk_AssessmentForm(instance=risk_Assessment)
    status_diagram = get_execution_history(stepStatus.execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=stepStatus.state_machine)['definition']
    # definition = get_execution_history(execution_arn)
    context = { 'stateId': id, 'RiskAssessmentForm': the_form, 'status_diagram': status_diagram , 'definition': definition}
    return render(request, 'riskAssessment.html', context)

@never_cache
@require_POST
def post_questionaire(request):
    risk_AssessmentForm = Risk_AssessmentForm(request.POST)
    if risk_AssessmentForm.is_valid():
        print('-------------Questionaire------------------')
        stateId = request.POST.dict()['stepStatus']
        print('resumed Questions')
        stepStatus = StepStatus.objects.get(pk =stateId)
        stepStatus.current_status = get_current_status(stepStatus.execution_arn)
        stepStatus.save()
        risk_AssessmentForm.save()
        # resume stepfunction
        resume_steps(str(stateId) + '-question')
    return redirect('/question/'+stateId)

#####################################################################


# enforcement
@never_cache
def get_enforcement(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    stepStatus.current_status = get_current_status(stepStatus.execution_arn)
    stepStatus.save()
    the_form_Warning = WarningsForm(initial={"stepStatus": stepStatus})
    the_form_SWO = SWOForm(initial={"stepStatus": stepStatus})
    swo = SWO.objects.filter(stepStatus=stepStatus)
    warnings = Warnings.objects.filter(stepStatus=stepStatus)
    status_diagram = get_execution_history(stepStatus.execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=stepStatus.state_machine)['definition']
    # definition = get_execution_history(execution_arn)
    if (warnings.exists()):
        warnings = Warnings.objects.get(stepStatus=stepStatus)
        the_form_Warning = WarningsForm(instance=warnings)
    if (swo.exists()):
        swo = SWO.objects.get(stepStatus=stepStatus)
        the_form_SWO = SWOForm(instance=swo)
    context = { 'stateId': id, 'SWOForm': the_form_SWO, 'WarningsForm': the_form_Warning, 'status_diagram': status_diagram , 'definition': definition}
    return render(request, 'Enforcement.html', context)


# Warning
@never_cache
@require_POST
def post_warnings(request):
    stateId = request.POST.dict()['stepStatus']
    warningsForm = WarningsForm(request.POST)
    if warningsForm.is_valid():
        print('-------------Warnings------------------')
        warningsForm.save()
    return redirect('/enforcement/'+stateId)
    
# SWO
@never_cache
@require_POST
def post_SWO(request):
    stateId = request.POST.dict()['stepStatus']
    swoForm = SWOForm(request.POST)
    if swoForm.is_valid():
        print('-------------Stop Watch Order------------------')
        swoForm.save()
    return redirect('/enforcement/'+stateId)

#####################################################################


# vet approve
@never_cache
def get_vetApproveAction(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    stepStatus.current_status = get_current_status(stepStatus.execution_arn)
    stepStatus.save()
    the_form = ApprovalActionForm(initial={"stepStatus": stepStatus})
    approvalAction = ApprovalAction.objects.filter(stepStatus=stepStatus)
    if (approvalAction.exists()):
        approvalAction = ApprovalAction.objects.get(stepStatus=stepStatus)
        the_form = ApprovalActionForm(instance=approvalAction)
    status_diagram = get_execution_history(stepStatus.execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=stepStatus.state_machine)['definition']
    # definition = get_execution_history(execution_arn)
    context = { 'stateId': id, 'ApprovalActionForm': the_form, 'status_diagram': status_diagram , 'definition': definition}
    return render(request, 'approveAction.html', context)

@never_cache
@require_POST
def post_vetApproveAction(request):
    approvalActionForm = ApprovalActionForm(request.POST)
    
    if approvalActionForm.is_valid():
        print('-------------approvalActionForm------------------')
        stateId = request.POST.dict()['stepStatus']
        decision = request.POST.dict()['decision']
        assignee = request.POST.dict()['assignee']
        stepStatus = StepStatus.objects.get(pk=stateId)
        if (stepStatus.current_status == 'Vet/Approve Action' ):
            # resume stepfunction
            approvalAction = ApprovalAction.objects.filter(stepStatus=stepStatus)
            if (approvalAction.exists()):
                approvalAction = ApprovalAction.objects.get(stepStatus=stepStatus)
                approvalActionForm = ApprovalActionForm(request.POST,instance=approvalAction)
            resume_steps('done',decision)
            print('resumed Vet/Approve Action')
            stepStatus = StepStatus.objects.get(pk =stateId)
            stepStatus.current_status = get_current_status(stepStatus.execution_arn)
            stepStatus.assignee = assignee
            stepStatus.save()
            approvalActionForm.save()
        else:
            return HttpResponse('<h1>please to finish the remaining functions highlighted in blue in the diagram</h1><br><a href="/">click here to go back</a>')
    return redirect('/vet_approve/'+stateId)

#####################################################################


# approve officer
@never_cache
def get_Approve(request, id):
    stepStatus = StepStatus.objects.get(pk=id)
    submission = ApprovalAction.objects.filter(stepStatus=stepStatus)
    if (submission.exists() == False):
        return HttpResponse('<h1>please submit for approval </h1><br><a href="/">click here to go back</a>')
    the_form = ApproveOfficerForm(initial={"stepStatus": stepStatus})
    approveOfficer = ApproveOfficer.objects.filter(stepStatus=stepStatus)
    if (approveOfficer.exists()):
        approveOfficer = ApproveOfficer.objects.get(stepStatus=stepStatus)
        the_form = ApproveOfficerForm(instance=approveOfficer)
    status_diagram = get_execution_history(stepStatus.execution_arn)
    definition = sfn.describe_state_machine(stateMachineArn=stepStatus.state_machine)['definition']
    # definition = get_execution_history(execution_arn)
    context = { 'stateId': id, 'ApproveOfficerForm': the_form, 'status_diagram': status_diagram , 'definition': definition}
    return render(request, 'approveOfficer.html', context)

@never_cache
@require_POST
def post_Approve(request):
    approveOfficerForm = ApproveOfficerForm(request.POST)
    stateId = request.POST.dict()['stepStatus']
    if approveOfficerForm.is_valid():
        print('-------------approvalActionForm------------------')
        stepStatus = StepStatus.objects.get(pk=stateId)
        # resume stepfunction
        resume_steps('done')
        print('resumed approve officer Action')
        stepStatus = StepStatus.objects.get(pk =stateId)
        stepStatus.current_status = get_current_status(stepStatus.execution_arn)
        stepStatus.save()
        approveOfficerForm.save()
    return redirect('/approve/'+stateId)

#####################################################################

@never_cache
@require_POST
def post_enforcement(request):
    stateId = request.POST.dict()['stepStatus']
        # resume stepfunction
    resume_steps('done-enforcement')
    print('resumed enforcement')
    stepStatus = StepStatus.objects.get(pk=stateId)
    stepStatus.current_status = get_current_status(stepStatus.execution_arn)
    stepStatus.save()
    return redirect('/enforcement/'+stateId)


@never_cache
@require_POST
def post_resume(request):
    stateId = request.POST.dict()['stepStatus']
    states = request.POST.dict()['states'].split(',')
    stepStatus = StepStatus.objects.get(pk=stateId)
    if stepStatus.current_status == 'Failed':
        reply = parseFailureHistory(stepStatus.execution_arn)
        # create and start first
        updates = resume_failed_steps(stepStatus.execution_arn,tuple(reply)[0],stateId)
        stepStatus.state_machine = updates[0]
        stepStatus.execution_arn = updates[1]
        for state in states:
            # resume those who is successful
            print('-----------------TASK TOKEN--------------------')
            time.sleep(1.4)
            print('task Token',get_final_task_token(str(stateId)+ '-{}'.format(state)))
            resume_steps(str(stateId)+ '-{}'.format(state),mode="Finding")
            stepStatus.current_status = get_current_status(stepStatus.execution_arn)
            stepStatus.save()
    return redirect('/')


# 1) create inspection -> step function triggered
# 2) updateinspection -> Update_Inspection details -> send task success after getting task token via id+inspection_detail
# 3) updateinspection -> findings -> send task success after getting task token via id+Findings
# 4) updateinspection -> enforcement -> send task success after getting task token via id+enforcement
# 5) updateinspection -> questionaire -> send task success after getting task token via id+question
# 6)updateinspection -> send task success with the choices approve/Reassign/Clarification to go to approval stage/ update inspection again
# 7) approval stage -> approve /reject
# 8) launch enforcements -> for each item in the enforcements 
