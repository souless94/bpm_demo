import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { ProcessForm } from '../_models/processForm';
import { environment } from 'src/environments/environment';
import { State } from '../_models/State';

@Injectable()
export class StateService {
    baseUrl = environment.apiUrl;

constructor(private http: HttpClient) { }

getTasks(status: string) {
    let params = new HttpParams();
    params = params.append('status', status);
    return this.http.get(this.baseUrl + 'State/',{params});
}

submitForm(processForm: ProcessForm){
    return this.http.post(this.baseUrl + 'processForm/', processForm);
}

updateState(id: string, state: State){
    return this.http.patch(this.baseUrl + 'State/' + id, state);
}

getState(id: string){
    return this.http.get<State>(this.baseUrl + 'State/' + id);
}

}
