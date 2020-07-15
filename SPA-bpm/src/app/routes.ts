import { Routes } from '@angular/router';
import { HomeComponent } from './Home/Home.component';
import { FrontComponent } from './front/front.component';
import { CreateInspectionComponent } from './CreateInspection/CreateInspection.component';
import { FindingsComponent } from './findings/findings.component';
import { EnforcementComponent } from './Enforcement/Enforcement.component';
import { QuestionnaireComponent } from './Questionnaire/Questionnaire.component';
import { ApprovalComponent } from './Approval/Approval.component';

export const appRoutes: Routes = [
  {
    path: 'task/:id',
    component: HomeComponent,
  },
  {
    path: '',
    redirectTo: '',
    pathMatch: 'full',
    component: FrontComponent,
  },
  {
    path: 'create',
    component: CreateInspectionComponent,
  },
  {
    path: 'findings',
    component: FindingsComponent,
  },
  {
    path: 'Questionaire',
    component: QuestionnaireComponent,
  },
  {
    path: 'enforcement',
    component: EnforcementComponent,
  },
  {
    path: 'approval',
    component: ApprovalComponent,
  },
  {
    path: '**',
    redirectTo: '',
    pathMatch: 'full',
    component: FrontComponent,
  },

];
