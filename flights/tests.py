from django.test import TestCase, Client
from .models import Airport, Flights, Passenger

# Create your tests here.
# Creates an entirely separate database specifically only for testing purposes

class FlightTestCase(TestCase):

    #Predefined function to add some sample data in our database which we gonna test checks on
    def setUp(self):
        
        # Create Airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create Flights
        Flights.objects.create(origin=a1, destination=a2, duration=100)
        Flights.objects.create(origin=a1, destination=a1, duration=200)
        Flights.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)   # Check that only 3 flights depart from airport a1

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)     # Check if only 1 flight arrives at airport a1

    # Test default web page to ensure it works correctly
    def test_index(self):
        c = Client()
        response = c.get("/flights/")                   # The route which gets us the index page for all flights
        self.assertEqual(response.status_code, 200)     # Status code of the response returned must be 200 to indicate no error
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flights.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    # def test_invalid_flight_page(self):
    #     # Gets the flight with max id in database
    #     max_id = Flights.objects.all().aggregate(Max("id"))["id__max"]    # Getting error - Max not defined

    #     c = Client()
    #     response = c.get(f"/flights/{max_id + 1}")
    #     self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flights.objects.get(pk=1)
        p = Passenger.objects.create(fname="Alice", lname="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a2, duration= -100)
        self.assertFalse(f.is_valid_flight())