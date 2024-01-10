import { Component } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent {
  dnaForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.dnaForm = this.fb.group({
      dnaSequence: ['', [Validators.required, Validators.pattern('^[ATCGatcg]*$')]]
    });
  }
}