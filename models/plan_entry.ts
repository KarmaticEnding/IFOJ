import * as TypeORM from 'typeorm';
import Model from './common';
@TypeORM.Entity()
export default class PlanEntry extends Model {
  @TypeORM.PrimaryColumn({type:'integer'}) user_id: number;
  @TypeORM.PrimaryColumn({type:'varchar',length:10}) date: string;
  @TypeORM.PrimaryColumn({type:'varchar',length:8}) kind: string;
  @TypeORM.Column({type:'text'}) description: string;
  @TypeORM.Column({type:'text'}) completion: string;
  @TypeORM.Column({type:'text'}) comment: string;
  @TypeORM.Column({type:'integer'}) version: number;
  @TypeORM.Column({type:'varchar',length:32}) saved_at: string;
}
