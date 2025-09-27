# Database Migration Guide

## Overview
This migration updates the database schema to support exercises that can work multiple muscle groups (many-to-many relationship).

## Migration Steps

### 1. Backup your data
Before running any migration, ensure you have a backup of your database.

### 2. Run the migration script
```bash
python migrate_db_many_to_many.py
```

This script will:
- Create the new `exercise_muscle_groups` table
- Copy existing data from `exercises.muscle_group_id` to the new table
- Keep the old column for compatibility during testing

### 3. Test the application
Test all functionality to ensure everything works correctly:
- Add new exercises with multiple muscle groups
- Edit existing exercises
- Check that workouts and analytics still work
- Test delete functionality

### 4. Remove old column (optional)
Once you've verified everything works correctly, you can remove the old column:
```bash
python remove_old_column.py
```

## New Database Schema

### exercise_muscle_groups table
```sql
create table exercise_muscle_groups (
    id serial primary key,
    exercise_id integer references exercises(id) on delete cascade,
    muscle_group_id integer references muscle_groups(id) on delete cascade,
    unique(exercise_id, muscle_group_id)
);
```

## Rollback Plan
If you need to rollback:
1. Stop the application
2. Restore from your backup
3. Or manually drop the `exercise_muscle_groups` table if no data was lost