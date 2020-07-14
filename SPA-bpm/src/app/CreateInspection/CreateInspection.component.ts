import { Component, OnInit } from '@angular/core';
import { StateService } from '../_services/State.service';
import {State} from '../_models/State';
import { Router } from '@angular/router';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';
import { CreateInspectionForm } from '../_models/CreateInspectionForm';

@Component({
  selector: 'app-CreateInspection',
  templateUrl: './CreateInspection.component.html',
  styleUrls: ['./CreateInspection.component.scss']
})
export class CreateInspectionComponent implements OnInit {
  inspectionForm: FormGroup;
  newInspection: CreateInspectionForm;
  isNext =false;
  workplace = false;
  task: any;

  inspectionCategories = ['engagement','general','program','Others'];
  inspectionTypes = ['unplanned','Complaint'];
  references = ['case management','feedback'];

  constructor(private fb: FormBuilder , private stateService: StateService, private router: Router) { }

  ngOnInit() {
    this.inspectionForm = this.createInspectionForm();
  }

  createInspectionForm() {
    return this.fb.group(
      {
        inspectionCategory: ['', Validators.required],
        inspectionType: ['', Validators.required],
        reference: [''],
        referenceNo: [''],
        TeamDetails: ['OSHD1',Validators.required],
        arrivalDate: ['2020-07-14'],
        workPlaceNo: ['',Validators.required]
      }
    );
  }

  createInspection(){
    this.newInspection = Object.assign({}, this.inspectionForm.value);
    console.log(this.newInspection);
    this.task = Object.assign({},{
      name: 'workflow 1',
      status: 'Create Inspection',
      workflow: 'Create Inspection, Update Inspection , Vet/Approve Inspection',
      Assignee: 'OSHD1',
      isReady: false,
      LeftReady: 'Update Inspection Detail, '
    });
    return this.stateService.createTask(this.task).subscribe(
      res => {
        alert('created task');
        this.stateService.createInspection(this.newInspection).subscribe(
          res =>{
            alert('created inspection');
          }
        );
      }
    );
  }

  nothing(){
    console.log('nothing');
  }

  nextIt(){
    this.isNext=true;
  }

  search(){
    this.workplace=true;
  }

}
