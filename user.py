def read_issues():
    # read database
    database = []
    with open('database.txt') as file:
        database = file.readlines()

    while True:
        # print issues title
        print()
        print("*****************************************************")
        index = 0
        total_titles = 1
        while index < len(database):
            print(f'{total_titles}) {database[index]}')
            index += 3
            total_titles += 1
        print(f'{total_titles}) exit')
        print()
        print("*****************************************************")

        # Choose issue to read or exit
        print("Choose the issue you want to read!")
        first_input = int(input())
        if first_input == total_titles:
            break
        elif 1 <= first_input <= total_titles-1:
            print(
                "********************************************************************************************")
            index = (first_input-1)*3
            print(f'Title: {database[index]}')
            index += 1
            print(f'Description: {database[index]}')
            index += 1
            print(f'Readdresal: {database[index]}')
            print(
                "********************************************************************************************")
            nothing = input("press enter after you finish read it")
            print()


def user_write_issue():
    print()
    print("*******************************************************************")
    print("Please write the issue title and description below")
    issue_title = input("Title: ")
    issue_description = input("Description: ")
    issue_addresal = "No Addresal Yet"
    write_file = ['', issue_title, issue_description, issue_addresal]
    with open('database.txt', 'a') as f:
        f.writelines('\n'.join(write_file))
    print("*******************************************************************")
    print("Your issue has been posted")
    print()


# Main function
user_type = None
while True:
    print("""
Please select the user type that you want to use
1) admin
2) user
3) exit
    """)

    first_input = int(input())
    if first_input == 1:
        user_type = "admin"
    elif first_input == 2:
        user_type = "user"
    elif first_input == 3:
        break
    else:
        print("Please select only 1-3")

    # If it is user
    while True and user_type == "user":
        second_input = int(input("""
Please select what do you want to do
1) Read issues
2) Post new issue
3) Exit
        """))
        if second_input == 1:
            read_issues()
        elif second_input == 2:
            user_write_issue()
        elif second_input == 3:
            break
        else:
            print("Please select only 1-3")

    # If it is an admin

print("Thank you for using our app")
