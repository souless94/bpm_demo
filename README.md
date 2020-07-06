# bpm_demo with steps

Step 1 : get task
Step 2: submit task 
 - Db will save form
 - Step function will run execute task which pause the workflow by using a callback. Then the lambda function will save the tasktoken in a db and id of submission.
 -
resume:
 - get history from step function and find out which step it is in.
 - Submit form as usual

expiry:
 - create a new state machine and then key in the previous inputs
 - set the form to the new state machine and new execution id
 - need do clean up once a year.

idea is to use step functions, lambda, database to store the task token in each state. 

Model:
Form :form with execution id, submission id and the statemachine

