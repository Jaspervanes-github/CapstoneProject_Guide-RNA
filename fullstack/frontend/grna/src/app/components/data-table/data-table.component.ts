import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.css']
})
export class DataTableComponent implements OnInit {
  @Input() top_10: any[] = [];
  @Input() all_predictions: any[] = [];
  @Input() dna: string = '';

  selectedItem: any = null;
  hoveredItem: any = null;

  constructor() { }

  ngOnInit(): void {
  }

  getNucleotideClass(nucleotide: string): string {
    switch (nucleotide.toUpperCase()) {
      case 'A': return 'a';
      case 'T': return 't';
      case 'C': return 'c';
      case 'G': return 'g';
      default: return '';
    }
  }

  getHoveredItem(index: number): any {
    // Determine which 20-mer is being hovered based on the nucleotide index
    // This assumes the all_predictions array is sorted by the index
    return this.all_predictions.find(item => index >= item.index && index < item.index + 20);
  }

}
