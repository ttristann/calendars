# This file is compiled of all the classes that are critical
# actors to the calendar application. These classes interact
# with each other in certain ways to achieve the essential 
# functionalities of the application. 

from zoneinfo import ZoneInfo
from datetime import datetime

class User:
    users = {} # stores all of the user instances that are created during the session

    def __init__(self, username, timezone = "UTC"):
        self.username = username
        self.timezone = timezone
        self.calendars = list() # holds the list of Calendars the user have access to
        User.users[username] = self # keeps track of the user instances in the dictionary to manage them globally

    @classmethod
    def loginUser(cls, username):
        """
        Returns the User instance that 
        is associated with the username. 

        If the username is not associated
        with any, it returns None. 
        """
        return cls.users.get(username, None)
    
    @classmethod
    def createUser(cls, username):
        """
        Creates a User based on the username
        if the username is not already taken
        by an existing User. 
        """
        if username not in cls.users:
            return User(username) # constructs a new User object
        return None
    
    def removeCalendar(self, calendar_name):
        """
        Removes all Calendar objects from the calendars
        that are associated with the calendar_name.
        """
        self.calendars = [cal for cal in self.calendars if cal.calendar_name != calendar_name]

    def createCalendar(self, calendar_name, is_public):
        """
        Creates a new Calendar that is automatically 
        associated with the User. 
        """
        new_calendar = Calendar(calendar_name, is_public, self)
        self.calendars.append(new_calendar)

        return new_calendar

    def updateCalendar(self, calendar_name, new_name = None, is_public = None):
        """
        Accesses the corresponding the Calendar based on 
        the calendar_name within the calendars the User 
        has access to. 

        Makes edits to the Calendars based on the inputs
        the User wants to change. If no inputs, no updates
        will be made. 
        """
        for calendar in self.calendars:
            if calendar.calendar_name == calendar_name:
                if is_public is not None:
                    calendar.is_public = is_public
                if new_name:
                    calendar.calendar_name = new_name
                break

class Calendar:
    def __init__(self, calendar_name, is_public, owner):
        self.calendar_name = calendar_name
        self.is_public = is_public
        self.owner = owner
        self.events = list()
        self.shared_with = list()
        self.config = ConfigurationScreen()

    def create_event(self, event_name, description, start_time, end_time):
        """
        Creates an Event based on the given inputs and
        stores it in events to keep track of all events
        the that are part of the current Calendar. 
        """
        new_event = Event(event_name, description, start_time, end_time)
        self.events.appened(new_event)

    def remove_event(self, event_name):
        """
        Removes all instances of Events that are
        associated with the event_name. 
        """
        self.events = [event for event in self.events if event.event_name != event_name]
    
    def share_calendar(self, username):
        """
        Adds the User associated with the username
        to the list of users that have access to
        the current Calendar. 
        """
        if username not in self.shared_with:
            self.shared_with.append(username)
            message = f"The Calendar has been successfully shared with user {username}.\n"
        else:
            message = f"The User {username} already been shared of this Calendar.\n"

        return message

    def remove_share(self, username):
        """
        Removes the User that is associated with
        the username from the list of usernames 
        that have access to the current Calendar.
        """
        if username in self.shared_with:
            self.shared_with.remove(username)
            message = f"The User {username} has been removed from the Calendar.\n"
        else:
            message = f"The User {username} cannot be removed due to not being to the User.\n"

        return message
    
    def update_event(self, event_name, field, new_value):
        """
        Updates the Events that are associated with
        the event_name based on a certain field. 
        It updates with the inputted new_value for
        the specified field. 
        """
        for event in self.events:
            if event.event_name == event_name:
                if field == "description":
                    event.change_description(new_value)
                elif field == "start_time":
                    event.change_time(new_value, event.end_time.strftime("%H:%M"))
                elif field == "end_time":
                    event.change_time(event.start_time.strftime("%H:%M"), new_value)
                break

    def display_calendar(self):
        """
        Prints the name of the Calendar and its status,
        and then the events that have been created in it.
        """
        print(f"Calendar: {self.calendar_name} (Public: {self.is_public}) has the following events: \n")
        for event in self.events:
            print(f"- {event}")

