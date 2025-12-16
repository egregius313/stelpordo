import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { PersonService } from '../../services/person';
import { Field, form } from '@angular/forms/signals';

@Component({
  selector: 'app-createperson',
  imports: [FormsModule, RouterModule, Field],
  templateUrl: './createperson.html',
  styleUrl: './createperson.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CreatePerson {
  name = signal({
    name: ''
  });
  personForm = form(this.name);

  constructor(private router: Router, private personService: PersonService) {}

  protected onSubmit(): void {
    this.personService.createPerson(this.name().name).subscribe({
      next: (data) => {
        console.log('Person created:', data);
        this.router.navigate(['/person', this.name().name]);
      },
      error: (error) => {
        console.error('Error creating person:', error);
      },
    });
  }
}
