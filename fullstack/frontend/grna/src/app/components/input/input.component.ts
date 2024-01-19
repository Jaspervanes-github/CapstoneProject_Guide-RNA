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
  loading: boolean = false;
  result: any;

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
    console.log(this.dnaSequence?.value);

    let url: string = "http://127.0.0.1:8000/api/predictions/";
    let dna = this.dnaSequence?.value;

    this.loading = true;

    this._httpClient
        .post<any>(url, { dna })
        .subscribe(data => {
          this.loading = false;
          this.result = data;
        });
  }
}