import { Routes } from '@angular/router';
import { PersonList } from './components/person-list/person-list';
import { Person } from './components/person/person';

export const routes: Routes = [
    { path: 'people', component: PersonList },
    { path: 'person/:name', component: Person },
    { path: '', redirectTo: '/people', pathMatch: 'full' },
];
