from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import sqlite3
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import os

app = Flask(__name__, template_folder='Templates')
app.secret_key = 'hmaschool_secret_key_2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True

def init_db():
    try:
        conn = sqlite3.connect('hmaschool.db')
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            year INTEGER,
            parent_name TEXT,
            parent_email TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS exit_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT NOT NULL,
            parent_email TEXT NOT NULL,
            reason TEXT NOT NULL,
            exit_date TEXT NOT NULL,
            exit_time TEXT NOT NULL DEFAULT '14:00',
            return_date TEXT NOT NULL,
            return_time TEXT NOT NULL DEFAULT '18:00',
            verification_code TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            
            -- PICK-UP PERSON FIELDS
            pickup_by_other INTEGER DEFAULT 0,
            other_person_name TEXT,
            other_person_phone TEXT,
            other_person_id TEXT,
            other_person_relationship TEXT,
            
            admin_notes TEXT,
            admin_decision_date TEXT,
            printed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS verification_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT NOT NULL,
            code TEXT NOT NULL,
            is_used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        students = [
            ('Ebenezer Gudina', 'ebenezer2025@hmacademy.org', 2025, 'Gudina', 'gudina.parent@email.com'),
            ('Feven Sanka', 'feven2024@hmacademy.org', 2024, 'Sanka', 'sanka.parent@email.com'),
            ('Mikias Tesfaye', 'mikias2026@hmacademy.org', 2026, 'Tesfaye', 'tesfaye.parent@email.com'),
            ('Amen Alemu', 'amen2025@hmacademy.org', 2025, 'Alemu', 'alemu.parent@email.com'),
            ('Wubshet Destaw', 'wubshet2024@hmacademy.org', 2024, 'Destaw', 'destaw.parent@email.com')
        ]
        
        for student in students:
            c.execute('INSERT OR IGNORE INTO students (name, email, year, parent_name, parent_email) VALUES (?, ?, ?, ?, ?)', student)
        
        admin_hashed_password = generate_password_hash('admin123')
        c.execute('INSERT OR IGNORE INTO users (email, password, role, name) VALUES (?, ?, ?, ?)',
                  ('admin@hmacademy.org', admin_hashed_password, 'admin123', 'School Administrator'))
        
        parents = [
            ('sanka.parent@email.com', generate_password_hash('parent123'), 'parent', 'Sanka Parent'),
            ('gudina.parent@email.com', generate_password_hash('parent123'), 'parent', 'Gudina Parent'),
            ('tesfaye.parent@email.com', generate_password_hash('parent123'), 'parent', 'Tesfaye Parent'),
            ('alemu.parent@email.com', generate_password_hash('parent123'), 'parent', 'Alemu Parent'),
            ('destaw.parent@email.com', generate_password_hash('parent123'), 'parent', 'Destaw Parent')
        ]
        
        for email, password, role, name in parents:
            c.execute('INSERT OR IGNORE INTO users (email, password, role, name) VALUES (?, ?, ?, ?)', 
                     (email, password, role, name))
        
        conn.commit()
        conn.close()
        print("✅ Database initialized with ALL features INCLUDING PICK-UP PERSON!")
        print("   - Admin: admin@hmacademy.org / admin123")
        print("   - Parents: parent emails / parent123")
        print("   - Students: Register first")
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        traceback.print_exc()
        return False

init_db()

