import { Component } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent {
  dnaForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private _httpClient: HttpClient
  ) {
    this.dnaForm = this.fb.group({
      dnaSequence: ['', [Validators.required, Validators.pattern('^[ATCGatcg]*$')]]
    });
  }

  get dnaSequence() {
    return this.dnaForm.get('dnaSequence');
  }

  get isDnaSequenceValid() {
    return this.dnaSequence?.valid;
  }

  submitPrediction() {
    let port = 8000;
    let dna = this.dnaSequence?.value;

    console.log(`http://localhost:${port}}/api/predictions`, `dna: ${dna}`);

    this._httpClient.post<any>(`http://127.0.0.1:8000/api/predictions/`, { dna }).subscribe(data => {
      console.log(data);
    });
  }
}