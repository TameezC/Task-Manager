# import datetime and Counter for use in my defined functions.
from datetime import datetime
from collections import Counter


# Defined 'reg_user' function to add new users.
# If admin is logged in, then request user for new username and password.
# If entered username matches username in user.txt, display error and keep requesting username again until it is new.
# If non-admin is logged in, display appropriate message and go back to menu.
# Request confirm password. If same, open user.txt in append and write to bottom of file.
def reg_user():
    if menu == "r" and login[0] != "admin":
        print("\nSorry you do not have admin rights.")
    elif menu == "r" and login[0] == "admin":
        username = input("\nPlease enter a new username: ")
        with open("user.txt", "r") as user_name:
            user_list = [x.strip().split(", ") for x in user_name]
            user_check = [item[0] for item in user_list]
            while username in user_check:
                print("\nSorry, this username is taken. Please try another.")
                username = input("\nPlease enter a different username: ")
        password = input("\nPlease enter a new password: ")
        conf_password = input("\nPlease confirm your new password by entering again: ")
        while password != conf_password:
            print("\nSorry, the passwords are not the same. Please try again.\n")
            conf_password = input("\nPlease confirm your new password by entering again: ")
        else:
            with open("user.txt", "a") as user_txt:
                user_txt.write(f"\n{username}, {password}")
                print("\nYour new username and password has been created.")


# Defined 'add_task' function to add new task.
# Request task info and open/create tasks.txt in append and write to bottom of file.
def add_task():
    task_user = input("\nPlease enter the username of the person whom the task is assigned to: ")
    task_title = input("\nPlease enter the title of the task: ")
    task_desc = input("\nPlease enter a description of the task: ")
    task_due = input("\nPlease enter the due date of the task (e.g. 28 Mar 2022): ")
    current_date = datetime.date(datetime.now()).strftime(("%d %b %Y"))
    with open("tasks.txt", "a") as task_txt:
        task_txt.write(f"{task_user}, {task_title}, {task_desc}, {current_date}, {task_due}, No\n")
        print("\nYour new task information has been recorded.")


# Defined 'view_all' function to display all tasks.
# Open tasks.txt and read text.
# Display text using f- formatting, tab spacing and use indexing to find correct element in list.
def view_all():
    try:
        with open("tasks.txt", "r") as task_list:
            print("\nHere are all the tasks: \n")
            all_tasks = [x.strip().split(", ") for x in task_list]
            task_count = 1
            for i in all_tasks:
                i.insert(0, task_count)
                task_count += 1
            for lst in all_tasks:
                print('⸻' * 25)
                print(f"Task number:\t\t {lst[0]}\nTask:\t\t\t\t {lst[2]}\nAssigned to:\t\t {lst[1]}\n"
                      f"Date assigned:\t\t {lst[4]}\nDue date:\t\t\t {lst[5]}"
                      f"\nTask complete?\t\t {lst[6]}\n"f"Task description:\n{lst[3]}")
            print('⸻' * 25)
    except FileNotFoundError:
        print("\nSorry the task file does not exist. Please use the add task option to create the file")


# Defined 'view_mine' function to display and edit tasks assigned to the logged-in user.
# Open tasks.txt and add task number which increments.
# Check if login username is within the nested lists. If found, will display the relevant list.
# Give user option to mark their task as complete or edit either due date or assigned user on their task.
def view_mine():
    try:
        with open("tasks.txt", "r") as task_list:
            print(f"\nHere are all of your tasks {login[0]} \n")
            print("⸻" * 25)
            my_tasks = [x.strip().split(", ") for x in task_list]
            task_count = 1
            for i in my_tasks:
                i.insert(0, task_count)
                task_count += 1
            for lst in my_tasks:
                if login[0] in lst:
                    print(f"Task number:\t\t {lst[0]}\nTask:\t\t\t\t {lst[2]}\nAssigned to:\t\t {lst[1]}\n"
                          f"Date assigned:\t\t {lst[4]}\nDue date:\t\t\t {lst[5]}"
                          f"\nTask complete?\t\t {lst[6]}\n"f"Task description:\n{lst[3]}")
                    print('⸻' * 25)
            my_tasks = {x[0]: x[1:] for x in my_tasks}
            while True:
                task_select = int(
                    input("Please select a task number for further options or enter -1 to return to the menu: "))
                if task_select in my_tasks:
                    task_options = (input(f"\nYou have chosen task number: {task_select}\n"
                                      f"\nIf you want to mark the task as complete, enter 'complete'"
                                      f"\nIf you want to edit the task, enter 'edit'"
                                      f"\n(Note: only the username of the person to whom the task is assigned to, "
                                      f"or the due date of the task can be edited): ").lower())
                    if task_options == "complete":
                        my_tasks.get(task_select)[-1] = "Yes"
                        temp_tasks = (my_tasks.values())
                        with open("tasks.txt", "w") as f:
                            for item in temp_tasks:
                                f.write(", ".join(item) + "\n")
                            print("\nTask has been updated.")
                            break
                    if task_options == "edit" and my_tasks.get(task_select)[-1] == "No":
                        edit_select = input(
                            "\nPlease enter 'username' to edit the username assigned to the task or enter 'date' "
                            "to edit the due date of the task: ").lower()
                        if edit_select == "username":
                            new_user = input("\nPlease enter the new user assigned to the task: ")
                            my_tasks.get(task_select)[0] = new_user
                            temp_tasks = (my_tasks.values())
                            with open("tasks.txt", "w") as f:
                                for item in temp_tasks:
                                    f.write(", ".join(item) + "\n")
                                print("\nTask has been updated")
                                break
                        elif edit_select == "date":
                            new_date = input("\nPlease enter a new due date. (e.g. 28 Mar 2022): ")
                            my_tasks.get(task_select)[-2] = new_date
                            temp_tasks = (my_tasks.values())
                            with open("tasks.txt", "w") as f:
                                for item in temp_tasks:
                                    f.write(", ".join(item) + "\n")
                                print("\nTask has been updated.")
                                break
                        else:
                            print("\nSorry that is not the correct option.")
                    elif task_options == "edit" and my_tasks.get(task_select)[-1] == "Yes":
                        print("\nSorry, you cannot edit a completed task.\n")
                elif task_select == -1:
                    print("\nReturning to the menu")
                    break
                else:
                    print("\nSorry, that task does not exist. Please try again.\n")
                    continue
    except FileNotFoundError:
        print("\nSorry the task file does not exist. Please use the add task option to create the file")


