import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PersonList } from './components/person-list/person-list';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, PersonList],
    templateUrl: './app.component.html',
})
export class AppComponent {
}