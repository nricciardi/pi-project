import { Injectable } from '@angular/core';
import { EntityApiService } from '../entity-api.service';
import { UserModel } from 'src/app/model/entity/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService extends EntityApiService<UserModel> {
  override ALL: string = "user_all";
  override FIND: string = "user_find";
  override DELETE_BY_ID: string = "user_delete_by_id";
}
