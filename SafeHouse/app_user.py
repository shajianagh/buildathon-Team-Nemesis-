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
def home():
    return redirect(url_for('request_assistance'))

@app.route('/request_assistance', methods=['GET', 'POST'])
def request_assistance():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        emergency_type = request.form['emergencyType']
        resources_needed = request.form.getlist('resources')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO assistance_requests (name, phone, email, emergency_type) VALUES (%s, %s, %s, %s)',
                    (name, phone, email, emergency_type))
        conn.commit()


        if emergency_type == 'pandemic':
            cur.execute('''
                SELECT name, capacity, food, drugs 
                FROM safehouses 
                WHERE capacity > 0 AND food > 0 AND drugs > 0
                ORDER BY capacity DESC, food DESC, drugs DESC
                LIMIT 1;
            ''')
        else:
            cur.execute('''
                SELECT name, capacity, food 
                FROM safehouses 
                WHERE capacity > 0 AND food > 0
                ORDER BY capacity DESC, food DESC
                LIMIT 1;
            ''')

        safehouse = cur.fetchone()  

        cur.close()
        conn.close()

        if safehouse is None:
            return "No suitable safehouse found.", 404

        if emergency_type == 'pandemic':
            if len(safehouse) == 4:
                return render_template('safehouse_allocated.html',
                                       name=name,
                                       safehouse_name=safehouse[0],
                                       safehouse_capacity=safehouse[1],
                                       safehouse_food=safehouse[2],
                                       safehouse_medicine=safehouse[3])
            else:
                return "Safehouse data is incomplete.", 500
        else:
            if len(safehouse) == 3:
                return render_template('safehouse_allocated.html',
                                       name=name,
                                       safehouse_name=safehouse[0],
                                       safehouse_capacity=safehouse[1],
                                       safehouse_food=safehouse[2])
            else:
                return "Safehouse data is incomplete.", 500

    return render_template('request_assistance.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
