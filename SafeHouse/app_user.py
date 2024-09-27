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
    return redirect(url_for('request_assistance'))  # Redirect directly to the request form

@app.route('/request_assistance', methods=['GET', 'POST'])
def request_assistance():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        emergency_type = request.form['emergencyType']
        resources_needed = request.form.getlist('resources')  # Get list of resources from checkboxes

        conn = get_db_connection()
        cur = conn.cursor()

        # Here we assume the database has a 'requests' table to log assistance requests
        cur.execute('INSERT INTO assistance_requests (name, phone, email, emergency_type) VALUES (%s, %s, %s, %s)',
                    (name, phone, email, emergency_type))
        
        # Define resource reduction based on emergency type
        if emergency_type == 'naturalDisaster':
            if 'food' in resources_needed:
                cur.execute('UPDATE safehouses SET food = food - 1 WHERE food > 0;')
            if 'shelter' in resources_needed:
                cur.execute('UPDATE safehouses SET capacity = capacity - 1 WHERE capacity > 0;')
        elif emergency_type == 'medicalServices':
            if 'medicine' in resources_needed:
                cur.execute('UPDATE safehouses SET drugs = drugs - 1 WHERE drugs > 0;')

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('home'))  # Redirect to home or another page after submission
    return render_template('request_assistance.html')  # Render the form on GET request

if __name__ == '__main__':
    app.run(debug=True)

