import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home.component';
import { InputComponent } from 'src/app/components/input/input.component';
import { DataTableComponent } from 'src/app/components/data-table/data-table.component';
import { InputModule } from 'src/app/components/input/input.module';

const routes: Routes = [
  { path: '', component: HomeComponent }
];

@NgModule({
  declarations: [
    HomeComponent,
  ],
  imports: [
    CommonModule,
    InputModule,
    RouterModule.forChild(routes),
  ],
  exports: [RouterModule]
})
export class HomeModule { }
