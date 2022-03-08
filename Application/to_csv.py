import csv
from .timestamp import *  # current time stamp
from flask import send_file

'''
A function to write all the logs to a csv file and return the send_file() function of FLASK, which is used to send
files to the client.

CSV file has a filename of log_{{tracker_type}}_{{timestamp}}, where timestamp is the time of downloading the log!

CSV is created and stored in the folder static/logs_download/
CSV file is also deleted after it has been sent to the client. This has been implemented in the controller. 
'''


def log_export(tracker_type, logs):  # tracker_Type and all the logs are given as the parameters
    filename = "log_" + tracker_type + "_" + current_timestamp() + ".csv"  # defining the file name
    with open("static/logs_download/"+filename, 'w', newline='') as log_file:
        csv_writer = csv.writer(log_file, delimiter=',')  # Creating a CSV writer object.
        if tracker_type == 'time_dur':
            # First, writing the header of the CSV file, i.e., all the titles.
            # This is different for time_dur tracker type and for all other trackers!
            csv_writer.writerow(['log_id', "tracker_id", "timestamp", "start_time", "end_time", "note"])
            for log in logs:  # Iterating through the logs, and then writing them to the csv file
                csv_writer.writerow([log.log_id, log.tracker_id, log.timestamp, log.time_start, log.time_end, log.note])
        else:
            csv_writer.writerow(['log_id', "tracker_id", "timestamp", "value", "note"])
            for log in logs:
                csv_writer.writerow([log.log_id, log.tracker_id, log.timestamp, log.value, log.note])

    # returning the send_file method of FLASK and the filename(used while deleting the file from the server)
    return send_file('static/logs_download/'+filename,
                     mimetype='text/csv',
                     as_attachment=True), filename