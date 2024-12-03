import zmq
from datetime import datetime
import time

def get_stats(timeframe, data):
    activities = 0
    distance = 0
    time = 0
    elevation_gain = 0
    # if time == "MONTH":
    #     current_date = datetime.now().date()
    #     for activity in data:
    #         activity_date = datetime.strptime(activity['date'], '%Y-%m-%s')
    #         if current_date (activity_date - current_date).days <= 28:
    #             activities += 1
    #             distance += data['distance']
    #             time += data['duration']
    #             elevation_gain += data['elevation']
    if timeframe == "YEAR":
        current_year = datetime.now()
        current_year_str = current_year.strftime("%Y")
        for activity in data:
            if activity['date'][0:4] == current_year_str:
                activities += 1
                distance += activity['distance']
                time += activity['duration']
                elevation_gain += activity['elevation']

    if timeframe == "ALL":
        for activity in data:
            activities += 1
            distance += activity['distance']
            time += activity['duration']
            elevation_gain += activity['elevation']

    return {'activities': activities, 'distance': distance, 'duration': time, 'elevation': elevation_gain}
def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("Listening for requests...")
    while True:
        request = socket.recv_json()
        stats = get_stats(request['time'], request['data'])
        print(f"Retrieving {request['time']} stats...")
        socket.send_json(stats)

if __name__ == '__main__':
    main()