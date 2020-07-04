import { Component, OnInit, ViewChild } from '@angular/core';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';
import { StateService } from '../_services/State.service';
import { ActivatedRoute } from '@angular/router';
import { State } from '../_models/State';
import { ProcessForm } from '../_models/processForm';
import { MatStepper } from '@angular/material/stepper';
@Component({
  selector: 'app-Home',
  templateUrl: './Home.component.html',
  styleUrls: ['./Home.component.css']
})
export class HomeComponent implements OnInit {
  @ViewChild('stepper') stepper: MatStepper;
  state: State;
  FirstProcessForm: FormGroup;
  processForm: ProcessForm;
  id: string;
  steps: string[];
  currentStatusIndex: number;

  constructor(private fb: FormBuilder,private stateService: StateService,private route: ActivatedRoute) { }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
    this.FirstProcessForm = this.createProcessForm();
    this.currentStatusIndex = parseInt(localStorage.getItem('currentStatusIndex'));
  }


  createProcessForm() {
    return this.fb.group(
      {
        name: ['', Validators.required],
        comments: ['', [Validators.required]],
        file_upload : [''],
      }
    );
  }
  
  getTask(id:string){
    return this.stateService.getTask(id).subscribe(
      res => {
        this.state = res;
        this.steps = this.state.workflow.split(',');
        this.currentStatusIndex = this.steps.indexOf(this.state.status);
        localStorage.setItem('currentStatusIndex',this.currentStatusIndex.toString());
      }
    )
  }

  submitForm(step:string){
    this.processForm = Object.assign({}, this.FirstProcessForm.value);
    const currentIndex = this.steps.indexOf(step);
    const nextIndex = (currentIndex + 1) % this.steps.length;
    const newState = this.steps[nextIndex];
    console.log(newState);
    this.stateService.submitForm(this.processForm).subscribe(
      (res) =>{
        this.stateService.updateState(this.id,newState).subscribe();
      }
    )
  }



}
