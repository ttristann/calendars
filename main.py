from classes import *

class CalendarAppFacade:
    def __init__(self):
        self.current_user = None

    def sign_up(self, username):
        user = User.createUser(username)
        if user:
            self.current_user = user
            return f"User {username} has successfully been created!"
        return f"Username {username} already exists. Try logging in or use a different username."

    def log_in(self, username):
        user = User.loginUser(username)
        if user:
            self.current_user = user
            return f"Welcome back, {username}!"
        return "That User does not exist. Try signing up."

    def create_calendar(self, calendar_name, is_public):
        if self.current_user:
            self.current_user.create_calendar(calendar_name, is_public)
            return f"Calendar '{calendar_name}' created successfully!"
        return "No user logged in."

    def display_calendars(self):
        if self.current_user:
            self.current_user.display_calendars()
        else:
            return "No user logged in."

    def delete_calendar(self, calendar_name):
        if self.current_user:
            self.current_user.remove_calendar(calendar_name)
            return f"Calendar '{calendar_name}' has been deleted!"
        return "No user logged in."

    def update_calendar(self, calendar_name, new_name=None, is_public=None):
        if self.current_user:
            self.current_user.update_calendar(calendar_name, new_name, is_public)
            return f"Calendar '{calendar_name}' has been updated!"
        return "No user logged in."

    def create_event(self, calendar_name, event_name, description, start_time, end_time):
        if self.current_user:
            calendar = next((cal for cal in self.current_user.calendars if cal.calendar_name == calendar_name), None)
            if calendar:
                calendar.create_event(event_name, description, start_time, end_time)
                return f"Event '{event_name}' added to calendar '{calendar_name}'!"
            return "Calendar not found."
        return "No user logged in."

    def display_calendar_events(self, calendar_name):
        if self.current_user:
            calendar = next((cal for cal in self.current_user.calendars if cal.calendar_name == calendar_name), None)
            if calendar:
                calendar.display_calendar()
            else:
                return "Calendar not found."
        else:
            return "No user logged in."

    def delete_event(self, calendar_name, event_name):
        if self.current_user:
            calendar = next((cal for cal in self.current_user.calendars if cal.calendar_name == calendar_name), None)
            if calendar:
                calendar.remove_event(event_name)
                return f"Event '{event_name}' removed from calendar '{calendar_name}'!"
            return "Calendar not found."
        return "No user logged in."

    def update_event(self, calendar_name, event_name, field, new_value):
        if self.current_user:
            calendar = next((cal for cal in self.current_user.calendars if cal.calendar_name == calendar_name), None)
            if calendar:
                calendar.update_event(event_name, field, new_value)
                return f"Event '{event_name}' updated successfully!"
            return "Calendar not found."
        return "No user logged in."

    def share_calendar(self, calendar_name, username):
        if self.current_user:
            calendar = next((cal for cal in self.current_user.calendars if cal.calendar_name == calendar_name), None)
            if calendar:
                return calendar.share_calendar(username)
            return "Calendar not found."
        return "No user logged in."

    def log_out(self):
        self.current_user = None
        return "Logged out successfully."


def main():
    app = CalendarAppFacade()
    print("\nWelcome to the Calendar Application\n")

    while True:
        print("What would you like to do:")
        print("  1. Sign up")
        print("  2. Log in")
        print("  3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            username = input("Enter a username: ").strip()
            print(app.sign_up(username))
        elif choice == "2":
            username = input("Enter your username: ").strip()
            print(app.log_in(username))
            user_menu(app)
        elif choice == "3":
            print("Exiting the application now. Goodbye!")
            break
        else:
            print("Invalid choice. Choose 1, 2, or 3.")


def user_menu(app):
    while True:
        print("\nUser Menu:")
        print("  1. Create a Calendar")
        print("  2. View My Calendars")
        print("  3. Manage Events")
        print("  4. Delete a Calendar")
        print("  5. Update a Calendar")
        print("  6. Log Out")
        option = input("Choose an option (1-6): ")

        if option == "1":
            calendar_name = input("Enter calendar name: ").strip()
            is_public = input("Should it be public? (yes/no): ").strip().lower() == "yes"
            print(app.create_calendar(calendar_name, is_public))
        elif option == "2":
            app.display_calendars()
        elif option == "3":
            calendar_name = input("Enter calendar name to manage events: ").strip()
            manage_events(app, calendar_name)
        elif option == "4":
            calendar_name = input("Enter calendar name to delete: ").strip()
            print(app.delete_calendar(calendar_name))
        elif option == "5":
            calendar_name = input("Enter calendar name to update: ").strip()
            new_name = input("Enter new name (leave blank to keep the same): ").strip()
            change_public = input("Change privacy setting? (yes/no): ").strip().lower()
            is_public = change_public == "yes"
            print(app.update_calendar(calendar_name, new_name if new_name else None, is_public))
        elif option == "6":
            print(app.log_out())
            break
        else:
            print("Invalid choice. Choose 1-6.")


def manage_events(app, calendar_name):
    while True:
        print("\nManage Events:")
        print("  1. Add an Event")
        print("  2. View Events")
        print("  3. Delete an Event")
        print("  4. Update an Event")
        print("  5. Go Back")
        option = input("Choose an option (1-5): ")

        if option == "1":
            event_name = input("Enter event name: ").strip()
            description = input("Enter event description: ").strip()
            start_time = input("Enter start time (HH:MM): ").strip()
            end_time = input("Enter end time (HH:MM): ").strip()
            print(app.create_event(calendar_name, event_name, description, start_time, end_time))
        elif option == "2":
            app.display_calendar_events(calendar_name)
        elif option == "3":
            event_name = input("Enter event name to delete: ").strip()
            print(app.delete_event(calendar_name, event_name))
        elif option == "4":
            event_name = input("Enter event name to update: ").strip()
            new_desc = input("Enter the new description: ").strip()
            print(app.update_event(calendar_name, event_name, "description", new_desc))
            new_start = input("Enter new start time (HH:MM): ").strip()
            print(app.update_event(calendar_name, event_name, "start_time", new_start))
            new_end = input("Enter new end time (HH:MM): ").strip()
            print(app.update_event(calendar_name, event_name, "end_time", new_start))
        elif option == "5":
            break

if __name__ == "__main__":
    main()