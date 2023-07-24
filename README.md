# mssql-django Index Issue

This project was created to reproduce a problem with handling indexes by mssql-django version 1.3.

Specifically, the mssql-django library does not remove an index before modifying a column upon which the index depends.

### Steps to reproduce with this repo:

1. Clone this repo.
2. Modify database connection string to match your environment.
3. Run migrations.

Observe the following error:

```
django.db.utils.ProgrammingError: ('42000', "[42000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]The index 'my_custom_index' is dependent on column 'another_field'. (5074) (SQLExecDirectW)")
```

### Steps to reproduce this issue in general:

1. Add a nullable field to a model.
2. Add a custom index that references the new field in the model's Meta class.
3. Make and apply migrations.
4. Remove the nullable option from the field.
5. Make and apply migrations.


SQL from the migration created in step 3 (polls 0002):

```sql
BEGIN TRANSACTION
--
-- Add field another_field to demo
--
ALTER TABLE [polls_demo] ADD [another_field] int NULL;
--
-- Create index my_custom_index on field(s) name, another_field of model demo
--
CREATE INDEX [my_custom_index] ON [polls_demo] ([name], [another_field]);
COMMIT;
```

SQL from the migration created in step 5 (polls 0003):

```sql
BEGIN TRANSACTION
--
-- Alter field another_field on demo
--
ALTER TABLE [polls_demo] ALTER COLUMN [another_field] int NOT NULL;
COMMIT;
```

This migration is not dropping the index before altering the column and recreating the index afterwards.


If an index is defined directly on the column (db_index=True), the migration correctly drops and recreates the index.
This is demonstrated on the index_on_column branch in this repo.

```sql
BEGIN TRANSACTION
--
-- Add field another_field to demo
--
ALTER TABLE [polls_demo] ADD [another_field] int NULL;
CREATE INDEX [polls_demo_another_field_2f8da3bd] ON [polls_demo] ([another_field]);
COMMIT;
```

```sql
BEGIN TRANSACTION
--
-- Alter field another_field on demo
--
DROP INDEX [polls_demo_another_field_2f8da3bd] ON [polls_demo];
ALTER TABLE [polls_demo] ALTER COLUMN [another_field] int NOT NULL;
CREATE INDEX [polls_demo_another_field_2f8da3bd] ON [polls_demo] ([another_field]);
COMMIT;
```

