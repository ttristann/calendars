from classes import *

def main():
    """
    This is the main script that runs the program. 
    Uses all of the classes and functions that 
    are imported into this file. 
    """
    print("\nWelcome to the Calendar Application\n")

    current_user = None # to keep track of the logged-in user throughout the whole session

    while True:
        print("What would you like to do:")
        print("  1. Sign up")
        print("  2. Log in")
        print("  3. Exit")
        welcome_option = input("Choose an option (1-3): ")

        if welcome_option == "1":
            username = input("Enter a username: ").strip()
            user = User.createUser(username)
            if user:
                current_user = user
                print(f"\nThe User {username} has successfully been created!\n")
                user_menu(current_user)
            else:
                print(f"Username {username} already exists. Try loggin in or use a different username.\n")

        elif welcome_option == "2":
            username = input("Enter your username: ").strip()
            user = User.loginUser(username)
            if user:
                print(f"Welcome back, {username}!\n")
                current_user = user
                user_menu(current_user)
            else:
                print("That User does not exist. Try signing up.")
        elif welcome_option == "3":
            print("Exiting the application now. Goodbye!")
            break
        else:
            print("Invalid choice. Choose 1, 2, 3")


def user_menu(user):
    """Menu for logged-in users to manage calendars and events."""
    while True:
        print(f"\nWelcome, {user.username}! What would you like to do?")
        print("  1. Create a Calendar")
        print("  2. View My Calendars")
        print("  3. Manage a Calendar")
        print("  4. Delete a Calendar")
        print("  5. Update a Calendar")
        print("  6. Log Out")
        option = input("Choose an option (1-6): ")

        if option == "1":
            calendar_name = input("Enter calendar name: ").strip()
            is_public = input("Should it be public? (yes/no): ").strip().lower() == "yes"
            user.create_calendar(calendar_name, is_public)
            print(f"Calendar '{calendar_name}' created successfully!")

        elif option == "2":
            user.display_calendars()

        elif option == "3":
            if not user.calendars:
                print("You have no calendars. Create one first!")
                continue

            calendar_name = input("Enter the calendar name to manage: ").strip()
            calendar = next((cal for cal in user.calendars if cal.calendar_name == calendar_name), None)

            if not calendar:
                print("Calendar not found.")
                continue

            manage_calendar(calendar)

        elif option == "4":
            if not user.calendars:
                print("You have no calendars to delete!")
                continue

            calendar_name = input("Enter the calendar name to delete: ").strip()
            user.remove_calendar(calendar_name)
            print(f"Calendar '{calendar_name}' has been deleted!")

        elif option == "5":
            if not user.calendars:
                print("You have no calendars to update!")
                continue

            calendar_name = input("Enter the calendar name to update: ").strip()
            new_name = input("Enter the new calendar name (leave blank to keep the same): ").strip()
            change_public = input("Change privacy setting? (yes/no): ").strip().lower()

            if change_public == "yes":
                is_public = input("Should it be public? (yes/no): ").strip().lower() == "yes"
            else:
                is_public = None  # Keep the current setting

            user.update_calendar(calendar_name, new_name if new_name else None, is_public)
            print(f"Calendar '{calendar_name}' has been updated!")

        elif option == "6":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please choose 1-6.")

def manage_calendar(calendar):
    """Menu to manage a specific calendar."""
    while True:
        print(f"\nManaging Calendar: {calendar.calendar_name}")
        print("  1. Add an Event")
        print("  2. View Events")
        print("  3. Delete an Event")
        print("  4. Update an Event")
        print("  5. Share Calendar")
        print("  6. Go Back")
        option = input("Choose an option (1-6): ")

        if option == "1":
            event_name = input("Enter event name: ").strip()
            description = input("Enter event description: ").strip()
            start_time = input("Enter start time (HH:MM): ").strip()
            end_time = input("Enter end time (HH:MM): ").strip()
            calendar.create_event(event_name, description, start_time, end_time)
            print(f"Event '{event_name}' added!")

        elif option == "2":
            calendar.display_calendar()

        elif option == "3":
            event_name = input("Enter event name to delete: ").strip()
            calendar.remove_event(event_name)
            print(f"Event '{event_name}' removed!")

        elif option == "4":
            update_event(calendar)

        elif option == "5":
            share_with = input("Enter username to share with: ").strip()
            calendar.share_calendar(share_with)
            print(f"Calendar shared with {share_with}!")

        elif option == "6":
            print("Going back to the main menu...")
            break

        else:
            print("Invalid option. Please choose 1-6.")

def update_event(calendar):
    """Updates an event in a calendar."""
    event_name = input("Enter the event name to update: ").strip()
    event = next((e for e in calendar.events if e.event_name == event_name), None)

    if not event:
        print("Event not found!")
        return

    print("\nWhat would you like to update?")
    print("  1. Event Name")
    print("  2. Description")
    print("  3. Start Time")
    print("  4. End Time")
    option = input("Choose an option (1-4): ")

    if option == "1":
        new_name = input("Enter the new event name: ").strip()
        event.name = new_name
        print("Event name updated!")

    elif option == "2":
        new_desc = input("Enter the new description: ").strip()
        event.change_description(new_desc)
        print("Event description updated!")

    elif option == "3":
        new_start = input("Enter new start time (HH:MM): ").strip()
        event.change_time(new_start, event.end_time.strftime("%H:%M"))
        print("Event start time updated!")

    elif option == "4":
        new_end = input("Enter new end time (HH:MM): ").strip()
        event.change_time(event.start_time.strftime("%H:%M"), new_end)
        print("Event end time updated!")

    else:
        print("Invalid option. No changes made.")

if __name__ == "__main__":
    main()