def add_missing_columns():
    """Safely add missing columns to existing tables"""
    try:
        conn = sqlite3.connect('hmaschool.db')
        c = conn.cursor()
        
        c.execute("PRAGMA table_info(exit_requests)")
        existing_columns = {col[1] for col in c.fetchall()}
        
        required_columns = {
            'pickup_by_other': 'INTEGER DEFAULT 0',
            'other_person_name': 'TEXT',
            'other_person_phone': 'TEXT',
            'other_person_id': 'TEXT',
            'other_person_relationship': 'TEXT'
        }
        
        # Add any missing columns
        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                sql = f'ALTER TABLE exit_requests ADD COLUMN {column_name} {column_type}'
                c.execute(sql)
                print(f"✅ Added missing column: {column_name}")
        
        conn.commit()
        conn.close()
        print("✅ Database migration completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        return False

add_missing_columns()

def get_db():
    conn = sqlite3.connect('hmaschool.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_valid_student_email(email):
    if not email.endswith('@hmacademy.org'):
        return False
    username = email.replace('@hmacademy.org', '')
    if len(username) >= 4 and username[-4:].isdigit():
        year = int(username[-4:])
        return 2023 <= year <= 2030
    return False

def generate_verification_code():
    return secrets.token_hex(3).upper()


@app.route('/')
def index():
    if 'user_email' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user:
            if check_password_hash(user['password'], password):
                session['user_email'] = user['email']
                session['user_role'] = user['role']
                session['user_name'] = user['name']
                flash('Login successful!', 'success')
                return redirect('/dashboard')
            else:
                flash('Invalid password', 'error')
        else:
            flash('Email not registered. Students must register first.', 'error')
    
    return render_template('login.html')

@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect('/register/student')
        
        if not is_valid_student_email(email):
            flash('Email must be in format: nameYEAR@hmacademy.org', 'error')
            return redirect('/register/student')
        
        conn = get_db()
        student = conn.execute('SELECT * FROM students WHERE email = ?', (email,)).fetchone()
        if not student:
            flash('Student not found in school records.', 'error')
            conn.close()
            return redirect('/register/student')
        
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash('Email already registered. Please login instead.', 'error')
            conn.close()
            return redirect('/register/student')
        
        try:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (email, password, role, name) VALUES (?, ?, ?, ?)',
                        (email, hashed_password, 'student', name))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Email already registered', 'error')
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
        finally:
            conn.close()
    
    return render_template('register_student.html')

@app.route('/register/parent')
def register_parent():
    abort(404)

@app.route('/dashboard')
def dashboard():
    if 'user_email' not in session:
        return redirect('/login')
    
    conn = get_db()
    role = session['user_role']
    email = session['user_email']
    
    if role == 'student':
        requests = conn.execute('SELECT * FROM exit_requests WHERE student_email = ? ORDER BY created_at DESC', 
                               (email,)).fetchall()
        student = conn.execute('SELECT * FROM students WHERE email = ?', (email,)).fetchone()
        codes = conn.execute('SELECT * FROM verification_codes WHERE student_email = ? AND is_used = 0 ORDER BY created_at DESC', 
                            (email,)).fetchall()
        conn.close()
        return render_template('student_dashboard.html', 
                             requests=requests, 
                             student=student,
                             codes=codes,
                             user_name=session['user_name'])
    
    elif role == 'parent':
        children = conn.execute('SELECT * FROM students WHERE parent_email = ?', (email,)).fetchall()
        child_emails = [child['email'] for child in children]
        
        if child_emails:
            placeholders = ','.join(['?'] * len(child_emails))
            query = f'SELECT * FROM exit_requests WHERE student_email IN ({placeholders}) ORDER BY created_at DESC'
            requests = conn.execute(query, child_emails).fetchall()
        else:
            requests = []
        
        conn.close()
        return render_template('parent_dashboard.html',
                             children=children,
                             requests=requests,
                             user_name=session['user_name'])
    
    elif role == 'admin':
        pending_requests = conn.execute('SELECT * FROM exit_requests WHERE status = "pending" ORDER BY created_at DESC').fetchall()
        all_requests = conn.execute('SELECT * FROM exit_requests ORDER BY created_at DESC').fetchall()
        students = conn.execute('SELECT * FROM students').fetchall()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return render_template('admin_dashboard.html',
                             pending_requests=pending_requests,
                             all_requests=all_requests,
                             students=students,
                             users=users,
                             user_name=session['user_name'])
    
    conn.close()
    return redirect('/login')

@app.route('/generate_verification/<student_email>')
def generate_verification(student_email):
    if 'user_email' not in session or session['user_role'] != 'student':
        flash('Unauthorized access', 'error')
        return redirect('/login')
    
    if session['user_email'] != student_email:
        flash('Unauthorized access', 'error')
        return redirect('/dashboard')
    
    verification_code = generate_verification_code()
    
    conn = get_db()
    conn.execute('INSERT INTO verification_codes (student_email, code) VALUES (?, ?)',
                (student_email, verification_code))
    conn.commit()
    
    student = conn.execute('SELECT * FROM students WHERE email = ?', (student_email,)).fetchone()
    conn.close()
    
    flash('Verification code generated successfully! Share it with your parent.', 'success')
    return redirect('/dashboard')

@app.route('/request_exit', methods=['GET', 'POST'])
def request_exit():
    if 'user_email' not in session or session['user_role'] != 'parent':
        return redirect('/login')
    
    parent_email = session['user_email']
    conn = get_db()
    
    if request.method == 'POST':
        student_email = request.form['student_email']
        reason = request.form['reason']
        exit_date = request.form['exit_date']
        exit_time = request.form['exit_time']
        return_date = request.form['return_date']
        return_time = request.form['return_time']
        verification_code = request.form.get('verification_code', '').strip().upper()
        
        pickup_by = request.form.get('pickup_by', 'parent')
        other_person_name = request.form.get('other_person_name', '')
        other_person_phone = request.form.get('other_person_phone', '')
        other_person_id = request.form.get('other_person_id', '')
        other_person_relationship = request.form.get('other_person_relationship', '')
        
        pickup_by_other = 1 if pickup_by == 'other' else 0
        
        if not verification_code:
            flash('Verification code is required', 'error')
            conn.close()
            return redirect('/request_exit')
        
        code_entry = conn.execute('''SELECT * FROM verification_codes 
                                   WHERE student_email = ? 
                                   AND code = ?
                                   AND is_used = 0''',
                                (student_email, verification_code)).fetchone()
        
        if code_entry:
            conn.execute('''INSERT INTO exit_requests 
                          (student_email, parent_email, reason, exit_date, exit_time, 
                           return_date, return_time, verification_code, status,
                           pickup_by_other, other_person_name, other_person_phone,
                           other_person_id, other_person_relationship) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, "pending",
                                  ?, ?, ?, ?, ?)''',
                       (student_email, parent_email, reason, exit_date, exit_time, 
                        return_date, return_time, verification_code,
                        pickup_by_other, other_person_name, other_person_phone,
                        other_person_id, other_person_relationship))
            
            conn.execute('UPDATE verification_codes SET is_used = 1 WHERE id = ?', (code_entry['id'],))
            
            conn.commit()
            conn.close()
            flash('Exit request submitted successfully!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid or already used verification code.', 'error')
            conn.close()
            return redirect('/request_exit')
    
    children = conn.execute('SELECT * FROM students WHERE parent_email = ?', (parent_email,)).fetchall()
    conn.close()
    
    if not children:
        flash('No students found under your account', 'error')
        return redirect('/dashboard')
    
    return render_template('request_exit.html', children=children)

@app.route('/admin/approve_with_notes/<int:request_id>', methods=['GET', 'POST'])
def admin_approve_with_notes(request_id):
    if 'user_email' not in session or session['user_role'] != 'admin':
        flash('Admin access required', 'error')
        return redirect('/login')
    
    conn = get_db()
    
    if request.method == 'POST':
        admin_notes = request.form.get('admin_notes', '').strip()
        admin_decision_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('''UPDATE exit_requests 
                       SET status = "approved", 
                           admin_notes = ?,
                           admin_decision_date = ?,
                           printed = 0
                       WHERE id = ?''',
                    (admin_notes, admin_decision_date, request_id))
        conn.commit()
        conn.close()
        
        flash(f'Exit request #{request_id} approved successfully!', 'success')
        return redirect('/dashboard')
    
    request_data = conn.execute('SELECT * FROM exit_requests WHERE id = ?', (request_id,)).fetchone()
    conn.close()
    
    if not request_data:
        flash('Request not found', 'error')
        return redirect('/dashboard')
    return render_template('admin_approve.html', request_data=request_data)

@app.route('/admin/reject_with_reason/<int:request_id>', methods=['GET', 'POST'])
def admin_reject_with_reason(request_id):
    if 'user_email' not in session or session['user_role'] != 'admin':
        flash('Admin access required', 'error')
        return redirect('/login')
    
    conn = get_db()
    
    if request.method == 'POST':
        admin_notes = request.form.get('admin_notes', '').strip()
        admin_decision_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('''UPDATE exit_requests 
                       SET status = "rejected", 
                           admin_notes = ?,
                           admin_decision_date = ?
                       WHERE id = ?''',
                    (admin_notes, admin_decision_date, request_id))
        conn.commit()
        conn.close()
        
        flash(f'Exit request #{request_id} has been rejected.', 'error')
        return redirect('/dashboard')
    
    request_data = conn.execute('SELECT * FROM exit_requests WHERE id = ?', (request_id,)).fetchone()
    conn.close()
    
    if not request_data:
        flash('Request not found', 'error')
        return redirect('/dashboard')
    
    return render_template('admin_reject.html', request_data=request_data)

@app.route('/print_slip/<int:request_id>')
def print_slip(request_id):
    if 'user_email' not in session:
        return redirect('/login')
    
    # ONLY ADMIN CAN PRINT
    if session['user_role'] != 'admin':
        flash('Only administrators can print exit slips.', 'error')
        return redirect('/dashboard')
    
    conn = get_db()
    request_data = conn.execute('SELECT * FROM exit_requests WHERE id = ?', (request_id,)).fetchone()
    
    if not request_data:
        flash('Request not found', 'error')
        conn.close()
        return redirect('/dashboard')
    
    # Mark as printed by admin
    conn.execute('UPDATE exit_requests SET printed = 1 WHERE id = ?', (request_id,))
    
    student = conn.execute('SELECT * FROM students WHERE email = ?', (request_data['student_email'],)).fetchone()
    conn.commit()
    conn.close()
    
    return render_template('print_slip.html', 
                         request=request_data, 
                         student=student,
                         user_name=session.get('user_name'),
                         user_role=session.get('user_role'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect('/')

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("""
    ============================================
    Haile Manas Academy - COMPLETE Exit System
    ============================================
    ✅ System initialized with ALL features:
    
    FEATURES:
    1. 👨‍🎓 Student Registration & Login
    2. 🔐 Student Verification Code Generation
    3. 👨‍👩‍👧‍👦 Parent Login (No Registration)
    
    System:
    1. Student → Register → Login → Generate Code
    2. Parent → Login → Request Exit → Enter Code
    3. Admin → Login → Review → Approve/Reject with Notes
    4. Admin → Print Slip → Send to Parent/Student
    5. Student → Show printed slip → Exit Campus
    
    LOGIN CREDENTIALS:
    ------------------
    Admin:     admin@hmacademy.org / admin123
    Parents:   parent emails / parent123
    Students:  Register first (5 predefined)
    
    ACCESS URLS:
    ------------
    Home:        http://localhost:5000
    Login:       http://localhost:5000/login
    Dashboard:   http://localhost:5000/dashboard
    
    ============================================
    """)
    
    app.run(debug=True, port=5000)