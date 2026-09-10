from gtts import gTTS 
from playsound import playsound
import threading
import json
import time as tm
import time
from datetime import datetime

def speak(text):
    filename = "voice_" + str(int(time.time())) + ".mp3"
    tts = gTTS(text=text, lang="te", slow=True)
    tts.save(filename)
    playsound(filename)


try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []

def reminder():
    spoken = set()

    while True:
         now = datetime.now()
         current_time = now.strftime("%H:%M")
         current_date = now.strftime("%d-%m-%Y")
         for item in tasks:
             task = item["task"]
             task_time = item["time"]
             task_date = item["date"]
             repeat = item["repeat"]
             should_remind = False
             if repeat == "1":
                should_remind = True
             elif repeat =="2":
                 saved_date= datetime.strptime(task_date,"%d-%m-%Y")
                 should_remind = now.weekday() == saved_date.weekday()
             elif repeat =="3":
                 should_remind= (current_date == task_date)
             elif repeat =="4":
                 saved_date=datetime.strptime(task_date, "%d-%m-%Y")
                 should_remind= now.day == saved_date.day
             elif repeat =="5":
                 saved_date=datetime.strptime(task_date, "%d-%m-%Y")
                 should_remind= (now.month == saved_date.month and now.day ==now.day == saved_date.day)
                              
                                  
             if should_remind:    
                 if current_time == task_time and task_time not in spoken:
                     speak(f"{task} cheyalisina time ayyindi")
                     spoken.add(task_time)
             tm.sleep(1)
thread = threading.Thread(target=reminder, daemon=True)
thread.start()

while True:
    print("===============================================")
    print("            Smart Voice Planner                ")
    print("===============================================")

    print("1. Add New Task")
    print("2. View Tasks")
    print("3. Exit")
    print("4. Delete Task")
    print("5. Edit Task")
    choice = input("choose an option:")
    print(choice)
    if choice == "1":
        print("you selected add new Task")
        task = input("Enter your new task:")
        task_time = input("Enter time (HH:MM) AM/PM):")
        task_date = input("Enter date (DD-MM-YYYY):")
        print("1. Daily")
        print("2. Every Week")
        print("3. No Repeat")
        print("4. Every Month")
        print("5. Every Year")

        repeat = input("choose repeat option:")

        tasks.append({"task": task,"time": task_time,"date": task_date, "repeat": repeat})
        with open("tasks.json", "w") as file:
            json.dump(tasks, file)
            print("Task Added Successfully")
        
    elif choice == "2":
        print("your Tasks:")
        for i, item in enumerate(tasks, start=1):
            repeat_name = {"1": "Daily","2": "Weekly", "3": "No Repeat", "4": "Every Month", "5": "Every Year"}
            print(i, "-",item["task"],"-",item["time"], "_", repeat_name.get(item["repeat"], item["repeat"]))
    elif choice == "3":
        print("Exit")
        break
    elif choice == "4":
        print("your Tasks:")

        for i, item in enumerate(tasks, start=1):
            print(i,"_",item["task"], "_",item["time"])
        delete_task = int(input("Enter task number to delete:"))
        if 1<= delete_task <=len(tasks):
            tasks.pop(delete_task-1)
            with open("tasks.json", "w") as file:
                json.dump(tasks,file)
            print("Task deleted successfully")
        else:
            print("invalid task number")
    elif choice == "5":
        print("your Tasks:")

        for i, item in enumerate(tasks, start=1):
            print(i, "_", item["task"], "_", item["time"])
        edit_task = int(input("Enter task number to edit:"))
        if 1 <=edit_task <=len(tasks):
                item = tasks[edit_task-1]
                item["task"] = input("Enter new task name:")
                item["time"] = input("Enter new time (HH:MM):")
                item["date"] = input("Enter new date (DD-MM-YYYY):")
                item["repeat"] = input("choose repeat option(1-Dail,2-Weekly,3-None,4-Monthly,5-Yearly):")               
                with open("tasks.json", "w") as file:
                    json.dump(tasks,file)
                    print("Task updated successfully")
        else:
                print("invalid task number")
            
        
