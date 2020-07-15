/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';

import { EnforcementComponent } from './Enforcement.component';

describe('EnforcementComponent', () => {
  let component: EnforcementComponent;
  let fixture: ComponentFixture<EnforcementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EnforcementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EnforcementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
