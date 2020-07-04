import { Component, OnInit } from '@angular/core';
import { StateService } from '../_services/State.service';
import { State } from '../_models/State';

@Component({
  selector: 'app-front',
  templateUrl: './front.component.html',
  styleUrls: ['./front.component.css']
})
export class FrontComponent implements OnInit {
  tasks: State[];

  constructor(private stateService: StateService) { }

  ngOnInit() {
    this.loadTasks();
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
      (res) =>{
        localStorage.setItem('id',id);
      }
    );
  }

}
