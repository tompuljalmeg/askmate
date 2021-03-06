from flask import Flask, render_template, redirect, request, session, escape
import data_manager
import password_hash

app = Flask(__name__)
app.secret_key = b'_+#y9L"F4O8o\n\xec]/'
switch = True


@app.route('/')
def homepage():
    questions = data_manager.last_5_questions()
    if 'username' in session:
        return render_template('index.html', questions=questions, user=escape(session['username']))
    else:
        return render_template('index.html', questions=questions)


@app.route('/list', methods=['GET', 'POST'])
def list():
    global switch
    if request.method == 'POST' and switch:
        switch = False
        return redirect('/list')
    elif request.method == 'POST' and not switch:
        switch = True
        return redirect('/list')
    if switch:
        questions = data_manager.title_order_by_asc()
    else:
        questions = data_manager.title_order_by_desc()
    return render_template('list.html', questions=questions)


@app.route('/all-users')
def all_users_data():
    all_users = data_manager.all_user_data()
    return render_template('all-users.html', all_users=all_users)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if 'username' in session:
        if request.method == 'POST':
            data_manager.save_question(request.form['Your Question'], request.form['Your Comment'], escape(session['username']))
            return redirect('/')
        return render_template('add-question.html')
    else:
        return redirect('/')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id=None):
    if 'username' in session:
        if request.method == 'POST':
            data_manager.save_answer(question_id, request.form['note'], escape(session['username']))
            return redirect(f'/question/{question_id}')
        return render_template('new-answer.html', question_id=question_id)
    else:
        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id=None, username=None):
    if 'username' in session:
        username = escape(session['username'])
    questions = data_manager.title_order_by_desc()
    answers = data_manager.get_answers()
    if request.method == 'POST':
        data_manager.view_num(question_id)
        return redirect(f'/question/{question_id}')
    return render_template('question.html', question_id=int(question_id), questions=questions, answers=answers, user=username)


@app.route('/question/<question_id>/up_vote')
def question_up_vote(question_id=None):
    data_manager.question_up_vote(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<answer_id>/up_vote')
def answer_up_vote(answer_id=None, question_id=None):
    data_manager.answer_up_vote(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/delete')
def delete_question(question_id=None):
    if 'username' in session:
        user = escape(session['username'])
        data_manager.delete_question(question_id, user)
        return redirect('/')
    else:
        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<answer_id>/delete')
def delete_question(question_id=None, answer_id=None):
    if 'username' in session:
        user = escape(session['username'])
        data_manager.delete_answer(answer_id, user)
        return redirect(f'/question/{question_id}')
    else:
        return redirect(f'/question/{question_id}')


@app.route('/<username>')
def user_page(username=None):
    if 'username' in session:
        username = escape(session['username'])
        questions = data_manager.title_order_by_asc()
        return render_template('user_page.html', user=username, questions=questions)
    else:
        return redirect('/')


@app.route('/registrator', methods=['GET', 'POST'])
def registration():

    if 'username' not in session:
        if request.method == 'POST':
            name = request.form["username"]
            password = request.form["password"]
            password1 = request.form["password1"]
            if password == password1 and not data_manager.check_user_name(name):
                hashed_password = password_hash.hash_password(password)
                data_manager.register_user(name, hashed_password)
                session['username'] = name
                return redirect('/')
            else:
                return render_template('password.html', wrong_user_info=True)
        else:
            return render_template('password.html', wrong_user_info=False)
    else:
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' not in session:
        if request.method == 'POST':
            name = request.form["username"]
            password = request.form["password"]
            if data_manager.get_user_data(name) \
                    and password_hash.verify_password(password, data_manager.get_user_data(name)[0]['hashed_password']) == True:
                session['username'] = name
                return redirect('/')
            else:
                return render_template('login.html')
        return render_template('login.html')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
