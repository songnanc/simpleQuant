import { BrowserModule } from '@angular/platform-browser';
import { ChartsModule } from 'ng2-charts';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { HttpModule }    from '@angular/http';
import { ButtonsModule, ModalModule, PopoverModule } from 'ng2-bootstrap';
import { CodemirrorModule } from 'ng2-codemirror';
import { NgModule }      from '@angular/core';

import { AppComponent }  from './app.component';
import { AppRoutingModule }     from './app-routing.module';
import { DynamicFormComponent }         from './dynamic-form.component';
import { DynamicFormQuestionComponent } from './dynamic-form-question.component';
import { LineChartComponent } from './line-chart';
import { QuestionService } from './question.service';
import { StrategyDetailComponent } from './strategy-detail.component';
import { StrategiesComponent }     from './strategies.component';
import { StrategyService }         from './strategy.service';
import { TransitionDetailComponent } from './transition-detail.component';
import { TransitionsComponent } from './transitions.component';
import { TransitionService } from './transition.service';



@NgModule({
  imports: [
      AppRoutingModule,
      BrowserModule,
      FormsModule,
      HttpModule,
      ButtonsModule.forRoot(),
      ModalModule.forRoot(),
      PopoverModule.forRoot(),
      CodemirrorModule,
      ChartsModule,
      ReactiveFormsModule
  ],
  declarations: [
      AppComponent,
      DynamicFormComponent,
      DynamicFormQuestionComponent,
      TransitionDetailComponent,
      StrategyDetailComponent,
      StrategiesComponent,
      LineChartComponent,
      TransitionsComponent
  ],
  providers: [
      QuestionService,
      StrategyService,
      TransitionService,
      QuestionService
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
