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
  id: string;
  steps: string[];
  currentStatusIndex: number;

  constructor(private fb: FormBuilder,private stateService: StateService,private route: ActivatedRoute) { }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
  }

  getTask(id:string){
    return this.stateService.getTask(id).subscribe(
      res => {
        this.state = res;
      }
    )
  }




}
