from flask import render_template
from flask import request, redirect
from flask import session, url_for
from flask import current_app as app
from .models import *
from .controller_index import *
from .graph import *
from .timestamp import *
import matplotlib.pyplot as plt
from .to_csv import *
import os
import datetime

'''
This file contains all the dashboard related actions!
from signin to signout, from viewing trackers to deleting them
from adding logs to deleting them, everything!

'''


@app.route("/signin-up/", methods=['GET', 'POST'])
def signin_up():  # A function to signin or sign up the user. Streak count, sessions are maintained here.
    if request.method == 'GET':  # displays the signin/up page or redirects to the dashbaord.
        if "username" in session:
            return redirect("/dashboard/")
        return render_template("signup.html")
    if request.method == 'POST':  # If POST, then either signs in or signs up the user, according to the details received.
        try:  # Trying to sign in
            si_un = request.form['si_un'].lower()
            si_ps = request.form['si_ps']
            validity = USER.query.filter_by(username=si_un, password=si_ps).first()

            if validity is not None:
                session['username'] = si_un  # Storing sign-in username in the session!

                # Handling streak for the user
                streak_data = STREAK.query.filter_by(username=si_un).first()
                # If difference has '1 day' in it, then ->
                if '1 day' in str(datetime.datetime.today() - datetime.datetime.strptime(streak_data.date, '%Y-%m-%d')):
                    streak_data.date = datetime.date.today()
                    streak_data.count += 1  # Add 1 to last streak count
                    db.session.commit()
                # else if difference has 'days' in it, then the streak has been broken. So ->
                elif 'days' in str(
                        datetime.datetime.today() - datetime.datetime.strptime(streak_data.date, '%Y-%m-%d')):
                    streak_data.date = datetime.date.today()
                    streak_data.count = 1  # Reset to 1
                    db.session.commit()
                else:
                    pass

                return redirect("/dashboard/")  # After updating streak, redirect to the dashboard

            elif validity is None:  # If validity fails, render signin-up page with error message
                return render_template('signup.html', error="Incorrect")

        except:  # else, it retrieves the sign-up information.
            su_un = request.form['su_un'].lower()
            su_ps = request.form['su_ps']
            su_email = request.form['su_email']

            # Creation_date() function from timestamp.py, returns today's date
            creation_date = date_today()

            try:  # Try to add a user to the db
                new_user = USER(username=su_un, password=su_ps, email=su_email, creation=creation_date)
                streak_data = STREAK(username=su_un, date=date.today(), count=1)
                db.session.add(new_user)
                db.session.add(streak_data)
                db.session.commit()
            except:  # if anything fails, it renders the signup page with an error
                db.session.rollback()  # Roll-back just in case anything was changed
                return render_template('signup.html', error='failed')

            return render_template('signup.html', error='success')  # at last, if everything works,
            # it renders the signin/up page with a message saying successful signup


@app.route("/dashboard/", methods=['GET'])
def dashboard(): # Renders the dashboard according to the session.
    if "username" in session:
        si_un = session['username']
        # Streak count ->
        streak = STREAK.query.filter_by(username=si_un).first().count
        # ----------------------

        # Tracker count ->
        trackers = USER_TRACKER.query.filter_by(username=si_un).distinct()
        tracker_count = 0
        for i in trackers:
            tracker_count += 1
        # ----------------------

        # member since ->
        member_create = USER.query.filter_by(username=si_un).first()
        member_since = str(datetime.datetime.today() - datetime.datetime.strptime(member_create.creation, '%Y-%m-%d'))
        member_since = member_since.split(",")
        member_since = member_since[0]
        # ----------------------

        # List of trackers ->
        tracker_ids = USER_TRACKER.query.filter_by(username=si_un).distinct()
        trackers = []
        for t_id in tracker_ids:
            trackers.append(TRACKER.query.filter_by(tracker_id=t_id.tracker_id).first())
        # ----------------------

        # Trend line graph ->
        filename_path = plot_homepage(si_un=si_un)  # Function from graph.py
        # ----------------------
        return render_template("dashboard.html", user=si_un, streak=streak, tracker_count=tracker_count,
                               member_since=member_since, trackers=trackers, filename_path=filename_path)

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect('/signin-up/')


