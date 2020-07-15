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
import { WarningsForm } from '../_models/WarningsForm';
import { SWOForm } from '../_models/SWOForm';

@Component({
  selector: 'app-Enforcement',
  templateUrl: './Enforcement.component.html',
  styleUrls: ['./Enforcement.component.scss']
})
export class EnforcementComponent implements OnInit {

  state: State;
  id: string;
  inspectionWarningForm: FormGroup;
  inspectionSWOForm: FormGroup;
  warningsForm: WarningsForm;
  SWOForm: SWOForm;
  LeftReady: string;
  responses = ['good','bad'];
  
  constructor(
    private fb: FormBuilder,
    private stateService: StateService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
    this.inspectionWarningForm = this.createWarningForm();
    this.inspectionSWOForm = this.createSWOForm();
  }

  getTask(id: string) {
    return this.stateService.getTask(id).subscribe((res) => {
      this.state = res;
      this.LeftReady = this.state.LeftReady;
      console.log(this.state);
    });
  }
  createSWOForm() {
    return this.fb.group(
      {
        orderNo: ['some OrderNo',Validators.required],
        proposal: ['some proposal',Validators.required],
        description: ['some Description',Validators.required],
      }
    );
  }

  createWarningForm() {
    return this.fb.group(
      {
        enforcementAction: ['some Action',Validators.required],
        law: ['some law',Validators.required],
        act: ['some act',Validators.required],
        description: ['some Description',Validators.required],
      }
    );
  }

  submitWarning(){
    this.warningsForm = Object.assign({}, this.inspectionWarningForm.value);
    this.warningsForm['state'] = this.state.id;
    this.stateService.createWarning(this.warningsForm).subscribe(
          res =>{
            alert('warning Created');
          }
        );
  }

  submitSWO(){
    this.SWOForm = Object.assign({}, this.inspectionSWOForm.value);
    this.SWOForm['state'] = this.state.id;
    this.stateService.createSWO(this.SWOForm).subscribe(
          res =>{
            alert('SWO Created');
          }
        );
  }

  goToApproval(){
    const leftReady = this.LeftReady.split(',');
    const index =  leftReady.indexOf('Enforcement');
    if (index !== -1) {
      leftReady.splice(index, 1);
    }
    this.LeftReady = leftReady.toString();
    console.log(this.LeftReady);

    return this.stateService.updateState(this.state.id,{'LeftReady': this.LeftReady}).subscribe(
      res => {
        alert('state Updated');}
    );
  }
}