# Defined task_user_reports function to generate task and user overview reports.
# Use of list comprehensions, for loops, if statements, file open and write mode and lists and dictionaries.
def task_user_reports():
    try:
        print("\nTask and user overview reports have been generated.")
        # Block to generate task_overview.txt and write info to file in easy to read format.
        # Imported datetime for overdue tasks.
        with open("tasks.txt", "r") as task_list:
            all_tasks = [x.strip().split(", ") for x in task_list]
            tasks_total = (len(all_tasks))
            tasks_yes = sum("Yes" in x for x in all_tasks)
            tasks_no = sum("No" in x for x in all_tasks)
            overdue_count = 0
            for lst in all_tasks:
                if (datetime.strptime(lst[4], "%d %b %Y").date()) < datetime.date(datetime.now()) and lst[-1] == "No":
                    overdue_count += 1
            perc_tasks_no = round(percentage_of(tasks_no, tasks_total))
            perc_tasks_overdue = round(percentage_of(overdue_count, tasks_total))
            with open("task_overview.txt", "w") as task_overview:
                task_overview.write(f"Task Overview:\n\n"
                                f"Total number of tasks generated and tracked: {tasks_total}\n\n"
                                f"Total number of completed tasks: {tasks_yes}\n\n"
                                f"Total number of not completed tasks: {tasks_no}\n\n"
                                f"Total number of not completed and overdue tasks: {overdue_count}\n\n"
                                f"% of incomplete tasks: {perc_tasks_no}\n\n"
                                f"% of overdue tasks: {perc_tasks_overdue}")

        # Block to generate user_overview.txt and write info to file in easy to read format.
        with open("user.txt", "r") as user_list:
            all_users = [x.strip().split(", ") for x in user_list]
            users_total = (len(all_users))

            # count number of tasks assigned to each user. Imported Counter to use Count for tasks.
            user_task_count = [item[0] for item in all_tasks]
            user_task_count = (Counter(user_task_count))
            str_task_count = "\n".join(f"{key}: {value}" for key, value in user_task_count.items())

            # % of tasks assigned to each user using dictionary
            perc_user_tasks = {key: value / tasks_total * 100 for key, value in user_task_count.items()}
            perc_user_tasks_round = {}
            for key in perc_user_tasks.keys():
                perc_user_tasks_round[key] = round(perc_user_tasks[key])
            str_perc_user_tasks = "\n".join(f"{key}: {value}" for key, value in perc_user_tasks_round.items())

            # % of tasks assigned to each user that has been completed using dictionary. Use of Count for tasks.
            user_tasks_complete = [x[0] for x in all_tasks if x[-1] == "Yes"]
            user_tasks_complete = (Counter(user_tasks_complete))
            perc_tasks_complete = {key: value / tasks_total * 100 for key, value in user_tasks_complete.items()}
            perc_tasks_complete_round = {}
            for key in perc_tasks_complete.keys():
                perc_tasks_complete_round[key] = round(perc_tasks_complete[key])
            str_perc_tasks_complete = "\n".join(f"{key}: {value}" for key, value in perc_tasks_complete_round.items())

            # % of tasks assigned to each user that must be completed using dictionary. Use of Count for tasks.
            user_tasks_not_complete = [x[0] for x in all_tasks if x[-1] == "No"]
            user_tasks_not_complete = (Counter(user_tasks_not_complete))
            perc_tasks_not_complete = {key: value / tasks_total * 100 for key, value in user_tasks_not_complete.items()}
            perc_tasks_not_complete_round = {}
            for key in perc_tasks_not_complete.keys():
                perc_tasks_not_complete_round[key] = round(perc_tasks_not_complete[key])
            str_perc_tasks_not_complete = "\n".join(
                f"{key}: {value}" for key, value in perc_tasks_not_complete_round.items())

            # % of tasks assigned to each user that must be completed and is overdue using dictionary. Use of Count for tasks.
            user_overdue_tasks = []
            for x in all_tasks:
                if (datetime.strptime(x[4], "%d %b %Y").date()) < datetime.date(datetime.now()) and x[-1] == "No":
                    user_overdue_tasks.append(x[0])
            user_overdue_tasks = (Counter(user_overdue_tasks))
            perc_user_overdue_tasks = {key: value / tasks_total * 100 for key, value in user_overdue_tasks.items()}
            perc_user_overdue_tasks_round = {}
            for key in perc_user_overdue_tasks.keys():
                perc_user_overdue_tasks_round[key] = round(perc_user_overdue_tasks[key])
            str_perc_user_overdue_tasks = "\n".join(
                f"{key}: {value}" for key, value in perc_user_overdue_tasks_round.items())

            # write the above outputs to user_overview.txt in easy to read format.
            with open("user_overview.txt", "w") as user_overview:
                user_overview.write(f"User overview:\n\n"
                                f"Total number of users registered: {users_total}\n\n"
                                f"Total number of tasks generated and tracked: {tasks_total}\n\n"
                                f"Total number of tasks assigned to each user:\n{str_task_count}\n\n"
                                f"% of total number of tasks assigned to each user:\n{str_perc_user_tasks}\n\n"
                                f"% of tasks assigned to users that has been completed:\n{str_perc_tasks_complete}\n\n"
                                f"% of tasks assigned to users that must be completed:\n{str_perc_tasks_not_complete}\n\n"
                                f"% of tasks assigned to users that must be completed and are overdue:\n{str_perc_user_overdue_tasks}")
    except FileNotFoundError:
        print("\nSorry the task file does not exist. Please use the add task option to create the file")


