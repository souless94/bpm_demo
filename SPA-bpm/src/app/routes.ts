import { Routes } from '@angular/router';
import { HomeComponent } from './Home/Home.component';
import { FrontComponent } from './front/front.component';
import { CreateInspectionComponent } from './CreateInspection/CreateInspection.component';

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
    path: '**',
    redirectTo: '',
    pathMatch: 'full',
    component: FrontComponent,
  },

];
