from .views import app, mysql, read_sql_file
# Create tables from schema.sql
with app.app_context():
    cursor = mysql.connection.cursor()
    sql = read_sql_file('schema.sql')
    for statement in sql.split(';'):
        cursor.execute(statement)
    mysql.connection.commit()
    cursor.close()
