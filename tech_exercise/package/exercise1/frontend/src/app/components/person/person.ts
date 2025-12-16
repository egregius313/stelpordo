import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterModule, Router } from '@angular/router';
import { Person as PersonModel, PersonService } from '../../services/person';

@Component({
  selector: 'app-person',
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './person.html',
  styleUrl: './person.css',
})
export class Person {
  person = signal<PersonModel>({ name: '', currentDutyTitle: '', currentRank: '', id: 0, careerStartDate: '', careerEndDate: '' });

  constructor(private route: ActivatedRoute, private router: Router, private service: PersonService) {}
  
  ngOnInit(): void {
    // Load person details based on route parameter (to be implemented)
    const name = this.route.snapshot.paramMap.get('name');
    if (name) {
      this.loadPerson(name);
    }
  }

  private loadPerson(name: string): void {
    this.service.getPersonByName(name).subscribe({
      next: (data: PersonModel) => {
        console.log(data);
        this.person.set(data);
      },
      error: (error) => {
        console.error('Error fetching person:', error);
      },
    });
  }

  private createAstronautDuty(): void {
    
  }
}
