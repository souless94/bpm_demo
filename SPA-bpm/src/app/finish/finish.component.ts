import { Component, OnInit } from '@angular/core';
import { StateService } from '../_services/State.service';
import { State } from '../_models/State';
import { ActivatedRoute } from '@angular/router';
import { ApprovalForm } from '../_models/ApprovalForm';
import { Router } from '@angular/router';

@Component({
  selector: 'app-finish',
  templateUrl: './finish.component.html',
  styleUrls: ['./finish.component.css']
})
export class FinishComponent implements OnInit {
  state: State;
  id: string;
  approvalForm: ApprovalForm;

  constructor(
   
    private stateService: StateService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getTask(this.id);
  }

  getTask(id: string) {
    return this.stateService.getTask(id).subscribe((res) => {

      this.state = res;
      this.stateService.getApproval(id).subscribe(
        res => {
          this.approvalForm = res[0];
        }
      );
      console.log(this.state);
    });
  }

  finishTask(id: string ){
    return this.stateService.updateState(id,{'done':true,'status':'Approved'}).subscribe(
      res => {
        console.log('nagivate ? ')
        this.router.navigate(['/']);
      }
    );
  }

  rejectTask(id: string ){
    return this.stateService.updateState(id,{'done':true,'status':'Rejected'}).subscribe(
      res => {
        console.log('nagivate ? ')
        this.router.navigate(['/']);
      }
    );
  }

}
