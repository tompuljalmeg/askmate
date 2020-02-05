from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)
switch = True


@app.route('/')
def all_questions():
    questions = data_manager.last_5_questions()
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


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question ():
    if request.method == 'POST':
        data_manager.save_question(request.form['Your Question'], request.form['Your Comment'])
        return redirect('/')
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id=None):
    if request.method == 'POST':
        data_manager.save_answer(question_id, request.form['note'])
        return redirect(f'/question/{question_id}')
    return render_template('new-answer.html', question_id=question_id)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id=None):
    questions = data_manager.title_order_by_desc()
    answers = data_manager.get_answers()
    if request.method == 'POST':
        data_manager.view_num(question_id)
        return redirect(f'/question/{question_id}')
    return render_template('question.html', question_id=int(question_id), questions=questions, answers=answers)


@app.route('/question/<question_id>/up_vote')
def question_up_vote(question_id=None):
    data_manager.question_up_vote(question_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/<answer_id>/up_vote')
def answer_up_vote(answer_id=None, question_id=None):
    data_manager.answer_up_vote(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/registrator', methods=['GET', 'POST'])
def registration():

    return render_template('password.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)