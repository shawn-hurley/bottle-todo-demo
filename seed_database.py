"""Seed database with default tasks."""


def load_database(connection):
    """Execute database commands for the connection given."""
    conn = connection.cursor()
    conn.execute("CREATE TABLE todo (id serial PRIMARY KEY, task char(100) NOT NULL, status int NOT NULL)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Test various editors for and check the syntax highlighting',1)")
    conn.execute("INSERT INTO todo (task,status) VALUES ('Choose your favorite WSGI-Framework',0)")
    connection.commit()
