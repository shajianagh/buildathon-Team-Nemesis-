from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='safehouses',
        user='postgres', 
        password='nemesis'
        )
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM safehouses;')
    safehouses = cur.fetchall()  

    cur.execute('SELECT * FROM assistance_requests;')
    assistance_requests = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', items=safehouses, requests=assistance_requests)


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    capacity = request.form['capacity']
    food = request.form['food']
    drugs = request.form['drugs']
    
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT id FROM safehouses WHERE name = %s;', (name,))
    existing_safehouse = cur.fetchone()

    if existing_safehouse:
       cur.execute('UPDATE safehouses SET capacity = %s, food = %s, drugs = %s WHERE name = %s;',
                    (capacity, food, drugs, name))
    else:
       cur.execute('INSERT INTO safehouses (name, capacity, food, drugs) VALUES (%s, %s, %s, %s);',
                    (name, capacity, food, drugs))

    conn.commit()
    cur.close()
    conn.close()
    
    return redirect('/')


@app.route('/reduce_capacity/<int:safehouses_id>', methods=['POST'])
def reduce_capacity(safehouses_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE safehouses SET capacity = capacity - 1 WHERE id = %s AND capacity > 0;', (safehouses_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:safehouses_id>')
def delete(safehouses_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM safehouses WHERE id = %s;', (safehouses_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


