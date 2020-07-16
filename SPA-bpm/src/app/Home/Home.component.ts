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
import { CreateInspectionForm } from '../_models/CreateInspectionForm';

@Component({
  selector: 'app-Home',
  templateUrl: './Home.component.html',
  styleUrls: ['./Home.component.css'],
})
export class HomeComponent implements OnInit {
  state: State;
  id: string;
  inspectionForm: FormGroup;
  createInspectionForm: CreateInspectionForm;
  LeftReady: string;
  inspectionFormId: string;
  currentStatusIndex: number;
  steps: string[];
  leftReadyArr: string[];

  constructor(
    private fb: FormBuilder,
    private stateService: StateService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.updateInspectionForm();
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
    this.getInspectionForm(this.id);
  }

  getTask(id: string) {
    return this.stateService.getTask(id).subscribe((res) => {
      this.state = res;
      console.log(this.state);
      this.LeftReady = this.state.LeftReady;
      this.steps = this.state.workflow.split(',');
      this.currentStatusIndex = this.steps.indexOf(this.state.status);
      this.leftReadyArr = this.LeftReady.split(',');
    });
  }
  getInspectionForm(id: string) {
    return this.stateService.getInspectionForm(id).subscribe((res) => {
      this.createInspectionForm = res[0];
      this.inspectionFormId =this.createInspectionForm.id;
      this.inspectionForm.setValue({
        inspectionCategory: this.createInspectionForm.inspectionCategory,
        inspectionType: this.createInspectionForm.inspectionType,
        reference: this.createInspectionForm.reference,
        referenceNo: this.createInspectionForm.referenceNo,
        TeamDetails: this.createInspectionForm.TeamDetails,
        arrivalDate: this.createInspectionForm.arrivalDate,
        workPlaceNo: this.createInspectionForm.workPlaceNo
      });
      console.log(res);
    });
  }

  updateInspectionForm() {
    this.inspectionForm = this.fb.group({
      inspectionCategory: ['', Validators.required],
      inspectionType: ['', Validators.required],
      reference: [''],
      referenceNo: [''],
      TeamDetails: ['OSHD1', Validators.required],
      arrivalDate: ['2020-07-14'],
      workPlaceNo: ['', Validators.required],
    });
  }

  updateInspection(){
    this.createInspectionForm = Object.assign({}, this.inspectionForm.value);
    const leftReady = this.LeftReady.split(',');
    const index =  leftReady.indexOf('Inspection details')
    if (index !== -1) {
      leftReady.splice(index, 1);
    }
    this.LeftReady = leftReady.toString();
    console.log(this.LeftReady);

    this.stateService.updateState(this.state.id,{'LeftReady': this.LeftReady}).subscribe(
      res => {
        alert('state Updated');
        console.log(this.inspectionFormId);
        this.stateService.updateInspection(this.inspectionFormId,this.createInspectionForm).subscribe(
          res => {
            alert('form updated');
          }
        )
      }
    );
  }
  
}
