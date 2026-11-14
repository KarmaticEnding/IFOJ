import * as TypeORM from 'typeorm';
import Model from './common';
@TypeORM.Entity()
export default class ReviewTable extends Model {
  @TypeORM.PrimaryColumn({type:'integer'}) contest_id: number;
  @TypeORM.PrimaryColumn({type:'integer'}) user_id: number;
  @TypeORM.Column({type:'json'}) data: any;
  @TypeORM.Column({type:'integer'}) version: number;
  @TypeORM.Column({type:'varchar',length:32}) saved_at: string;
}
