# bpm_demo

Step 1 : get task
Step 2: submit task 
 - Db will save the final state of the workflow which is done in the frontend on submit.

resume:
 - Load workflow from DB. 
 - Submit form as usual
 - Db will save the final state of the workflow which is done in the frontend on submit.

idea is to create and update steps only. ignoring the workflow aspects and use angular steppers to handle the workflow part. 

Model:
Form :any form is ok.
Steps: 
- id: number;
- name: string;
- status: string;
- workflow: string;
- assignee: string;
- submitTime: Date;