@app.route("/view_trackers/", methods=['GET'])
def view_trackers():
    # ----------------------
    # shows all the trackers with their details at the mentioned URI.
    # Filters the trackers according to the username(sign in user-name)
    # ----------------------
    if "username" in session:
        si_un = session['username']
        tracker_ids = USER_TRACKER.query.filter_by(username=si_un).distinct()
        trackers = []
        for tid in tracker_ids:
            trackers.append(TRACKER.query.filter_by(tracker_id=tid.tracker_id).first())

        return render_template("view_trackers.html", trackers=trackers, user=si_un)
    else:
        return redirect('/signin-up/')


@app.route("/create/", methods=['GET', 'POST'])
def create_tracker():
    # ----------------------
    # Creates a new tracker.
    # uses GET and POST methods.
    # ----------------------
    if "username" in session:
        si_un = session['username']

        if request.method == 'GET':
            return render_template("add_tracker.html", user=si_un)

        if request.method == 'POST':
            try:
                tracker_name = request.form['tracker_name']
                tracker_type = request.form['tracker_type']
                tracker_desc = request.form['tracker_desc']

                tracker_record = TRACKER(name=tracker_name, description=tracker_desc, type=tracker_type)
                db.session.add(tracker_record)
                db.session.commit()

                if tracker_type == 'mc':
                    # ----------------------
                    # When the tracker type is multi choice, add those choices to the MULTI_CHOICE table
                    # ----------------------
                    mc_choices = request.form['mc_choices']
                    mc_record = MULTI_CHOICES(tracker_id=tracker_record.tracker_id, choices=mc_choices)
                    db.session.add(mc_record)

                # ----------------------
                # Link the user with the tracker ID in the USER_TRACKER table
                # ----------------------
                user_tracker_record = USER_TRACKER(username=si_un, tracker_id=tracker_record.tracker_id)

                db.session.add(user_tracker_record)
                db.session.commit()
            except:
                # ----------------------
                # If by any chance, something goes wrong(on the user or client side), this throws an error!
                # ----------------------
                return render_template("add_tracker.html", error='Incorrect', user=si_un)

            return redirect("/dashboard/")

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up/")


@app.route("/<string:tracker_id>/log/", methods=['GET', 'POST'])
def add_log(tracker_id):
    # ----------------------
    # adding a log to the tracker!
    # ----------------------
    if "username" in session:
        si_un = session['username']
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
        choices = None
        if tracker.type == 'mc':
            choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
            choices = choices_record.choices.split(",")
        if request.method == 'GET':
            return render_template("add_log.html", tracker_id=tracker_id, tracker=tracker, choices=choices, user=si_un,
                                   time_value=current_timestamp())

        elif request.method == 'POST':
            note = None
            timestamp = request.form['tracker_timestamp']
            note = request.form['note']

            if tracker.type == 'num':
                tracker_value = request.form['tracker_value']
                if note is not None:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value, note=note)
                else:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value)
                db.session.add(record)
                db.session.commit()

            elif tracker.type == 'time_dur':
                tracker_value_start = request.form['tracker_value_start']
                tracker_value_end = request.form['tracker_value_end']
                if note is not None:
                    record = TRACKER_TD(tracker_id=tracker_id, timestamp=timestamp,
                                        note=note, time_start=tracker_value_start,
                                        time_end=tracker_value_end)
                else:
                    record = TRACKER_TD(tracker_id=tracker_id, timestamp=timestamp,
                                        time_start=tracker_value_start,
                                        time_end=tracker_value_end)
                db.session.add(record)
                db.session.commit()

            elif tracker.type == 'bool':
                tracker_value = request.form['tracker_value']
                if note is not None:
                    record = TRACKER_BOOL(tracker_id=tracker_id, timestamp=timestamp,
                                          value=tracker_value, note=note)
                else:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value)
                db.session.add(record)
                db.session.commit()

            elif tracker.type == 'mc':
                tracker_values_list = request.form.getlist('tracker_value')
                tracker_value = ""
                for i in range(len(tracker_values_list)):
                    if i != len(tracker_values_list) - 1:
                        tracker_value += str(tracker_values_list[i]) + ","
                    else:
                        tracker_value += str(tracker_values_list[i])

                if note is not None:
                    record = TRACKER_MC(tracker_id=tracker_id, timestamp=timestamp,
                                        value=tracker_value, note=note)
                else:
                    record = TRACKER_NUM(tracker_id=tracker_id, timestamp=timestamp,
                                         value=tracker_value)
                db.session.add(record)
                db.session.commit()
            tracker.last_log = timestamp
            db.session.commit()

            return redirect("/dashboard/")

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up/")


