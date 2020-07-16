import { Component, OnInit } from '@angular/core';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';
import { StateService } from '../_services/State.service';
import { ActivatedRoute } from '@angular/router';
import { State } from '../_models/State';
import { ApprovalForm } from '../_models/ApprovalForm';


@Component({
  selector: 'app-Approval',
  templateUrl: './Approval.component.html',
  styleUrls: ['./Approval.component.scss']
})
export class ApprovalComponent implements OnInit {

  state: State;
  id: string;
  inspectionForm: FormGroup;
  approvalForm: ApprovalForm;
  LeftReady: string;
  responses = ['good','bad'];
  done= false;
  currentStatusIndex: number;
  steps: string[];
  leftReadyArr: string[];
  
  constructor(
    private fb: FormBuilder,
    private stateService: StateService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
    this.inspectionForm = this.createApprovalForm();
    this.checkApproval(this.id);
  }

  getTask(id: string) {
    return this.stateService.getTask(id).subscribe((res) => {
      this.state = res;
      this.LeftReady = this.state.LeftReady;
      this.state = res;
      this.steps = this.state.workflow.split(',');
      this.currentStatusIndex = this.steps.indexOf(this.state.status);
      this.leftReadyArr = this.LeftReady.split(',');
      console.log(this.state);
    });
  }

  checkApproval(id:string){
    return this.stateService.getApproval(id).subscribe(res =>{
      console.log( res);
      if (res.length > 0){
        this.done = true;
      }
      console.log(this.done);
    });
  }

  createApprovalForm() {
    return this.fb.group(
      {
        clarifications: ['some clarifications',Validators.required],
        approve: ['',Validators.required],
        officerName: ['some officer',Validators.required],
        remarks:['some remarks',Validators.required],
      }
    );
  }

  submitApproval(){
    this.approvalForm = Object.assign({}, this.inspectionForm.value);
    const leftReady = this.LeftReady.split(',');
    const index =  leftReady.indexOf('Vet/Approve Action');
    if (index !== -1) {
      leftReady.splice(index, 1);
    }
    this.LeftReady = leftReady.toString();
    console.log(this.LeftReady);
    const currentIndex = this.steps.indexOf(this.state.status);
    const nextIndex = (currentIndex + 1) % this.steps.length;
    const newState = this.steps[nextIndex];
    if (this.LeftReady === '' && this.done === false){
      return this.stateService.updateState(this.state.id,{ 'status':newState,'LeftReady': this.LeftReady}).subscribe(
        res => {
          this.approvalForm['state'] = this.state.id;
          this.stateService.createApproval(this.approvalForm).subscribe( res => {
          alert('submit' + this.approvalForm.approve);
        });
      });
    } else {
      alert('need complete rest first :' + this.LeftReady+ ' before approving or you already submitted for approval');
    }
  }

}
