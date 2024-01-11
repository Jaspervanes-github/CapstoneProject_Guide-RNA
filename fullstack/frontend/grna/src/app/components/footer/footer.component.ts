import { ChangeDetectorRef, Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {

  people = [
    {
      name: 'Jasper van Es',
      studentnumber: 'x',
      image: 'https://avatars.githubusercontent.com/u/57483435?v=4',
      imageLoaded: false
    },
    {
      name: 'Martijn van Zelst',
      studentnumber: 'x',
      image: 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2FD4E03AQFWBTin2OQYmw%2Fprofile-displayphoto-shrink_800_800%2F0%2F1670253191138%3Fe%3D2147483647%26v%3Dbeta%26t%3DjAH88WaYhAC84m-ehk-Gyq0ODZ_sYBtW48hTRi1r4Sc&f=1&nofb=1&ipt=64c6571687a8268b24798c70169fe61469e40ac194c1981b1ad217a14f0d945a&ipo=im,ages',
      imageLoaded: false
    },
    {
      name: 'Robin Janse',
      studentnumber: 'x',
      image: 'https://avatars.githubusercontent.com/u/58508244?v=4',
      imageLoaded: false
    },
    {
      name: 'Stan Barkmeijer',
      studentnumber: '2153846',
      image: 'https://avatars.githubusercontent.com/u/31732012?v=4',
      imageLoaded: false
    }
  ]

  constructor(
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
  }

  onImageLoad(person: any): void {
    person.imageLoaded = true;
    this.cdr.detectChanges();
  }

}
