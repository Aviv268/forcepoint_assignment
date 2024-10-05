import csv
import logging
import os
import pprint
import random


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/ride_allocation.log'),
        logging.StreamHandler()
    ]
)


def read_ride_requests(file_path):
    ride_requests = []
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['number_of_rides_requested'] = int(row['number_of_rides_requested'])
                ride_requests.append(row)
        logging.info('Successfully read ride requests from CSV.')
    except FileNotFoundError:
        logging.error(f'File not found: {file_path}')
        raise
    except Exception as e:
        logging.error(f'Error reading CSV file: {e}')
        raise
    return ride_requests


def aggregate_requests(ride_requests):
    aggregated_requests = {}
    for request in ride_requests:
        destination = request['destination']
        rides_requested = request['number_of_rides_requested']
        if destination in aggregated_requests:
            aggregated_requests[destination] += rides_requested
        else:
            aggregated_requests[destination] = rides_requested
    logging.info('Aggregated ride requests by destination.')
    return aggregated_requests


def request_rides_from_transit_agency(requested_rides):
    approved_rides = {}
    for destination, requested in requested_rides.items():
        approved = random.randint(int(requested * 0.5), requested)
        approved_rides[destination] = approved
    logging.info('Approved rides from transit agency.')
    return approved_rides


def distribute_rides(ride_requests, approved_rides):
    company_distribution = []

    for destination, approved in approved_rides.items():
        destination_requests = [req for req in ride_requests if req['destination'] == destination]
        total_requested = sum(req['number_of_rides_requested'] for req in destination_requests)

        for req in destination_requests:
            company = req['company_name']
            rides_requested = req['number_of_rides_requested']
            proportional_share = (rides_requested / total_requested) * approved
            allocated_rides = int(proportional_share // 100 * 100)
            allocated_rides = min(allocated_rides, rides_requested)
            company_distribution.append({
                'company_name': company,
                'destination': destination,
                'number_of_rides_approved': allocated_rides
            })

    logging.info('Distributed approved rides to companies.')
    return company_distribution


# old version distribute_rides*******
# def distribute_rides(company_requests, approved_rides):
#     company_distribution = []
#
#     for request in company_requests:
#         company = request['company_name']
#         destination = request['destination']
#         rides_requested = request['number_of_rides_requested']
#
#         if destination in approved_rides:
#             approved = approved_rides[destination]
#             allocation_ratio = min(approved / rides_requested, 1)  # Proportionally allocate
#             company_rides = int(allocation_ratio * rides_requested // 100 * 100)  # Rounded down to nearest 100
#             company_distribution.append((company, destination, company_rides))
#             approved_rides[destination] -= company_rides  # Reduce available rides
#
#     return company_distribution
# old version *******

def write_ride_allocations(file_path, company_distribution):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['company_name', 'destination', 'number_of_rides_approved']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for allocation in company_distribution:
                writer.writerow(allocation)
        logging.info('Successfully wrote ride allocations to CSV.')
    except Exception as e:
        logging.error(f'Error writing CSV file: {e}')
        raise


def main():
    input_file_path = os.path.join('../data', 'ride_requests.csv')
    output_file_path = os.path.join('../data', 'ride_allocations.csv')

    # Step 1: Read ride requests
    ride_requests = read_ride_requests(input_file_path)

    # Step 2: Aggregate requests per destination
    aggregated_requests = aggregate_requests(ride_requests)

    # Step 3: Request approved rides from transit agency
    approved_rides = request_rides_from_transit_agency(aggregated_requests)

    # Step 4: Distribute approved rides to companies
    company_distribution = distribute_rides(ride_requests, approved_rides)

    # Step 5: Write the distribution to an output file
    write_ride_allocations(output_file_path, company_distribution)


if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     input_file_path = os.path.join('../data', 'ride_requests.csv')
#     ride_requests = read_ride_requests(input_file_path)
#     pprint.pprint(('Ride Requests:', ride_requests))
#
#     aggregated_ride_requests = aggregate_requests(ride_requests)
#
#     # Print to verify
#     print('Aggregated Requests:', aggregated_ride_requests)
#
#     approved_rides = request_rides_from_transit_agency(aggregated_ride_requests)
#     print('Approved Rides:', approved_rides)
#
#     company_distribution = distribute_rides(ride_requests, approved_rides)
#     print(company_distribution)
