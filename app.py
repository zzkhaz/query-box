# -*- coding: utf-8 -*-
from flask import Flask,render_template,redirect,url_for,request,flash
from flask.ext.bootstrap import Bootstrap
from flask_login import LoginManager
from forms import Login,Register
import sqlite3
import datetime

app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object('config')

#主页
@app.route('/index')
def index():
    return render_template('index.html')

#登陆
@app.route('/login/',methods=('POST','GET'))
def login():
    form=Login()
    if form.validate_on_submit():
        name = form.name.data
        pwd = form.pwd.data
        if if_login(name,pwd):
            flash('登录成功')
            return redirect(url_for('user_console_noreply',user_id = name))
        else:
            flash('登录失败')
            return render_template('login.html',form=form)
    else:
        return render_template('login.html',form=form)

#注册
@app.route('/register/',methods=['GET','POST'])
def register():
    form=Register()
    if form.validate_on_submit():
        name=form.name.data
        pwd=form.pwd.data
        if_register(name,pwd)
        flash('注册成功')
        return redirect(url_for('user_console_noreply',user_id = name))
    return render_template('register.html',form=form)

#提问页
@app.route('/<user_id>/')
def user_index(user_id):
    if get_qa_list(user_id)[0]:
        qa_list = []
        for row in get_qa_list(user_id)[1]:
            if row[6] == 1:
                qa_list.append({'QUESTION': row[2] ,'ANSWER': row[3] ,'Q_DATE': row[4] ,'A_DATE': row[5] ,'STATE': row[6]})
        return render_template("user_main.html", user_name = user_id,qa_list = qa_list)
    else:
        return render_template("user_notfound.html", user_name = user_id)

@app.route('/<user_id>/',methods=['POST'])
def question_post(user_id):
    question = request.form['question']
    question_text = question.upper()
    ask_question(user_id,question_text)
    return redirect('/' + user_id +'/')

#管理页
@app.route('/<user_id>/box/')
def user_console_noreply(user_id):
    if get_qa_list(user_id)[0]:
        qa_list = []
        for row in get_qa_list(user_id)[1]:
            qa_list.append({'QA_ID': row[0] ,'QUESTION': row[2] ,'ANSWER': row[3] ,'Q_DATE': row[4] ,'A_DATE': row[5] ,'STATE': row[6]})
        return render_template("user_box.html", user_name = user_id,qa_list = qa_list)
    else:
        return render_template("user_notfound.html", user_name = user_id)

@app.route('/<user_id>/box/reply/')
def user_console_reply(user_id):
    if get_qa_list(user_id)[0]:
        qa_list = []
        for row in get_qa_list(user_id)[1]:
            qa_list.append({'QA_ID': row[0] ,'QUESTION': row[2] ,'ANSWER': row[3] ,'Q_DATE': row[4] ,'A_DATE': row[5] ,'STATE': row[6]})
        return render_template("user_box_reply.html", user_name = user_id,qa_list = qa_list)
    else:
        return render_template("user_notfound.html", user_name = user_id)

#问题页
@app.route('/q/<qa_id>/')
def reply(qa_id):
    qa = get_qa(qa_id)[0][0]
    user_name = get_qa(qa_id)[1][0][0]
    return render_template("question.html",qa = qa,user_name = user_name)

@app.route('/q/<qa_id>/', methods=['POST'])
def reply_post(qa_id):
    answer = request.form['answer']
    answer_text = answer.upper()
    reply_answer(qa_id,answer_text)
    return redirect('/q/' + qa_id +'/')

def if_login(name,pwd):
    n = str(name)
    conn = sqlite3.connect('data.db',check_same_thread = False)
    cursor = conn.cursor()
    if pwd == cursor.execute('SELECT * from user where user_name = "'+n+'"').fetchall()[0][2]:
        return 1
    else:
        return 0
 
def if_register(name,pwd):
    n = str(name)
    p = str(pwd)
    conn = sqlite3.connect('data.db',check_same_thread = False)
    cursor = conn.cursor()
    if cursor.execute('SELECT * from user where user_name = "'+n+'"').fetchall():
        print ('用户已存在')
    else:
        i = str(cursor.execute('SELECT max(user_id) from user').fetchall()[0][0] + 1)
        cursor.execute('insert into user (user_id,user_name,password) VALUES ("'+i+'","'+n+'","'+p+'")')
        conn.commit()
        cursor.close()
        conn.close()
        print ('注册成功')
        
    
def get_qa_list(user_id):
    n = str(user_id)
    conn = sqlite3.connect('data.db',check_same_thread = False)
    cursor = conn.cursor()
    name = cursor.execute('SELECT * from user where user_name = "'+n+'"').fetchall()
    qa = cursor.execute('select * from (select * from qa) s INNER join (select * from user where user_name = "'+n+'") t on s.user_id = t.user_id')
    return name,qa
    cursor.close()
    conn.close()

def get_qa(qa_id):
    q = str(qa_id)
    conn = sqlite3.connect('data.db',check_same_thread = False)
    cursor = conn.cursor()
    question = cursor.execute('SELECT * from qa where qa_id = "'+q+'"').fetchall()
    u = str(question[0][1])
    user = cursor.execute('select user_name from user where user_id = "'+u+'"').fetchall()
    return question,user
    cursor.close()
    conn.close()

def reply_answer(qa_id,answer):
    q = str(qa_id)
    a = str(answer)
    t = datetime.datetime.now().strftime("%Y-%m-%d") 
    conn = sqlite3.connect('data.db',check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute('update qa set answer = "'+a+'" where qa_id = "'+q+'"')
    cursor.execute('update qa set a_date = "'+t+'" where qa_id = "'+q+'"')
    cursor.execute('update qa set state = 1 where qa_id = "'+q+'"')    
    conn.commit()
    print('修改成功')
    cursor.close()
    conn.close()

def ask_question(user_id,question):
    conn = sqlite3.connect('data.db',check_same_thread = False)
    cursor = conn.cursor()
    u = str(cursor.execute('SELECT user_id from user where user_name = "'+str(user_id)+'"').fetchall()[0][0])
    q = str(question)
    t = datetime.datetime.now().strftime("%Y-%m-%d")
    i = str(cursor.execute('SELECT max(qa_id) from qa').fetchall()[0][0] + 1)
    cursor.execute('insert into qa (qa_id,user_id,question,answer,q_date,a_date,state) VALUES ("'+i+'","'+u+'","'+q+'"," ","'+t+'","'+t+'",0)')
    conn.commit()
    print('修改成功')
    cursor.close()
    conn.close()
    
if __name__=="__main__":
    app.run(debug=True)
