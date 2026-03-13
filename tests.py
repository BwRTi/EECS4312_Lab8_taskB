import unittest
# Assuming the EventRegistration class is in a file named event_registration.py
# from event_registration import EventRegistration

class TestEventRegistration(unittest.TestCase):

    def test_standard_flow_and_promotion(self):
        """
        Test 1 (Standard Flow): Register to capacity, waitlist a user, 
        and trigger an automatic promotion via cancellation.
        """
        system = EventRegistration(capacity=2)
        
        # Register up to capacity
        system.register("alice@example.com")
        state = system.register("bob@example.com")
        self.assertEqual(state["registered"], ["alice@example.com", "bob@example.com"])
        self.assertEqual(state["waitlisted"], [])
        
        # Waitlist a user
        state = system.register("charlie@example.com")
        self.assertEqual(state["registered"], ["alice@example.com", "bob@example.com"])
        self.assertEqual(state["waitlisted"], ["charlie@example.com"])
        
        # Registered user cancels, triggering promotion
        state = system.cancel("alice@example.com")
        self.assertEqual(state["registered"], ["bob@example.com", "charlie@example.com"])
        self.assertEqual(state["waitlisted"], [])

    def test_zero_capacity_initialization(self):
        """
        Test 2 (Edge Case - AC1 Zero Capacity): Initialize with capacity=0.
        Verify all users go straight to the waitlist.
        """
        system = EventRegistration(capacity=0)
        
        system.register("alice@example.com")
        state = system.register("bob@example.com")
        
        self.assertEqual(state["capacity"], 0)
        self.assertEqual(state["registered"], [])
        self.assertEqual(state["waitlisted"], ["alice@example.com", "bob@example.com"])

    def test_reregistration_goes_to_back_of_waitlist(self):
        """
        Test 3 (Edge Case - AC3 Re-registration): A user registers, cancels, 
        and registers again. Verify they are treated as a brand new user.
        """
        system = EventRegistration(capacity=1)
        system.register("alice@example.com") # Takes the only spot
        
        system.register("bob@example.com")     # Waitlist pos 0
        system.register("charlie@example.com") # Waitlist pos 1
        
        # Bob cancels
        system.cancel("bob@example.com")
        
        # Bob re-registers
        state = system.register("bob@example.com")
        
        # Charlie should now be ahead of Bob on the waitlist
        self.assertEqual(state["waitlisted"], ["charlie@example.com", "bob@example.com"])

    def test_waitlist_cancellation(self):
        """
        Test 4 (Edge Case - AC4 Waitlist Cancellation): A waitlisted user cancels.
        Verify no one is promoted and the waitlist order is preserved.
        """
        system = EventRegistration(capacity=1)
        system.register("alice@example.com") # Registered
        
        system.register("bob@example.com")     # Waitlist pos 0
        system.register("charlie@example.com") # Waitlist pos 1
        
        # Bob (waitlisted) cancels
        state = system.cancel("bob@example.com")
        
        # Alice is still the only registered user, Charlie moves up in the waitlist
        self.assertEqual(state["registered"], ["alice@example.com"])
        self.assertEqual(state["waitlisted"], ["charlie@example.com"])

    def test_constraints_and_exceptions(self):
        """
        Test 5 (Constraints & Exceptions): Test invalid operations to ensure
        ValueErrors are raised appropriately.
        """
        # Negative capacity
        with self.assertRaises(ValueError):
            EventRegistration(capacity=-1)
            
        system = EventRegistration(capacity=2)
        system.register("alice@example.com")
        
        # Duplicate registration
        with self.assertRaises(ValueError):
            system.register("alice@example.com")
            
        # Canceling a non-existent user
        with self.assertRaises(ValueError):
            system.cancel("nobody@example.com")

if __name__ == "__main__":
    unittest.main()
