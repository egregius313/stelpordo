import { Component, signal } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';

import { PersonList } from './components/person-list/person-list';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, PersonList, RouterModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
