import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname='dailyz',
        user='dailyz_user',
        password='dailyz_pass',
        host='localhost'
    )
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    conn.commit()
    c.close()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized!")