@app.route("/<string:tracker_id>/update/", methods=['GET', 'POST'])
def update_tracker(tracker_id):
    # ----------------------
    # updating the tracker
    # ----------------------
    if "username" in session:
        si_un = session['username']
        choices = ""
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
        if tracker.type == 'mc':
            choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
            choices = choices_record.choices.split(",")

        if request.method == 'GET':
            return render_template("update_tracker.html", user=si_un, tracker=tracker, choices=choices)

        elif request.method == 'POST':
            try:
                tracker_name = request.form['tracker_name_updated']
                tracker_desc = request.form['tracker_desc_updated']

                old_record = TRACKER.query.filter_by(tracker_id=tracker_id).first()
                old_record.name = tracker_name
                old_record.description = tracker_desc
                db.session.commit()
            except:
                return render_template("update_tracker.html", error='Incorrect', user=si_un)
            return redirect("/dashboard/")

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up/")


# ----------------------
# deleting the tracker
# ----------------------
@app.route("/<string:tracker_id>/delete/", methods=['GET'])
def delete_tracker(tracker_id):
    if "username" in session:
        si_un = session['username']
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
        if tracker.type == 'num':
            try:
                records = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).delete()
            except:
                pass
            user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            db.session.commit()

        elif tracker.type == 'bool':
            try:
                records = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).delete()
            except:
                pass
            user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            db.session.commit()

        elif tracker.type == 'mc':
            try:
                records = TRACKER_MC.query.filter_by(tracker_id=tracker_id).delete()
                mc_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).delete()
            except:
                pass
            user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            db.session.commit()

        else:
            try:
                records = TRACKER_TD.query.filter_by(tracker_id=tracker_id).delete()
            except:
                pass
            user_records = USER_TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            tracker = TRACKER.query.filter_by(tracker_id=tracker_id).delete()
            db.session.commit()
        # plot_homepage(si_un=si_un)
        return redirect("/dashboard/")

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up")


# ----------------------
# Shows the tracker details.
# ----------------------
@app.route("/<int:tracker_id>/details/")
def tracker_details(tracker_id):
    if "username" in session:
        si_un = session['username']
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()

        if tracker.type == 'num':
            logs = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).all()
            filename_path = plot_numTracker(tracker_id, logs)

        elif tracker.type == 'bool':
            logs = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).all()
            filename_path = plot_BoolTracker(tracker_id, logs)

        elif tracker.type == 'time_dur':
            logs = TRACKER_TD.query.filter_by(tracker_id=tracker_id).all()
            filename_path = plot_tdTracker(tracker_id, logs)

        elif tracker.type == 'mc':
            logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()
            filename_path = plot_mcTracker(tracker_id, logs)

        return render_template("view_tracker.html", logs=logs, tracker=tracker, user=si_un, filename_path=filename_path)

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up")


