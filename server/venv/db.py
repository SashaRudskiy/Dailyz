import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname='dailyz',
        user='dailyz_user',
        password='dailyz_pass',
        host='localhost'
    )
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL CHECK(length(task) <= 255),
            done BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized!')
