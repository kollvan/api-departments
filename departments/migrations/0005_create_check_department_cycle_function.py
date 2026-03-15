import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('departments', '0004_alter_department_parent_id'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
                CREATE OR REPLACE FUNCTION check_department_cycle(
                    dept_id INTEGER,
                    new_parent_id INTEGER
                ) RETURNS BOOLEAN AS $$
                BEGIN
                    RETURN EXISTS(
                        WITH RECURSIVE descendants AS (
                            SELECT id, parent_id_id
                            FROM departments_department
                            WHERE id = dept_id
                            
                            UNION ALL
                            
                            SELECT d.id, d.parent_id_id
                            FROM departments_department d
                            INNER JOIN descendants des ON d.parent_id_id = des.id
                        )
                        SELECT 1 FROM descendants WHERE id = new_parent_id
                    );
                END;
                $$ LANGUAGE plpgsql;
            ''',
            reverse_sql='DROP FUNCTION IF EXISTS check_department_cycle(INTEGER, INTEGER);'
        )
    ]
