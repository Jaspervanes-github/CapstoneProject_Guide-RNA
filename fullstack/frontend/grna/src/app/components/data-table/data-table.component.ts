import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.css']
})
export class DataTableComponent implements OnInit, OnChanges {
  @Input() top_10: any[] = [];
  @Input() all_predictions: any[] = [];
  @Input() dna: string = '';

  selectedItem: any = null;
  hoveredItem: any = null;

  currentPage: number = 1;
  itemsPerPage: number = 20;
  pagedItems: any[] = [];

  ceil = Math.ceil;

  constructor() { }

  ngOnInit(): void {
    this.setPage(1);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['dna']) {
      this.reset();
    }
  }

  reset(): void {
    this.currentPage = 1;
    this.selectedItem = null;
    this.hoveredItem = null;
    this.setPage(this.currentPage);
  }

  setPage(page: number): void {
    this.currentPage = page;
    const start = (this.currentPage - 1) * this.itemsPerPage;
    const end = start + this.itemsPerPage;
    this.pagedItems = this.all_predictions.slice(start, end);
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
    return this.all_predictions.find(item => index >= item.index && index < item.index + 20);
  }
}