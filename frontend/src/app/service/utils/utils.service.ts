import { Injectable } from '@angular/core';
import { UserModel } from 'src/app/model/entity/user.model';
import { AuthService } from '../api/auth/auth.service';
import { ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor(private authService: AuthService) {}

  getAvatarText(user: UserModel): string {
    if(user?.name && user?.surname) {
      return user.name.substring(0, 1) + user.surname.substring(0, 1)
    } else {
      return user ? user.username.substring(0, 2) : "-";
    }
  }

  canDelete(authorId: number): boolean {
    let loggedUser = this.authService.loggedUser;

    if(!loggedUser) {
      return false;
    }

    if(!!loggedUser.role?.permission_delete_all)
      return true;

    if(authorId == loggedUser.id && !!loggedUser.role?.permission_delete_own)
      return true;


    return false;

  }

  canModify(authorId: number): boolean {
    let loggedUser = this.authService.loggedUser;

    if(!loggedUser) {
      return false;
    }

    if(!!loggedUser.role?.permission_edit_all)
      return true;

    if(authorId == loggedUser.id && !!loggedUser.role?.permission_edit_own)
      return true;


    return false;

  }

  createPasswordStrengthValidator(minLenght: number): ValidatorFn {
    return (control:AbstractControl) : ValidationErrors | null => {

        const value = control.value;

        if (!value) {
            return null;
        }

        const hasUpperCase = /[A-Z]+/.test(value);

        const hasLowerCase = /[a-z]+/.test(value);

        const hasNumeric = /[0-9]+/.test(value);

        const hasLenght = value.length >= minLenght;

        const passwordValid = hasUpperCase && hasLowerCase && hasNumeric && hasLenght;

        return !passwordValid ? {passwordStrength:true}: null;
    }
  }
}
