import { TestBed } from '@angular/core/testing';

import { Errormessage } from './errormessage';

describe('Errormessage', () => {
  let service: Errormessage;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Errormessage);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
