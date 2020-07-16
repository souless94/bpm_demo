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
import { QuestionaireForm } from '../_models/QuestionaireForm';

@Component({
  selector: 'app-Questionnaire',
  templateUrl: './Questionnaire.component.html',
  styleUrls: ['./Questionnaire.component.scss']
})
export class QuestionnaireComponent implements OnInit {
  state: State;
  id: string;
  inspectionForm: FormGroup;
  questionaireForm: QuestionaireForm;
  LeftReady: string;
  responses = ['good','bad'];
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
    this.inspectionForm = this.createQuestionaireForm();
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

  createQuestionaireForm() {
    return this.fb.group(
      {
        questions: ['How are you?', Validators.required],
        response: ['', Validators.required],
      }
    );
  }

  submitQuestion(){
    this.questionaireForm = Object.assign({}, this.inspectionForm.value);
    const leftReady = this.LeftReady.split(',');
    const index =  leftReady.indexOf('Questionaire');
    if (index !== -1) {
      leftReady.splice(index, 1);
    }
    this.LeftReady = leftReady.toString();
    console.log(this.LeftReady);

    return this.stateService.updateState(this.state.id,{'LeftReady': this.LeftReady}).subscribe(
      res => {
        alert('state Updated');
        this.questionaireForm['state'] = this.state.id;
        this.questionaireForm['responses'] = this.responses.toString();
        this.stateService.createQuestion(this.questionaireForm).subscribe(
          res =>{
            alert('question Created');
          }
        )
      }
    )
  }

}
