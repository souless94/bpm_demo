import { Component, OnInit } from '@angular/core';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  FirstProcessForm: FormGroup;
  SecondProcessForm: FormGroup;


  constructor(private fb: FormBuilder) { }

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

}
