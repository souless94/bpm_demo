import { Routes } from '@angular/router';
import { HomeComponent } from './Home/Home.component';
import { FrontComponent } from './front/front.component';

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
    path: '**',
    redirectTo: '',
    pathMatch: 'full',
    component: FrontComponent,
  },

];
