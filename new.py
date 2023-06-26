import time
from win10toast import ToastNotifier
import threading

def get_total_time(task_name):
    try:
        with open(f"{task_name}_time.txt", "r") as file:
            total_time = int(file.read())
        return total_time
    except FileNotFoundError:
        return 0

def record_time(task_name, total_time):
    with open(f"{task_name}_time.txt", "w") as file:
        file.write(str(total_time))

def start_timer(task_name, last_activity_time):
    task_name = task_name.capitalize()
    previous_time = get_total_time(task_name)
    start_time = time.time()
    print(f"Started {task_name} timer.")
    toaster = ToastNotifier()
    notification_title = f"Task Started"
    notification_message = f"{task_name} timer started ."
    toaster.show_toast(notification_title, notification_message, duration=3)
    input("Press Enter to stop : ")
    end_time = time.time()
    time_spent = round(end_time - start_time, 2)
    total_time = previous_time + int(time_spent)
    record_time(task_name, total_time)
    print(f"Time spent on {task_name}: {time_spent} seconds ({time_spent / 60:.2f} minutes).")
    print(f"Total {task_name} time: {total_time} seconds ({total_time / 60:.2f} minutes).")
    last_activity_time[0] = end_time  # Update last_activity_time
    return total_time

def show_total_time():
    programming_time = get_total_time("programming")
    break_time = get_total_time("break")
    print(f"Total programming time: {programming_time} seconds ({programming_time / 60:.2f} minutes).")
    print(f"Total break time: {break_time} seconds ({break_time / 60:.2f} minutes).")

def check_exceeded_time(task_name, max_hours):
    total_time = get_total_time(task_name)
    if total_time > max_hours * 60 * 60:
        toaster = ToastNotifier()
        notification_title = f"{task_name.capitalize()} Time Exceeded"
        notification_message = f"Total {task_name} time exceeded {max_hours} hours!"
        toaster.show_toast(notification_title, notification_message, duration=20)

def show_no_activity_notification(last_activity_time):
    while True:
        current_time = time.time()
        elapsed_time = current_time - last_activity_time[0]
        if elapsed_time > 10 * 60:
            last_activity_time[0] = current_time
            toaster = ToastNotifier()
            notification_title = "REMINDER !!!"
            notification_message = "Are you focusing on your TASK right now ?"
            toaster.show_toast(notification_title, notification_message, duration=500)

def main():
    programming_max_hours = 8
    break_max_hours = 3
    last_activity_time = [time.time()]  # Store last_activity_time in a list

    activity_monitor_thread = threading.Thread(target=show_no_activity_notification, args=(last_activity_time,))
    activity_monitor_thread.start()

    while True:
        command = input("Enter command ('started programming', 'started break', 'show time', or 'stop'): ").lower()  # Convert command to lowercase
        current_time = time.time()

        if command == "started programming":
            total_time = start_timer("programming", last_activity_time)
            check_exceeded_time("programming", programming_max_hours)
        elif command == "started break":
            total_time = start_timer("break", last_activity_time)
            check_exceeded_time("break", break_max_hours)
        elif command == "show time":
            print(current_time - last_activity_time[0])
            show_total_time()
        elif command == "stop":
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
