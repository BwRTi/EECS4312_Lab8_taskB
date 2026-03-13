import unittest
from solution import EventRegistration


class TestEventRegistrationLab9(unittest.TestCase):

    # Covers C1, C2, C7, C9, AC1, AC2, AC7
    def test_fifo_promotion_with_explanation(self):
        system = EventRegistration(capacity=2)

        system.register("alice@example.com")
        system.register("bob@example.com")
        system.register("charlie@example.com")
        system.register("dina@example.com")

        state = system.cancel("alice@example.com")

        self.assertEqual(
            state["summary"],
            "alice@example.com cancelled. charlie@example.com was promoted from the waitlist because a registered spot became available."
        )
        self.assertEqual(
            state["registered"],
            ["bob@example.com", "charlie@example.com"]
        )
        self.assertEqual(state["waitlisted"], ["dina@example.com"])

    # Covers C3, C10, AC3
    def test_successful_registration_returns_summary_and_state(self):
        system = EventRegistration(capacity=1)

        state = system.register("alice@example.com")

        self.assertEqual(state["summary"], "alice@example.com registered successfully.")
        self.assertEqual(state["capacity"], 1)
        self.assertEqual(state["registered"], ["alice@example.com"])
        self.assertEqual(state["waitlisted"], [])

    # Covers C5, C11, AC5, AC12
    def test_duplicate_registration_is_explicit_and_state_unchanged(self):
        system = EventRegistration(capacity=1)

        system.register("alice@example.com")
        before_registered = list(system.registered)
        before_waitlisted = list(system.waitlisted)

        with self.assertRaises(ValueError) as ctx1:
            system.register("alice@example.com")
        self.assertEqual(
            str(ctx1.exception),
            "Registration failed: 'alice@example.com' is already in the system as 'Registered'."
        )

        with self.assertRaises(ValueError) as ctx2:
            system.register("alice@example.com")
        self.assertEqual(
            str(ctx2.exception),
            "Registration failed: 'alice@example.com' is already in the system as 'Registered'."
        )

        self.assertEqual(system.registered, before_registered)
        self.assertEqual(system.waitlisted, before_waitlisted)

    # Covers C6, C11, AC6, AC12
    def test_invalid_cancellation_is_explicit_and_state_unchanged(self):
        system = EventRegistration(capacity=1)
        system.register("alice@example.com")

        before_registered = list(system.registered)
        before_waitlisted = list(system.waitlisted)

        with self.assertRaises(ValueError) as ctx1:
            system.cancel("ghost@example.com")
        self.assertEqual(
            str(ctx1.exception),
            "Cancellation failed: 'ghost@example.com' is not registered or waitlisted."
        )

        with self.assertRaises(ValueError) as ctx2:
            system.cancel("ghost@example.com")
        self.assertEqual(
            str(ctx2.exception),
            "Cancellation failed: 'ghost@example.com' is not registered or waitlisted."
        )

        self.assertEqual(system.registered, before_registered)
        self.assertEqual(system.waitlisted, before_waitlisted)

    # Covers C8, AC8, AC9
    def test_zero_capacity_and_waitlist_cancellation(self):
        system = EventRegistration(capacity=0)

        system.register("alice@example.com")
        system.register("bob@example.com")

        state = system.cancel("alice@example.com")

        self.assertEqual(
            state["summary"],
            "alice@example.com was removed from the waitlist."
        )
        self.assertEqual(state["registered"], [])
        self.assertEqual(state["waitlisted"], ["bob@example.com"])

    # Covers C8, AC9
    def test_waitlist_cancellation_preserves_order(self):
        system = EventRegistration(capacity=1)

        system.register("alice@example.com")
        system.register("bob@example.com")
        system.register("charlie@example.com")

        state = system.cancel("bob@example.com")

        self.assertEqual(
            state["summary"],
            "bob@example.com was removed from the waitlist."
        )
        self.assertEqual(state["registered"], ["alice@example.com"])
        self.assertEqual(state["waitlisted"], ["charlie@example.com"])

    # Covers C8, C10, AC10
    def test_reregistration_after_cancellation_goes_to_back(self):
        system = EventRegistration(capacity=1)

        system.register("alice@example.com")
        system.register("bob@example.com")
        system.register("charlie@example.com")

        system.cancel("bob@example.com")
        state = system.register("bob@example.com")

        self.assertEqual(
            state["summary"],
            "bob@example.com was added to the waitlist because the event is full."
        )
        self.assertEqual(state["waitlisted"], ["charlie@example.com", "bob@example.com"])

    # Covers C4, AC4
    def test_identical_sequences_are_deterministic(self):
        def run_sequence():
            system = EventRegistration(capacity=2)
            summaries = []
            summaries.append(system.register("alice@example.com")["summary"])
            summaries.append(system.register("bob@example.com")["summary"])
            summaries.append(system.register("charlie@example.com")["summary"])
            summaries.append(system.cancel("alice@example.com")["summary"])
            return summaries, list(system.registered), list(system.waitlisted)

        result1 = run_sequence()
        result2 = run_sequence()

        self.assertEqual(result1, result2)

    # Covers C13, AC11
    def test_get_status_reflects_promotion_immediately(self):
        system = EventRegistration(capacity=1)

        system.register("alice@example.com")
        system.register("bob@example.com")
        system.cancel("alice@example.com")

        self.assertEqual(system.get_status("alice@example.com"), "Not Registered")
        self.assertEqual(system.get_status("bob@example.com"), "Registered")


if __name__ == "__main__":
    unittest.main()
