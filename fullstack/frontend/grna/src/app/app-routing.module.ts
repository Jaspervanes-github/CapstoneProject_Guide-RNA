import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'home', loadChildren: () => import('./views/home/home.module').then(m => m.HomeModule)
  },
  {
    path: 'about', loadChildren: () => import('./views/about/about.module').then(m => m.AboutModule)
  },
  {
    path: '*', loadChildren: () => import('./views/home/home.module').then(m => m.HomeModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
