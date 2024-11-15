import sqlite3
import bcrypt
from flask import Flask, jsonify,render_template,request,session,redirect,url_for,flash,logging




app = Flask(__name__)
app.secret_key = 'my_secret_key_123'


@app.route('/')
def hello_world():
    if 'username' not in session:
        return render_template('home.html')
    return render_template('home.html')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/applicants')
def applicants():
    if 'username' in session:
        connection = sqlite3.connect('mixmuse_users.db')
        cursor = connection.cursor()

        username = session['username']
        website_user = session['website_user']
        query = "SELECT * from users where username = '"+username+"' "
        cursor.execute(query)

        user_data = cursor.fetchone()
        return render_template('viewappli.html',user_data=user_data,website_user=website_user)

    return render_template('viewappli.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('home.html')






@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('mixmuse_users.db')
        cursor = connection.cursor()

        username = request.form['user']
        password = request.form['password']

        print(f"Login attempt for user: {username}")  # Debug print

        query = "SELECT username, password, website_user FROM users WHERE username = ?"
        cursor.execute(query, (username,))

        user_data = cursor.fetchone()

        if user_data:
            stored_username, stored_password, website_user = user_data
            print(f"User found: {stored_username}")  # Debug print
            print(f"Stored password type: {type(stored_password)}")
            print(f"Stored password length: {len(stored_password)}")

            try:
                # Convert input password to bytes for comparison
                input_password = password.encode('utf-8')

                
                # Use bcrypt to check the password
                if bcrypt.checkpw(input_password, stored_password):
                    print("Password check succeeded")
                    session['username'] = username
                    session['website_user'] = website_user
                    
                    # Fetch additional user data if needed
                    query = "SELECT * FROM users WHERE username = ?"
                    cursor.execute(query, (username,))
                    user_data = cursor.fetchone()

                    connection.close()

                    if website_user == 'artist':
                        return render_template('pexp.html', name=username, user_data=user_data)
                    elif website_user == 'employer':
                        return render_template('EmpHomePage.html', name=username, user_data=user_data)
                    else:
                        return redirect(url_for('login'))
                    
                    # return render_template('posts.html', name=username, user_data=user_data)
                else:
                    print("Password check failed")
                    connection.close()
                    flash('Invalid username or password', 'error')
                    return redirect(url_for('login'))
            except Exception as e:
                print(f"Exception during password check: {str(e)}")
                connection.close()
                flash('An error occurred during login. Please try again.', 'error')
                return redirect(url_for('login'))
        else:
            print(f"No user found for username: {username}")
            connection.close()
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            # Get form data with default values to prevent KeyError
            username = request.form.get('user', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm-password', '')
            email = request.form.get('email', '').strip()
            fullname = request.form.get('name', '').strip()
            phonenumber = request.form.get('phone', '').strip()
            gender = request.form.get('gender', '').strip()
            website_user = request.form.get('website_user', '').strip()
            

            # Validate required fields
            if not all([username, password, confirm_password, email, fullname, phonenumber, gender,website_user]):
                return render_template('signup.html',
                    error_msg="All fields are required.",
                    username=username,
                    email=email,
                    fullname=fullname,
                    phonenumber=phonenumber,
                    gender=gender)

            # Check if passwords match
            if password != confirm_password:
                return render_template('signup.html',
                    error_msg="Passwords do not match. Please try again.",
                    username=username,
                    email=email,
                    fullname=fullname,
                    phonenumber=phonenumber,
                    gender=gender)

            # Connect to database
            con = sqlite3.connect('mixmuse_users.db')
            c = con.cursor()

            # Check if username exists
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = c.fetchone()

            if existing_user:
                con.close()
                return render_template('signup.html',
                    error_msg="Username already exists. Please choose a different username.",
                    email=email,
                    fullname=fullname,
                    phonenumber=phonenumber,
                    gender=gender)

            # Hash password and insert user
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            c.execute("""
                INSERT INTO users (username, password, fullname, phoneno, gender, email,website_user) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, fullname, phonenumber, gender, email,website_user))
            
            con.commit()
            con.close()

            flash('Registration successful! Please login.')
            return redirect(url_for('login'))

        except Exception as e:
            app.logger.error(f"Error during signup: {str(e)}")  # For debugging
            return render_template('signup.html',
                error_msg="An error occurred during signup. Please try again.",
                username=username,
                email=email,
                fullname=fullname,
                phonenumber=phonenumber,
                gender=gender)

    # GET request
    return render_template('signup.html')



@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'username' not in session:
        return render_template('home.html')
    

    if 'username' in session:
        connection = sqlite3.connect('mixmuse_users.db')
        cursor = connection.cursor()

        username = session['username']
        website_user = session['website_user']
        query = "SELECT * from users where username = '"+username+"' "
        cursor.execute(query)

        user_data = cursor.fetchone()

        if request.method == 'POST':
            fullname = request.form['name']
            username = request.form["user"]
            password = request.form["password"]
            email = request.form["email"]
            phonenumber = request.form["phone"]
            gender = request.form["gender"]
            address = request.form["address"]
            skills = request.form["skills"]
            experience = request.form["exp"]

            query = "UPDATE users SET fullname = ?, username = ?, email = ?, phoneno = ?, password = ?, address = ?, skills = ?, experience = ?, gender = ? WHERE username = ?"
            cursor.execute(query,(fullname, username, email, phonenumber, password,address,skills,experience, gender, username))
            connection.commit()

            query = "SELECT * from users where username = '"+username+"' "
            cursor.execute(query)
            user_data = cursor.fetchone()

            session['username'] = username

            return render_template('profile.html', user_data=user_data,website_user=website_user)
        
        return render_template('profile.html', user_data=user_data,website_user=website_user)
    else:
        return render_template('profile.html')
    




@app.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    conn = sqlite3.connect('mixmuse_users.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM posts WHERE id=?", (id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"error": "Job not found"}), 404  # Job not found
        return jsonify({"message": "Job deleted successfully"}), 200  # Successful deletion
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500  # Internal server error
    finally:
        conn.close() 

    
@app.route('/emphome')
def emphome():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    posts = []

    connection = sqlite3.connect('mixmuse_users.db')
    cursor = connection.cursor()


    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    

    # if website_user == 'employer':
        
    # Fetch job posts for the logged-in employer
    posts = cursor.execute('SELECT * FROM posts WHERE username = ?',(username,)).fetchall()

    connection.close()
    return render_template('EmpHomePage.html', name=username, user_data=user_data, posts=posts)

    # else:
    return render_template('EmpHomePage.html',name=username,user_data=user_data)





# def get_jobs():    # Connect to your database    conn = sqlite3.connect('mixmuse_users.db')
#     conn = sqlite3.connect('mixmuse_users.db')
#     cursor = conn.cursor()

#     username = session['username']
#         # Fetch jobs from the posts table
#     cursor.execute("SELECT * FROM posts WHERE username = ?",(username,))
#     jobs = cursor.fetchall()

#         # Close the connection
#     conn.close()

#     # Format the jobs into a list of dictionaries
#     job_list = []
#     for job in jobs:
#         job_list.append({
#             'title': job[1],
#             'company_name': job[2],
#             'company_address': job[3],
#             'job_type': job[4],
#             'salary': job[5],
#             'duration': job[6],
#             'open_positions': job[7],
#             'requirements': job[8],
#             'job_description': job[9],
#             'employee_responsibilities': job[10],
#             'what_your_company_offers': job[11]
#         })

#     return job_list





@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    
        connection = sqlite3.connect('mixmuse_users.db')
        cursor = connection.cursor()
        
        
        username = session['username']

        # Fetch all job posts
        cursor.execute("SELECT id, job_title, company_name, open_positions,job_description FROM posts WHERE username = ?",(username,))
        jobs = cursor.fetchall()

        connection.close()

        # Convert jobs to a list of dictionaries
        job_list = []
        for job in jobs:
            job_list.append({
                'id': job[0],
                'title': job[1],
                'company_name': job[2],
                'open_positions': job[3],
                'job_description':job[4]
            })

        return jsonify(job_list)


@app.route('/api/alljobs', methods=['GET'])
def get_alljobs():
    
        connection = sqlite3.connect('mixmuse_users.db')
        cursor = connection.cursor()
        
        
        #username = session['username']

        # Fetch all job posts
        cursor.execute("SELECT id, job_title, company_name, open_positions,job_description FROM posts")
        jobs = cursor.fetchall()

        connection.close()

        # Convert jobs to a list of dictionaries
        job_list = []
        for job in jobs:
            job_list.append({
                'id': job[0],
                'title': job[1],
                'company_name': job[2],
                'open_positions': job[3],
                'job_description':job[4]
            })

        return jsonify(job_list)



@app.route('/posts',methods=['GET','POST'])
def posts():
    
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    posts = []

    connection = sqlite3.connect('mixmuse_users.db')
    cursor = connection.cursor()


    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    

    # if website_user == 'employer':
        
    # Fetch job posts for the logged-in employer
    posts = cursor.execute('SELECT * FROM posts').fetchall()

    connection.close()
    return render_template('pexp.html', name=username, user_data=user_data, posts=posts)
    

    # if 'username' in session:
    #     connection = sqlite3.connect('mixmuse_users.db')
    #     cursor = connection.cursor()

    #     username = session['username']
    #     website_user = session['website_user']

    #     cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    #     user_data = cursor.fetchone()

    #     if website_user == 'artists':
    #         query_jobs = "SELECT * FROM posts ORDER BY id DESC"
    #         cursor.execute(query_jobs)
    #         jobs = cursor.fetchall()

    #         connection.close()
    #         return render_template('pexp.html',name=username, user_data=user_data, website_user=website_user,jobs=jobs)
        

        # else:
        #     return render_template('pexp.html')

        

@app.route('/postjob',methods=['GET','POST'])
def postjob():
    
    if 'username' in session:
        connection = sqlite3.connect('mixmuse_users.db')
        cursor = connection.cursor()

        username = session['username']
        query = "SELECT * from users where username = '"+username+"' "
        cursor.execute(query)

        user_data = cursor.fetchone()

    if request.method == 'POST':
        job_title = request.form['profession']
        company_name = request.form['company']
        company_addr = request.form['address']
        job_type = request.form['jobType']
        sal = request.form['salary']
        duration = request.form['duration']
        openPos = int(request.form['positions'])
        req = request.form['requirements']
        job_desc = request.form['description']
        job_resp = request.form['responsibilities']
        offers = request.form['offers']

        try:
            con = sqlite3.connect('mixmuse_users.db')
            c = con.cursor()
            c.execute(''' INSERT INTO posts (job_title, company_name, company_address, job_type, salary, duration, open_positions, requirements, job_description, employee_responsibilities, what_your_company_offers,username)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
                    (job_title, company_name, company_addr, job_type, sal, duration, openPos, req, job_desc, job_resp, offers,username))
            
            post_id = c.lastrowid
            con.commit()
            con.close()
            return render_template('EmpHomePage.html',post_id=post_id,user_data=user_data)

        except Exception as e:
            con.rollback()
            print("An error occurred:", e)
            return render_template('postjob.html', error="An error occurred while posting the job.", user_data=user_data)
        finally:
            con.close()

    return render_template('postjob.html',user_data=user_data)

@app.route('/requirments/<int:job_id>')
def requirments(job_id):
    connection = sqlite3.connect('mixmuse_users.db')
    cursor = connection.cursor()

    # Fetch job details based on job_id
    cursor.execute("SELECT job_title, company_name, company_address,job_type, salary,duration,open_positions, requirements, job_description, employee_responsibilities, what_your_company_offers FROM posts WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    username = session['username']
    query = "SELECT * from users where username = '"+username+"' "
    cursor.execute(query)

    user_data = cursor.fetchone()

    connection.close()

    if job:
        job_details = {
            'title': job[0],
            'company_name': job[1],
            'company_address': job[2],
            'job_type': job[3],
            'salary': job[4],
            'duration': job[5],
            'open_positions': job[6],
            'requirements': job[7],
            'job_description': job[8],
            'employee_responsibilities': job[9],
            'what_your_company_offers': job[10]
        }
        return render_template('reqexp.html', job=job_details,user_data=user_data)
    else:
        return "Job not found", 404











app.run(debug="True")



