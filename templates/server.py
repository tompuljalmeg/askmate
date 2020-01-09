from flask import Flask, render_template, redirect, request
import data_manager

app = Flask(__name__)


@app.route('/')
def route_index():
    table = data_manager.question_list()
    return render_template('list.html', table=table)


@app.route('/question/<question_id>')
def route_question(question_id=None):
    table = data_manager.question_list()
    answers = data_manager.answer_list()
    return render_template('question.html', question_id=question_id, table=table, answers=answers)


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    saved_question = []
    if request.method == 'POST':
        saved_question.append(request.form['Your Question'])
        saved_question.append(request.form['Your Comment'])
        data_manager.save_question(saved_question)
        return redirect('/')
    return render_template('add-question.html')


@app.route('/question/<question_id>/new-answer')
def route_new_answer():
    return render_template('new-answer.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)