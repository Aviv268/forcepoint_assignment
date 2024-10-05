from src.ride_allocation import (
    read_ride_requests,
    aggregate_requests,
    request_rides_from_transit_agency,
    distribute_rides,
)


def test_read_ride_requests(tmp_path):
    # Create a temporary CSV file
    csv_content = """company_name,destination,number_of_rides_requested
Company A,Destination X,100
Company B,Destination Y,200
"""

    test_file = tmp_path / "test_ride_requests.csv"
    test_file.write_text(csv_content)

    # Call the function
    ride_requests = read_ride_requests(str(test_file))

    # Expected output
    expected = [
        {'company_name': 'Company A', 'destination': 'Destination X', 'number_of_rides_requested': 100},
        {'company_name': 'Company B', 'destination': 'Destination Y', 'number_of_rides_requested': 200},
    ]

    assert ride_requests == expected, "Failed to read ride requests correctly."


def test_aggregate_requests():
    ride_requests = [
        {'company_name': 'Company A', 'destination': 'Destination X', 'number_of_rides_requested': 100},
        {'company_name': 'Company B', 'destination': 'Destination X', 'number_of_rides_requested': 200},
        {'company_name': 'Company C', 'destination': 'Destination Y', 'number_of_rides_requested': 150},
    ]
    expected_output = {'Destination X': 300, 'Destination Y': 150}
    assert aggregate_requests(ride_requests) == expected_output, "Failed to aggregate requests correctly."


def test_request_rides_from_transit_agency():
    requested_rides = {'Destination X': 300, 'Destination Y': 150}
    approved_rides = request_rides_from_transit_agency(requested_rides)

    # Ensure approved rides are less than or equal to requested rides
    for destination, approved in approved_rides.items():
        assert approved <= requested_rides[destination] and approved >= 1, "Approved rides are not within expected range."


def test_distribute_rides():
    company_requests = [
        {'company_name': 'Company A', 'destination': 'Destination X', 'number_of_rides_requested': 100},
        {'company_name': 'Company B', 'destination': 'Destination X', 'number_of_rides_requested': 200},
    ]
    approved_rides = {'Destination X': 150}

    distribution = distribute_rides(company_requests, approved_rides)

    # Total distributed rides should not exceed approved rides
    total_distributed = sum([rides for _, _, rides in distribution])
    assert total_distributed <= approved_rides['Destination X'], "Distributed rides exceed approved rides."

    # Each company's allocated rides should be proportional to their request
    # Additional checks can be added here

# Additional tests can be added for edge cases and error handling
