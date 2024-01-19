import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';


import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { InputComponent } from './input.component';
import { DataTableModule } from '../data-table/data-table.module';

@NgModule({
  declarations: [
    InputComponent,
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    DataTableModule
  ],
  exports: [
    InputComponent
  ]
})
export class InputModule { }
