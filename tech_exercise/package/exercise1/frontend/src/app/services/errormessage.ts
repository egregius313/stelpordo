import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ErrorMessageService {
  errorMessage: string = '';
  isErrorMessageVisible: boolean = false;

  displayError(message: string): void {
    this.errorMessage = message;
    this.isErrorMessageVisible = true;
  }

  hideErrorMessage(): void {
    this.isErrorMessageVisible = false;
    this.errorMessage = '';
  }
}
