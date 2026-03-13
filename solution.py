## Student Name:Yifan Wang
## Student ID:218140046

class EventRegistration:
    """
    Manages event registrations for a single event with a fixed capacity and FIFO waitlist.
    Successful state-changing operations return one concise summary plus the updated state.
    Invalid operations raise ValueError with descriptive messages.
    """

    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Capacity cannot be negative.")

        self.capacity = capacity
        self.registered = []
        self.waitlisted = []
        self._user_status = {}

    def _state_snapshot(self) -> dict:
        return {
            "capacity": self.capacity,
            "registered": list(self.registered),
            "waitlisted": list(self.waitlisted),
        }

    def _success_response(self, summary: str) -> dict:
        snapshot = self._state_snapshot()
        return {
            "summary": summary,
            **snapshot,
        }

    def register(self, email: str) -> dict:
        if email in self._user_status:
            raise ValueError(
                f"Registration failed: '{email}' is already in the system as '{self._user_status[email]}'."
            )

        if len(self.registered) < self.capacity:
            self.registered.append(email)
            self._user_status[email] = "Registered"
            return self._success_response(f"{email} registered successfully.")

        self.waitlisted.append(email)
        self._user_status[email] = "Waitlisted"
        return self._success_response(
            f"{email} was added to the waitlist because the event is full."
        )

    def cancel(self, email: str) -> dict:
        if email not in self._user_status:
            raise ValueError(
                f"Cancellation failed: '{email}' is not registered or waitlisted."
            )

        current_status = self._user_status[email]

        if current_status == "Registered":
            self.registered.remove(email)
            del self._user_status[email]

            if self.waitlisted:
                promoted_user = self.waitlisted.pop(0)
                self.registered.append(promoted_user)
                self._user_status[promoted_user] = "Registered"
                return self._success_response(
                    f"{email} cancelled. {promoted_user} was promoted from the waitlist because a registered spot became available."
                )

            return self._success_response(
                f"{email} cancelled successfully. No waitlisted user was promoted."
            )

        self.waitlisted.remove(email)
        del self._user_status[email]
        return self._success_response(f"{email} was removed from the waitlist.")

    def get_status(self, email: str) -> str:
        return self._user_status.get(email, "Not Registered")
