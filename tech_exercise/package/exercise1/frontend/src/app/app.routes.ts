import { Routes } from '@angular/router';
import { PersonList } from './components/person-list/person-list';
import { Person } from './components/person/person';
import { CreatePerson } from './components/createperson/createperson';

export const routes: Routes = [
    { path: 'people', component: PersonList },
    { path: 'person/:name', component: Person },
    { path: 'createperson', component: CreatePerson },
    { path: '', redirectTo: '/people', pathMatch: 'full' },
];
