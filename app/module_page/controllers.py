@app.route('/', methods=['GET','POST'])
def index():
    form=NameForm()
    cur=mysql.connection.cursor()
    if 'username' in session:
        username_session = session['username']
        
        cur.execute("SELECT job FROM login where username = '" + username_session + "'")
        for job1 in cur.fetchall():
                if job1[0]=="student":
                    cur.execute("SELECT sf_check FROM s_profile WHERE s_username = '" + username_session + "'")
                    check_var = cur.fetchone()
                    if check_var==None:
                        return render_template('stud_profile.html')
                    return render_template('index_stud.html',session_name=username_session)
                cur.execute("SELECT tf_check FROM t_profile WHERE t_username = '" + username_session + "'")
                check_var = cur.fetchone()
                if check_var==None:
                    return render_template('teach_profile.html')
                return render_template('index_teach.html', session_name=username_session)

     
    return redirect(url_for('login'))




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=NameForm()
    return render_template('signup.html', form=form)

@app.route('/add_db', methods=['GET', 'POST'])
def add_db():
    form = NameForm()
    
    username1 = str(form.username.data)
    email1= str(form.email.data)
    password1=str(form.password.data)
    job1 = str(form.job.data) 
    cur=mysql.connection.cursor()
    
    cur.execute('''INSERT INTO login (username, email, password, job) VALUES (%s, %s, %s, %s)''' , (username1, email1, password1,job1))
    mysql.connection.commit()
    #return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/sformfill', methods=['GET', 'POST'])
def sformfill():
    if request.method == 'POST':
        name = request.form['name']
        dept = request.form['branch']
        sem =  request.form['sem']
        clg = request.form['clg']
        username = session['username']
        cur=mysql.connection.cursor()
    
        cur.execute("INSERT INTO s_profile(s_name, s_dept, s_sem, s_username, sf_check, s_clg) VALUES(%s, %s, %s, %s, %s, %s)",(name, dept, sem, username, 1, clg)) 
        mysql.connection.commit()

        return redirect(url_for('index'))

@app.route('/tformfill', methods=['GET','POST'])
def tformfill():
     if request.method == 'POST':
        name = request.form['name']
        dept = request.form['branch']
        
        clg = request.form['clg']
        username = session['username']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO t_profile(t_name, t_username, t_dept, t_clg, tf_check) VALUES(%s, %s, %s, %s, %s)",(name, username, dept,clg, 1)) 
        mysql.connection.commit()

        return redirect(url_for('index'))
        
    
    

    




@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form=NameForm()
    cur=mysql.connection.cursor()
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        return render_template('login4.html', form=form)
    
@app.route('/check', methods=["POST"])
def check():
    form=NameForm()
    cur=mysql.connection.cursor()
    if request.method == 'POST':
        username_form  = form.username.data
        cur.execute("SELECT username AS uname FROM login WHERE username = '{}'".format(username_form))
        fetched_name = cur.fetchone()
        if fetched_name == None:
            return 'Invalid username'
            
            
        password_form  = form.password.data
        cur.execute("SELECT password AS pword FROM login WHERE username = '{}'".format(username_form))
            
        for row in cur.fetchall():
            if password_form == row[0]:
                session['username'] = form.username.data
                return redirect(url_for('index'))
            return 'Invalid password'
        
    #return render_template('login4.html', form=form)
    
@app.route('/upload')
def upload():
    username_session = session['username']
    cur=mysql.connection.cursor()
    cur.execute("SELECT job FROM login where username = '" + username_session + "'")
    for job1 in cur.fetchall():
            if job1[0]=="student":
                return redirect(url_for('index'))
    form=NameForm()
    return render_template('upload.html', form=form)
    

@app.route('/uploading', methods=['POST'])
def uploading():
    form=NameForm()
    cur=mysql.connection.cursor()
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename): 
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        
        
        
        f_name1 = str(form.f_name.data)
        branch1 = request.form['branch']
       
        
        sem1 = request.form['sem']
        public1 = form.public.data
        username = session['username']
        
        cur=mysql.connection.cursor()
        #cur.execute("SELECT id as u_id FROM login WHERE username = '" + username + "'")
        
        #u_id1=cur.fetchall()
        
        
        
        cur.execute('''INSERT INTO files(f_name, actualname, f_username, branch, sem, public) VALUES (%s, %s, %s, %s, %s, %s)''',[f_name1, filename, username, branch1, sem1, public1])
        mysql.connection.commit()
        return redirect(url_for('index'))


                        
                    
    return 'Couldn\'t complete upload'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/search_results', methods=['GET','POST'])
def search():
    cur=mysql.connection.cursor()
    search = request.form['search']
    cur.execute("SELECT t_name from t_profile where t_username ='" + search + "'")
    username = cur.fetchall()
    
    return render_template('results.html',username = username)

@app.route('/teacher/<username>', methods=['GET','POST'])
def tprof(username):
    name = username
    cur=mysql.connection.cursor()
    cur.execute("SELECT t_name from t_profile where t_username ='" + name + "'")
    main_name = cur.fetchall()
    return render_template('teach_profile.html', main_name=main_name)

@app.route('/teacher/<username>/files')
def view_files(username):
    name = username
    sql = "SELECT fid from files WHERE f_username ='" + name + "'"
    cur=mysql.connection.cursor()
    cur.execute(sql)
    for ids in cur.fetchall():
        print ids
        sql1 = "select f_name from files where fid = %s"  
        cur.execute(sql1,ids)
        vf=cur.fetchall()
        return render_template('view_files.html',vf=vf)
    
    return 'No files uploaded'
        
        
    
    
    
    

    
        
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
