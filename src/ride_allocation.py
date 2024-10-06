import csv
import logging
import os
import random
from src.utils.helpers import setup_logging


setup_logging()


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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    input_file_path = os.path.join(data_dir, 'ride_requests.csv')
    output_file_path = os.path.join(data_dir, 'ride_allocations.csv')

    ride_requests = read_ride_requests(input_file_path)
    aggregated_requests = aggregate_requests(ride_requests)
    approved_rides = request_rides_from_transit_agency(aggregated_requests)
    company_distribution = distribute_rides(ride_requests, approved_rides)
    write_ride_allocations(output_file_path, company_distribution)


if __name__ == '__main__':
    main()
