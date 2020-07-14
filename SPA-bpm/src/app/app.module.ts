import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { HomeComponent } from './Home/Home.component';
import { FrontComponent } from './front/front.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { appRoutes } from './routes';

import { MatStepperModule } from '@angular/material/stepper';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatButtonModule} from '@angular/material/button';
import {MatNativeDateModule} from '@angular/material/core';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { MatTimepickerModule } from 'mat-timepicker';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import {MatCardModule} from '@angular/material/card';
import {MatSelectModule} from '@angular/material/select';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import {StateService} from '../app/_services/State.service';
import {ProcessFormService} from '../app/_services/ProcessForm.service';
import { CreateInspectionComponent } from './CreateInspection/CreateInspection.component';


@NgModule({
   declarations: [
      AppComponent,
      HomeComponent,
      FrontComponent,
      CreateInspectionComponent
   ],
   imports: [
      BrowserModule,
      HttpClientModule,
      BrowserAnimationsModule,
      FormsModule,
      ReactiveFormsModule,
      MatStepperModule,
      MatButtonModule,
      MatNativeDateModule,
      MatDatepickerModule,
      MatTimepickerModule,
      MatFormFieldModule,
      MatInputModule,
      MatIconModule,
      MatCardModule,
      MatSelectModule,
      RouterModule.forRoot(appRoutes)
   ],
   providers: [
      StateService,
      ProcessFormService
   ],
   bootstrap: [
      AppComponent
   ]
})
export class AppModule { }
