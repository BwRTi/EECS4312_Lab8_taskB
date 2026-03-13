class EventRegistration:
    """
    Manages event registrations, including a fixed capacity and a FIFO waitlist.
    """

    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        
        self.capacity = capacity
        # Using lists to maintain insertion/FIFO order
        self.registered = []
        self.waitlisted = []
        # Using a dictionary for O(1) status lookups and duplicate prevention
        self._user_status = {}

    def _generate_state_report(self) -> dict:
        """
        Helper method to generate the current state of the registration system.
        Returns a dictionary containing capacity, registered users, and waitlisted users.
        """
        return {
            "capacity": self.capacity,
            "registered": list(self.registered),
            "waitlisted": list(self.waitlisted)
        }

    def register(self, email: str) -> dict:
        """
        Attempts to register a user. 
        Places them in the registered list if under capacity, or waitlists them otherwise.
        
        Raises:
            ValueError: If the user is already registered or waitlisted.
        """
        if email in self._user_status:
            raise ValueError(f"Registration failed: '{email}' is already in the system as '{self._user_status[email]}'.")

        # Check against capacity (handles AC1: capacity == 0 gracefully)
        if len(self.registered) < self.capacity:
            self.registered.append(email)
            self._user_status[email] = "Registered"
        else:
            self.waitlisted.append(email)
            self._user_status[email] = "Waitlisted"

        return self._generate_state_report()

    def cancel(self, email: str) -> dict:
        """
        Cancels a user's registration or waitlist spot.
        Automatically promotes the next waitlisted user if a registered user cancels.
        
        Raises:
            ValueError: If the email is not found in the system.
        """
        if email not in self._user_status:
            raise ValueError(f"Cancellation failed: '{email}' is not registered or waitlisted.")

        current_status = self._user_status[email]

        if current_status == "Registered":
            # Remove from registered list
            self.registered.remove(email)
            del self._user_status[email]

            # Auto-promote the first person on the waitlist, if any exist
            if self.waitlisted:
                # pop(0) enforces strict FIFO ordering for promotions
                promoted_user = self.waitlisted.pop(0)
                self.registered.append(promoted_user)
                self._user_status[promoted_user] = "Registered"

        elif current_status == "Waitlisted":
            # Remove from waitlist without affecting the FIFO order of others (AC4)
            self.waitlisted.remove(email)
            del self._user_status[email]

        return self._generate_state_report()

    def get_status(self, email: str) -> str:
        """
        Queries the current status of a given email.
        Returns 'Registered', 'Waitlisted', or 'Not Registered'.
        """
        return self._user_status.get(email, "Not Registered")
