import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

export interface Person {
  id: number;
  name: string;
  currentDutyTitle: string;
  currentRank: string;
  careerStartDate: string;
  careerEndDate: string;
}

@Injectable({
  providedIn: 'root',
})
export class PersonService {
  private apiUrl = 'http://localhost:8080';

  constructor(private http: HttpClient) {}

  getPersons(): Observable<Person[]> {
    return this.http.get<{ people: Person[] }>(`${this.apiUrl}/person`, { mode: 'cors' }).pipe(
      map(response => response.people)
    );
  }

  getPersonByName(name: string): Observable<Person> {
    return this.http.get<Person>(`${this.apiUrl}/person/${name}`);
  }

  createPerson(name: string): Observable<Person> {
    return this.http.post<Person>(`${this.apiUrl}/person`, JSON.stringify(name), {
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
