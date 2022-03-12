import matplotlib
import matplotlib.pyplot as plt
from .models import *
from .timestamp import *
'''
Here are all the functions used to plot the graph and save them in png format in the static/images/ folder
Used matplotlib to do so.
graphs mainly include line plot, bar graphs, scatter plots.
'''
matplotlib.use('Agg')


def plot_homepage(si_un):
    user_trackers = USER_TRACKER.query.filter_by(username=si_un).all()
    num_count, bool_count, td_count, mc_count = 0, 0, 0, 0
    for i in user_trackers:
        trackers = TRACKER.query.filter_by(tracker_id=i.tracker_id).all()
        for tracker in trackers:
            if tracker.type == 'bool':
                bool_count += 1
            elif tracker.type == 'num':
                num_count += 1
            elif tracker.type == 'time_dur':
                td_count += 1
            elif tracker.type == 'mc':
                mc_count += 1
    x = ["num", "bool", "time_dur", "mc"]
    y = [num_count, bool_count, td_count, mc_count]
    c = ['magenta', '#38b6ff', 'teal', 'orange']
    x_label = plt.xlabel("Tracker Types")
    y_label = plt.ylabel("Number of trackers")
    title = plt.title("Summary of your Trackers")

    y_range = [i for i in range(0, 100)]
    plt.yticks(y_range)
    fig = plt.bar(x, y, color=c)
    filename_path = "static/images/homepage_" + str(si_un) + ".png"
    plt.savefig(filename_path)
    plt.close()

    return filename_path


def plot_numTracker(tracker_id, logs):
    x_list = []
    y_list = []
    values = {}
    for log in logs:
        datetime_obj = convert_datetime(log.timestamp)
        values[datetime_obj] = log.value

    for key in sorted(values):
        x_list.append(key)
        y_list.append(values[key])

    x_label = plt.xlabel("TIMESTAMP")
    y_label = plt.ylabel("VALUE LOGGED")
    title = plt.title("Summary of your Logs")
    plt.xticks(rotation=45)
    plt.tight_layout()
    fig = plt.plot(x_list, y_list, color='red')
    filename_path = "static/images/num_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path)
    plt.close()

    return filename_path


def plot_BoolTracker(tracker_id, logs):

    true_count = 0
    false_count = 0
    scatter_x = []
    scatter_y = []
    for log in logs:
        datetime_obj = convert_datetime(log.timestamp)
        scatter_x.append(datetime_obj)
        scatter_y.append(log.value)

        if log.value == 'True':
            true_count += 1

        elif log.value == 'False':
            false_count += 1

    x_list = ["True", "False"]
    y_list = [true_count, false_count]

    x_label = plt.xlabel("Value")
    y_label = plt.ylabel("Frequency")
    title = plt.title("Summary of your Logs")

    plt.subplot(2, 1, 1)
    y_range = [i for i in range(0, 100)]
    plt.yticks(y_range)
    plt.bar(x_list, y_list, color=['lightsteelblue', 'coral'], width=0.4)

    plt.subplot(2, 1, 2)
    plt.xticks(rotation=45)
    plt.scatter(scatter_x, scatter_y, color='teal')
    plt.tight_layout()
    filename_path = "static/images/bool_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path)
    plt.close()

    return filename_path


def plot_mcTracker(tracker_id, logs):
    logs = TRACKER_MC.query.filter_by(tracker_id=tracker_id).all()
    choices_record = MULTI_CHOICES.query.filter_by(tracker_id=tracker_id).first()
    choices = choices_record.choices.split(",")

    choices_dict = {}
    for choice in choices:
        choices_dict[choice] = 0

    for log in logs:
        choice_selected = (log.value).split(",")
        for i in choice_selected:
            choices_dict[i] += 1

    x_list = list(choices_dict.keys())
    y_list = list(choices_dict.values())

    x_label = plt.xlabel("Choices")
    y_label = plt.ylabel("#selected")
    title = plt.title("Summary of your Logs")

    # plt.xticks(rotation=45)
    # plt.tight_layout()
    y_range = [i for i in range(0, 100)]
    plt.yticks(y_range)
    plt.bar(x_list, y_list,
            color=['firebrick', 'palegreen', 'teal', 'cyan', 'orange', 'deeppink', 'lightcoral', 'cornflowerblue'])

    filename_path = "static/images/mc_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path)
    plt.close()

    return filename_path


def plot_tdTracker(tracker_id, logs):
    x_list = []
    y_list = []
    for log in logs:
        time_diff_obj = (convert_datetime(log.time_end) - convert_datetime(log.time_start))

        difference = float(time_diff_obj.total_seconds() / 60)

        datetime_obj = convert_datetime(log.timestamp)

        x_list.append(datetime_obj)
        y_list.append(difference)

    x_label = plt.xlabel("Timestamp")
    y_label = plt.ylabel("Time duration (Minutes)")
    title = plt.title("Summary of your Logs")

    plt.xticks(rotation=45)

    plt.scatter(x_list, y_list, color='red')
    plt.tight_layout()

    filename_path = "static/images/td_tracker_" + str(tracker_id) + ".png"
    plt.savefig(filename_path)
    plt.close()

    return filename_path
