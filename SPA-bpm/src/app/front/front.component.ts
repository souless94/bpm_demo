import { Component, OnInit } from '@angular/core';
import { StateService } from '../_services/State.service';
import { State } from '../_models/State';
import {
  FormGroup,
  FormControl,
  FormBuilder,
  Validators,
} from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-front',
  templateUrl: './front.component.html',
  styleUrls: ['./front.component.css']
})
export class FrontComponent implements OnInit {
  tasks: State[];
  newTask: State;
  taskForm: FormGroup;

  constructor(private fb: FormBuilder , private stateService: StateService, private router: Router) { }

  ngOnInit() {
    this.loadTasks();
    this.taskForm = this.createTaskForm();
  }

  loadTasks(){
    return this.stateService.getTasks('Not Started').subscribe(
      (res: State[]) => {
        this.tasks = res;
        console.log(this.tasks);
      }
    )
  }

  startTask(id: string ){
    console.log('clicked ' + id);
    return this.stateService.startTask(id,'OSHD1').subscribe(
      res => {
        console.log('nagivate ? ')
        this.router.navigate(['/task/' + id ]);
      }
    );
  }

  createTask(){
    this.newTask = Object.assign({}, this.taskForm.value);
    return this.stateService.createTask(this.newTask).subscribe(
      res =>{
        alert('created task');
        this.router.navigate(['']);
      }
    );
  }

  createTaskForm() {
    return this.fb.group(
      {
        name: ['', Validators.required],
        status: ['Not Started', Validators.required],
        workflow: ['Start,Verify,Approve', Validators.required],
        assignee: ['None', Validators.required],
      }
    );
  }

}
