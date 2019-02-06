from flask import redirect, render_template, request, session
from main_ok import app
from main_ok.models import User, Vote, Answer, Association
from main_ok.forms import UserForm, VoteForm, LoginForm


@app.route('/', methods=['GET'])
def main():
    return redirect('/login')


@app.route('/registration', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        if User.is_free(form.login.data):
            user = User(form.name.data, form.login.data, form.password.data)
            user.save()
            return redirect('/login')
        else:
            form.login.errors = ('Логин занят', '')
    return render_template('registration.html', form=form)


@app.route('/vote_creation', methods=['GET', 'POST'])
def add_vote():
    form = VoteForm()

    user_name = User.get_name(session['id'])
    if user_name == '':
        return redirect('/login_error')

    if request.method == 'POST':
        if form.add.data:
            form.answers.append_entry()
        elif form.dela.data:
            form.answers.pop_entry()
        else:
            title = form.title.data  # Название вопроса
            description = form.description.data  # Описание вопроса
            answers = form.answers.data  # Массив вариантов ответов
            author_id = session['id']  # ID пользователя
            radio_checkbox = form.radio_checkbox.data
            vote = Vote(title, description, author_id, radio_checkbox)
            v_id = vote.save()
            for ans in answers:
                new = Answer(ans, v_id)
                new.save()
            return redirect('/vote_creation')

    return render_template('vote_creation.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['id'] = ''
    form = LoginForm()
    if request.method == 'POST':
        if User.check(form.login.data, form.password.data):
            session['id'] = User.get_id(form.login.data)
            return redirect('/main_page')
        else:
            form.password.errors = ('Wrong login or password', '')
    return render_template('Log_In.html', form=form)


def comp(vote):
    answer_list = Vote.get_answers(vote.id)
    all_votes = 0
    for ans in answer_list:
        all_votes += ans.number_of_votes
    return -all_votes


@app.route('/login_error', methods=['GET', 'POST'])
def login_error():
    session['id'] = ''
    form = LoginForm()
    if request.method == 'POST':
        if User.check(form.login.data, form.password.data):
            session['id'] = User.get_id(form.login.data)
            return redirect('/main_page')
        else:
            form.password.errors = ('Wrong login or password', '')
    return render_template('login_error.html', form=form)


@app.route('/main_page', methods=['GET'])
def votes():
    user_name = User.get_name(session['id'])
    vote_list = Vote.get_all()
    vote_list.sort(key=comp)
    return render_template('Main_page.html', vote_list=vote_list, user_name=user_name)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    p = None
    print(request.args)
    for arg in request.args.values():
        print(arg)
        if arg.isdigit():
            p = Answer.add_vote(int(arg))

    a = Association(session['vote_id'], session['id'])
    a.save()

    return redirect('/vote_after/' + session['vote_id'])


@app.route('/vote/<vote_id>', methods=['GET'])
def voting(vote_id):
    session['vote_id'] = vote_id

    if Association.check(session['id'], vote_id):
        return redirect('/vote_after/' + str(vote_id))

    if len(request.args) > 0:
        return vote()

    ans_list = Vote.get_for_id(vote_id)
    ans_list.author_id = User.get_login(ans_list.author_id)

    user_name = User.get_name(session['id'])
    if user_name == '':
        return redirect('/vote_after/' + str(vote_id))

    if ans_list.radio_checkbox == 0:
        return render_template('Vote_for_user_checkbox.html', user_name=user_name, ans_list=ans_list)
    else:
        return render_template('Vote_for_users_radio.html', user_name=user_name, ans_list=ans_list)


@app.route('/User_account', methods=['GET'])
def user_votes():
    user_name = User.get_name(session['id'])
    if user_name == '':
        return redirect('/login_error')

    user_name = User.get_name(session['id'])
    vote_list = User.get_votes(session['id'])

    return render_template('User_account.html', vote_list=vote_list, user_name=user_name)


@app.route('/vote_after/<vote_id>', methods=['GET'])
def get_results(vote_id):
    user_name = User.get_name(session['id'])
    form = Vote.get_for_id(vote_id)
    answer_list = Vote.get_answers(vote_id)
    all_votes = 0
    for ans in answer_list:
        all_votes += ans.number_of_votes
    if all_votes == 0:
        all_votes = 1
    return render_template('Vote_after.html', form=form, answer_list=answer_list, all_votes=all_votes, user_name=user_name)


@app.route('/About_us', methods=['GET', 'POST'])
def about_us():
    return render_template('About_us.html')

