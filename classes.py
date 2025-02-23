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