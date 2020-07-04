/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { ProcessFormService } from './ProcessForm.service';

describe('Service: ProcessForm', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ProcessFormService]
    });
  });

  it('should ...', inject([ProcessFormService], (service: ProcessFormService) => {
    expect(service).toBeTruthy();
  }));
});