# ----------------------
# Updates the log
# ----------------------
@app.route("/<int:tracker_id>/<int:log_id>/update/", methods=['GET', 'POST'])
def update_log(log_id, tracker_id):
    if "username" in session:
        si_un = session['username']
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
        choices = None
        choices_marked = None

        if tracker.type == 'num':
            log = TRACKER_NUM.query.filter_by(log_id=log_id).first()
            logs = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).all()

        elif tracker.type == 'bool':
            log = TRACKER_BOOL.query.filter_by(log_id=log_id).first()
            logs = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).all()

        elif tracker.type == 'time_dur':
            log = TRACKER_TD.query.filter_by(log_id=log_id).first()
            logs = TRACKER_TD.query.filter_by(tracker_id=tracker_id).all()

        elif tracker.type == 'mc':
            log = TRACKER_MC.query.filter_by(log_id=log_id).first()
            logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()

            choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
            choices = choices_record.choices.split(",")
            choices_marked_record = TRACKER_MC.query.filter_by(log_id=log_id).first()
            choices_marked = choices_marked_record.value.split(",")

        if request.method == 'GET':
            return render_template("update_log.html", tracker=tracker, log=log, choices=choices,
                                   choices_marked=choices_marked, user=si_un)

        if request.method == 'POST':
            tracker_timestamp_update = request.form['tracker_timestamp_update']

            if tracker.type == 'time_dur':
                tracker_value_start_update = request.form['tracker_value_start_update']
                tracker_value_end_update = request.form['tracker_value_end_update']
                note_update = request.form['note_update']

                log.time_start = tracker_value_start_update
                log.time_end = tracker_value_end_update
                log.note = note_update
                log.timestamp = tracker_timestamp_update
                db.session.commit()

            elif tracker.type == 'mc':
                tracker_values_update_list = request.form.getlist('tracker_value_update')
                print("-----------")
                print(tracker_values_update_list)
                print("-----------")
                note_update = request.form['note_update']
                tracker_value_update = ""
                for i in range(len(tracker_values_update_list)):
                    if i != len(tracker_values_update_list) - 1:
                        tracker_value_update += str(tracker_values_update_list[i]) + ","
                    else:
                        tracker_value_update += str(tracker_values_update_list[i])
                print("-----------")
                print(note_update)
                print("-----------")
                log.value = tracker_value_update
                log.timestamp = tracker_timestamp_update
                log.note = note_update
                db.session.commit()
                db.session.commit()


            else:
                tracker_value_update = request.form['tracker_value_update']
                note_update = request.form['note_update']

                log.value = tracker_value_update
                log.timestamp = tracker_timestamp_update
                log.note = note_update
                db.session.commit()
            path_to_details = '/{tracker_id}/details/'.format(tracker_id=tracker_id)
            return redirect(path_to_details)

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up")


# ----------------------
# To delete any log that the user has logged before
# ----------------------
@app.route("/<int:tracker_id>/<int:log_id>/delete/", methods=['GET'])
def delete_log(tracker_id, log_id):
    if "username" in session:
        si_un = session['username']
        tracker = TRACKER.query.filter_by(tracker_id=tracker_id).first()
        if tracker.type == 'num':
            log = TRACKER_NUM.query.filter_by(log_id=log_id).delete()

        elif tracker.type == 'bool':
            log = TRACKER_BOOL.query.filter_by(log_id=log_id).delete()

        elif tracker.type == 'time_dur':
            log = TRACKER_TD.query.filter_by(log_id=log_id).delete()

        elif tracker.type == 'mc':
            log = TRACKER_MC.query.filter_by(log_id=log_id).delete()

        db.session.commit()
        path_to_details = '/{tracker_id}/details/'.format(tracker_id=tracker_id)
        return redirect(path_to_details)

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up")


# ----------------------
# to download logs
# ----------------------
@app.route("/<int:tracker_id>/details/download/")
def download_logs(tracker_id):
    if "username" in session:
        si_un = session['username']
        try:
            user_check = USER_TRACKER.query.filter_by(tracker_id=tracker_id).first().username
            if user_check == si_un:
                tracker_type = TRACKER.query.filter_by(tracker_id=tracker_id).first().type
                if tracker_type == 'num':
                    logs = TRACKER_NUM.query.filter_by(tracker_id=tracker_id).all()

                elif tracker_type == 'bool':
                    logs = TRACKER_BOOL.query.filter_by(tracker_id=tracker_id).all()

                elif tracker_type == 'time_dur':
                    logs = TRACKER_TD.query.filter_by(tracker_id=tracker_id).all()

                elif tracker_type == 'mc':
                    logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()

                print("sending file......")
                result, filename = log_export(tracker_type, logs)
                print("file sent!", "\nNow, removing....")
                os.remove("static/logs_download/" + filename)
                return result
            else:
                return redirect("/log_error/")

        except:
            return redirect("/dashboard/")
    else:
        return redirect("/signin-up/")


@app.route("/log_error/")
def log_error():
    if "username" in session:
        return render_template("dashboard.html", log_error='true')

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up/")

# ----------------------
# Finally, to sign out
# ----------------------
@app.route("/signout/", methods=['GET'])
def signout():
    if "username" in session:
        si_un = session['username']
        session.pop("username", None)
        return render_template("signup.html", signout='true')

    else:  # If user is not in the session, redirect to login page. ((prevents direct access of URI)
        return redirect("/signin-up/")