# Defined display_statisticss to read info from user_overview.txt in an easy-to-read format.
# Use of list comprehension and for loops with task and user overview files in read mode.
def display_stats():
    try:
        with open("task_overview.txt", "r") as task_display:
            task_info = [x.strip().split(", ") for x in task_display]
            print('⸻' * 25)
            for lst in task_info:
                print(f"{lst[0]}")
            print('⸻' * 25)
        with open("user_overview.txt", "r") as user_display:
            user_info = [x.strip().split(", ") for x in user_display]
            for lst in user_info:
                print(f"{lst[0]}")
            print('⸻' * 25)
    except FileNotFoundError:
        print("The task and user overview files do not exist. Please select the generate reports option")


# function to find percentage of two numbers
def percentage_of(val_a, val_b):
    return (val_a / val_b * 100)


# ====Login Section====
# open user.txt in read mode, strip it to remove \n and split words into nested lists.
# use while true to request login input, join these together and split to make them a list.
# for loop to determine if login input is in the user variable from the text file or not.
# Display appropriate error message then continue or correct details message and break loop.
with open("user.txt", "r") as user_txt:
    user = [x.strip().split(", ") for x in user_txt]
    while True:
        login_user = input("Please enter your username: ")
        login_pass = input("Please enter your password: ")
        login = (login_user + " " + login_pass)
        login = login.split(" ")
        for i in range(1):
            if login not in user:
                print("Wrong username or password. Please try again.\n")
                continue
        if login in user:
            print("\nYour details are correct. Thank you for logging in.")
            break

# presenting the menu to the user and
# making sure that the user input is converted to lower case.
# if admin logged in, will see a different menu with added option to view statistics. Non-admin will not see this.
while True:
    if login[0] != "admin":
        menu = input("\nSelect one of the following options below to continue: "
                     "\nr - Registering a user"
                     "\na - Adding a task"
                     "\nva - View all tasks"
                     "\nvm - view my task"
                     "\ne - Exit"
                     "\n").lower()
    else:
        menu = input("\nSelect one of the following options below to continue: "
                     "\nr - Registering a user"
                     "\na - Adding a task"
                     "\nva - View all tasks"
                     "\nvm - View my task"
                     "\ngr - Generate reports"
                     "\nds - Display statistics"
                     "\ne - Exit"
                     "\n").lower()

    # use if to call 'reg_user' function if user selects 'r'.
    if menu == "r":
        reg_user()

    # use elif to call 'add_user' function if user selects 'a'.
    elif menu == "a":
        add_task()

    # use elif to call 'view_all' function if user selects 'va'.
    elif menu == 'va':
        view_all()

    # use elif to call 'view_mine' function if user selects 'vm'.
    elif menu == 'vm':
        view_mine()

    # if 'gr' entered, generate task overview and user overview reports for admin.
    elif menu == 'gr' and login[0] == "admin":
        task_user_reports()


    # if 'ds' entered, displays statistics for admin from files. If non-admin selects, they will get an error message.
    elif menu == 'ds' and login[0] == "admin":
        display_stats()

    # use elif if "e" entered. Displays goodbye message and exits.
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # use else if wrong input and display error message. Loops to start.
    else:
        print("You have made a wrong choice, Please Try again")