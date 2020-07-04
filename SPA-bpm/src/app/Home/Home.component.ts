import { Component, OnInit } from '@angular/core';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';
import { StateService } from '../_services/State.service';
@Component({
  selector: 'app-Home',
  templateUrl: './Home.component.html',
  styleUrls: ['./Home.component.css']
})
export class HomeComponent implements OnInit {
  FirstProcessForm: FormGroup;
  SecondProcessForm: FormGroup;
  id = localStorage.getItem('id');

  constructor(private fb: FormBuilder,private stateService: StateService) { }

  ngOnInit() {
    this.FirstProcessForm = this.createProcessForm();
    this.SecondProcessForm = this.createProcessForm();
  }

  createProcessForm() {
    return this.fb.group(
      {
        name: ['', Validators.required],
        message: ['', [Validators.required, Validators.min(0)]],
        file_upload : [''],
      }
    );
  }
  
  getTask(id:string){

  }




}
