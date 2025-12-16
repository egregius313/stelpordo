import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { PersonService } from '../../services/person';
import { RouterModule } from '@angular/router';

interface Person {
  name: string;
  currentDutyTitle: string;
  currentRank: string;
}

@Component({
  selector: 'person-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './person-list.html',
  styleUrl: './person-list.css',
})
export class PersonList {
  persons = signal<Person[]>([]);

  constructor(private personService: PersonService) {}
  
  ngOnInit(): void {
    this.loadPersons();
  }

  private loadPersons(): void {
    this.personService.getPersons().subscribe({
      next: (data: Person[]) => {
        console.log(data);
        this.persons.set(data);
      },
      error: (error) => {
        console.error('Error fetching persons:', error);
      },
    });
  }
}
