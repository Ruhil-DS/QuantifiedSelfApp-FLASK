from .database import db

'''
In this file, we have all the necessary models to link with the database file.
We are extending the existing db.Model class with our user defined classes.
Each table has its own class.
We are defining the table name, attributes of the table along with the constraints.
'''


class USER(db.Model):
    __tablename__ = "user"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)  # Of no use yet, but can be used while implementing "forgot password?" functionality
    creation = db.Column(db.String)  # Date of creation of the user.


class TRACKER(db.Model):
    __tablename__ = "tracker"
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    name = db.Column(db.String)
    type = db.Column(db.String)
    last_log = db.Column(db.String, default='Not yet logged!')  # For storing the timestamp of last logged value in the tracker


class USER_TRACKER(db.Model):  # Links user and tracker together
    __tablename__ = "user_tracker"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, db.ForeignKey(USER.username), nullable=False)
    tracker_id = db.Column(db.Integer, db.ForeignKey(TRACKER.tracker_id), nullable=False)


class STREAK(db.Model): # Additional feature; Each user will have a streak count.
    __tablename__ = "streak"
    streak_id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    username = db.Column(db.String, db.ForeignKey(USER.username), nullable=False, unique=True)
    date = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer)  # Default is 1, which has been implemented in the code, when a user signs up.


class TRACKER_BOOL(db.Model):  # For tracker type = boolean
    __tablename__ = "tracker_bool"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey(TRACKER.tracker_id), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String)


class TRACKER_NUM(db.Model):  # For tracker type = numerical
    __tablename__ = "tracker_num"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey(TRACKER.tracker_id), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String)


class TRACKER_TD(db.Model):  # For tracker type = time duration
    __tablename__ = "tracker_td"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey(TRACKER.tracker_id), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    time_start = db.Column(db.String, nullable=False)
    time_end = db.Column(db.String, nullable=False)
    note = db.Column(db.String)


class TRACKER_MC(db.Model):  # For tracker type = multi choice
    __tablename__ = "tracker_mc"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey(TRACKER.tracker_id), nullable=False)
    timestamp = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    note = db.Column(db.String)


class MULTI_CHOICES(db.Model):  # For storing all the choices for tracker type = multi choice
    __tablename__ = "multi_choices"
    tracker_id = db.Column(db.Integer, db.ForeignKey(TRACKER.tracker_id), nullable=False, primary_key=True)
    choices = db.Column(db.String)


# Finally, committing everything to the DB
db.session.commit()
