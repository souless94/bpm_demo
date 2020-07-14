import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { State } from '../_models/State';
import { CreateInspectionForm } from '../_models/CreateInspectionForm';

@Injectable()
export class StateService {
    baseUrl = environment.apiUrl;

constructor(private http: HttpClient) { }

getTasks(status: string) {
    let params = new HttpParams();
    params = params.append('status', status);
    return this.http.get(this.baseUrl + 'state/', {params});
}

startTask(id: string,assignee: string,status:string){
    const payload = {
        status,
        assignee
    }
    return this.http.patch(this.baseUrl + 'state/' + id +'/',payload );
}

updateState(id: string, state: string){
    return this.http.patch(this.baseUrl + 'state/' + id +'/',{"status" : state});
}

getTask(id: string){
    return this.http.get<State>(this.baseUrl + 'state/' + id);
}

createTask(state:State){
    return this.http.post(this.baseUrl + 'state/', state);
}

createInspection(createInspectionForm: CreateInspectionForm){
    return this.http.post(this.baseUrl + 'createInspectionForm/', createInspectionForm);
}

}
