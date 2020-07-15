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
    return this.http.get(this.baseUrl + 'state/');
}

startTask(id: string,assignee: string,status:string, LeftReady: string){
    const payload = {
        status,
        assignee,
        LeftReady
    }
    return this.http.patch(this.baseUrl + 'state/' + id +'/',payload );
}

updateState(id: string, params:any){
    return this.http.patch(this.baseUrl + 'state/' + id +'/',params);
}

getTask(id: string){
    return this.http.get<State>(this.baseUrl + 'state/' + id);
}

getInspectionForm(id: string){
    let params = new HttpParams();
    params = params.append('state',id);
    return this.http.get<CreateInspectionForm[]>(this.baseUrl + 'createInspectionForm/', {params});
}

createTask(state:State){
    return this.http.post(this.baseUrl + 'state/', state);
}

createInspection(createInspectionForm: CreateInspectionForm){
    return this.http.post(this.baseUrl + 'createInspectionForm/', createInspectionForm);
}


}
