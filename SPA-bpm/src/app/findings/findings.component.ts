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
import { FindingsForm } from '../_models/FindingsForm';

@Component({
  selector: 'app-findings',
  templateUrl: './findings.component.html',
  styleUrls: ['./findings.component.scss']
})
export class FindingsComponent implements OnInit {
  state: State;
  id: string;
  inspectionForm: FormGroup;
  findingForm: FindingsForm;
  LeftReady: string;
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
    this.inspectionForm = this.createFindingForm();
  }

  getTask(id: string) {
    return this.stateService.getTask(id).subscribe((res) => {
      this.state = res;
      this.LeftReady = this.state.LeftReady;
      this.steps = this.state.workflow.split(',');
      this.currentStatusIndex = this.steps.indexOf(this.state.status);
      this.leftReadyArr = this.LeftReady.split(',');
      console.log(this.state);
    });
  }
  createFindingForm() {
    return this.fb.group(
      {
        description: ['', Validators.required],
      }
    );
  }

  createFinding(){
    this.findingForm = Object.assign({}, this.inspectionForm.value);
    const leftReady = this.LeftReady.split(',');
    const index =  leftReady.indexOf('Findings');
    if (index !== -1) {
      leftReady.splice(index, 1);
    }
    this.LeftReady = leftReady.toString();
    console.log(this.LeftReady);

    return this.stateService.updateState(this.state.id,{'LeftReady': this.LeftReady}).subscribe(
      res => {
        alert('state Updated');
        this.findingForm['state'] = this.state.id;
        this.stateService.createFinding(this.findingForm).subscribe(
          res =>{
            alert('finding Created');
          }
        )
      }
    )

  }




}


