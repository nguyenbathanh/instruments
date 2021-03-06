import psycopg2, psycopg2.extras
import hashlib

from instruments import app

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

def connect():
    
    conn = psycopg2.connect(app.config['DSN'])
    conn.set_client_encoding('UTF8')
    
    curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    return conn, curs
    
    
def create_tables(DSN, forename, surname, email, username, password):
    query = """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            forename TEXT,
            surname TEXT,
            email TEXT,
            username TEXT UNIQUE,
            password CHARACTER(128),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE INDEX password ON users(password);
            CREATE INDEX email ON users(email);
    """
    
    try:
        conn = psycopg2.connect(DSN)
    except:
        print "Error connecting to database: %s" % DSN
        return
        
    curs = conn.cursor()
    
    try:
        curs.execute(query)
    except:
        print "Error executing query on database"
        curs.close()
        conn.close()
        raise
        return
    
    # Create default account
    password_hash = hashlib.sha512(password).hexdigest()
    query = """INSERT INTO users (forename, surname, email, username, password)
               VALUES (%s, %s, %s, %s, %s);"""
    
    try:           
        curs.execute(query, (forename, surname, email, username, password_hash))
        conn.commit()
    except:
        print "Error executing query on database: %s" % DSN
        raise
    else:
        print "Tables successfully created."
    finally:
        curs.close()
        conn.close()
    
    
def check_login_details(username, password_plaintext):
    #return {'forename': 'Mike', 'surname': 'Watts', 'user_id': 0}
    password_hash = hashlib.sha512(password_plaintext).hexdigest()
    query = """
        SELECT user_id, forename, surname
        FROM users
        WHERE username LIKE %s
        AND password LIKE %s
    """
    
    conn, curs = connect()
    
    curs.execute(query, (username, password_hash))
    
    result = curs.fetchone()
    
    conn.rollback()
    curs.close()
    conn.close()
    
    return result
    
    
def get_username_for_id(user_id):
    query = """
        SELECT username
        FROM users
        WHERE user_id = %s
    """
    
    conn, curs = connect()
    
    curs.execute(query, (user_id,))
    
    result = curs.fetchone()
    
    conn.rollback()
    curs.close()
    conn.close()
    
    if result:
        return result['username']
    else:
        return None
        
        
def update_password(user_id, password_plaintext):
    password_hash = hashlib.sha512(password_plaintext).hexdigest()
    
    query = """
        UPDATE users
        SET password = %s
        WHERE user_id = %s
    """
    
    conn, curs = connect()
    
    curs.execute(query, (password_hash, user_id))
    
    conn.commit()
    curs.close()
    conn.close()
    
    
def execute_query(query, values=[]):
    conn, curs = connect()
    
    curs.execute(query, values)
    
    results = []
    try:
        conn.commit()
        results = curs.fetchall()
        
    except:
        #log an error
        pass
    
    if len(results) == 1 and len(results[0]) == 1:
        results = results[0][0]
    
    curs.close()
    conn.close()
    
    return results
