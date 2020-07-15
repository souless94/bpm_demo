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

@Component({
  selector: 'app-findings',
  templateUrl: './findings.component.html',
  styleUrls: ['./findings.component.scss']
})
export class FindingsComponent implements OnInit {
  state: State;
  id: string;
  inspectionForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private stateService: StateService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    // this.updateInspectionForm();
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
    // this.getInspectionForm(this.id);
  }

  getTask(id: string) {
    return this.stateService.getTask(id).subscribe((res) => {
      this.state = res;
      console.log(this.state);
    });
  }
  // getInspectionForm(id: string) {
  //   return this.stateService.getInspectionForm(id).subscribe((res) => {
  //     this.createInspectionForm = res[0];
  //     this.inspectionForm.setValue({
  //       inspectionCategory: this.createInspectionForm.inspectionCategory,
  //       inspectionType: this.createInspectionForm.inspectionType,
  //       reference: this.createInspectionForm.reference,
  //       referenceNo: this.createInspectionForm.referenceNo,
  //       TeamDetails: this.createInspectionForm.TeamDetails,
  //       arrivalDate: this.createInspectionForm.arrivalDate,
  //       workPlaceNo: this.createInspectionForm.workPlaceNo
  //     });
  //     console.log(res);
  //   });
  // }

  // updateInspectionForm() {
  //   this.inspectionForm = this.fb.group({
  //     inspectionCategory: ['', Validators.required],
  //     inspectionType: ['', Validators.required],
  //     reference: [''],
  //     referenceNo: [''],
  //     TeamDetails: ['OSHD1', Validators.required],
  //     arrivalDate: ['2020-07-14'],
  //     workPlaceNo: ['', Validators.required],
  //   });
  // }

}


