import { RoleModel } from "./role.model";

export interface UserModel {
  id: number;
  username: string;
  name: string | null;
  surname: string | null;
  email: string;
  avatar_hex_color: string;
  // password: string;    hidden
  role_id: number;
  role: RoleModel | null;
}
