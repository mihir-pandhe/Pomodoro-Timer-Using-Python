import time

def pomodoro_timer(work_duration, break_duration):
    print("Pomodoro Timer Started!")
    while True:
        print("Work session started. Focus!")
        time.sleep(work_duration * 60)
        print("Work session ended. Take a break!")
        
        print("Break session started. Relax!")
        time.sleep(break_duration * 60)
        print("Break session ended. Get ready for the next session!")

if __name__ == "__main__":
    work_duration = int(input("Enter work duration in minutes: "))
    break_duration = int(input("Enter break duration in minutes: "))
    pomodoro_timer(work_duration, break_duration)
