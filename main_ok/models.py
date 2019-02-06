from main_ok import app, db
from flask import session

# association_table = db.Table('association', db.metadata,
#                              db.Column('left_id', db.Integer, db.ForeignKey('left.id')),
#                              db.Column('right_id', db.Integer, db.ForeignKey('right.id'))
#                              )


class User(db.Model):
    __tablename__ = 'left'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    login = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=True, nullable=False)

    # votes = db.relationship('Vote', backref='author', lazy='dynamic')

    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def check(login, password):
        u = User.query.filter_by(login=login, password=password).first()
        return u is not None

    @staticmethod
    def is_free(login):
        u = User.query.filter_by(login=login).first()
        return u is None

    @staticmethod
    def get_id(login):
        u = User.query.filter_by(login=login).first().id
        return u

    @staticmethod
    def get_login(id):
        u = User.query.filter_by(id=id).first().login
        return u

    @staticmethod
    def get_votes(id):
        u = User.query.filter_by(id=id).first().votes
        return u

    @staticmethod
    def get_name(id):
        u = User.query.filter_by(id=id).first()
        if u is None:
            return ''
        return u.name


class Vote(db.Model):
    __tablename__ = 'right'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('left.id'))
    number_of_votes = db.Column(db.Integer)
    # already_voted = db.relationship("User", secondary=association_table, backref='right')
    radio_checkbox = db.Column(db.Integer)
    # answers = db.relationship("Answer", backref="vote_object")
    owner = db.relationship("User", backref=db.backref('votes', lazy='joined'))

    def __init__(self, title, description, author_id, radio_checkbox):
        self.title = title
        self.description = description
        self.author_id = author_id
        self.radio_checkbox = radio_checkbox

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_all():
        return Vote.query.all()

    @staticmethod
    def get_for_select_field():
        vote_list = Vote.get_all()
        select_field_options = []
        for vote in vote_list:
            information = "{0} ({1}) {2} {3} {4} {5}".format(vote.title,
                                                             vote.description,
                                                             vote.author,
                                                             vote.number_of_votes,
                                                             vote.already_voted,
                                                             vote.variants)
            option = (str(Vote.id), information)
            select_field_options.append(option)
        return select_field_options

    @staticmethod
    def get_for_id(id):
        return Vote.query.filter_by(id=id).first()

    @staticmethod
    def get_answers(id):
        return Vote.query.filter_by(id=id).first().answers


class Answer(db.Model):
    __tablename__ = 'third'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    variant = db.Column(db.String(256), nullable=False)
    number_of_votes = db.Column(db.Integer)

    vote_id = db.Column(db.Integer, db.ForeignKey('right.id'))
    vote = db.relationship("Vote", backref=db.backref('answers', lazy='joined'))

    def __init__(self, variant, vote_id):
        self.variant = variant
        self.vote_id = vote_id
        self.number_of_votes = 0

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def add_vote(id):
        a = Answer.query.filter_by(id=id).first()
        a.number_of_votes += 1
        db.session.commit()
        return a

    @staticmethod
    def results(id):
        a = Answer.query.filter_by(id=id).first()
        return a.number_of_votes


class Association(db.Model):
    __tablename__ = 'association'
    left_id = db.Column(db.Integer, db.ForeignKey('left.id'), primary_key=True)
    right_id = db.Column(db.Integer, db.ForeignKey('right.id'), primary_key=True)
    voter = db.relationship('User', backref=db.backref('already_voted', lazy='joined'))
    voting = db.relationship('Vote', backref=db.backref('already_voted', lazy='joined'))

    def __init__(self, user, vote):
        self.left_id = user
        self.right_id = vote

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check(u_id, v_id):
        print(u_id, v_id)
        a = Association.query.filter_by(left_id=v_id, right_id=u_id).first()
        return a is not None
