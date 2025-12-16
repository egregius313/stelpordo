import { Injectable } from "@angular/core";
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { ErrorMessageService } from "./services/errormessage";
import { catchError, Observable } from "rxjs";

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
    // Implementation of the interceptor would go here
    constructor(private errorMessageService: ErrorMessageService) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(req).pipe(
            catchError((error, caught) => {
                const errorMsg = error.error || 'An unknown error occurred';
                this.errorMessageService.displayError(errorMsg);

                return caught;
            })
        );
    }
}