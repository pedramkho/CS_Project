import time

from my_operator import Operator
from section import Section
from utils import *

CUSTOMER_COUNT = 10 ** 7


def run_simulation(section_count, arrival_rate, tolerance_avg, service_rate, service_times, CUSTOMER_COUNT=CUSTOMER_COUNT):
    print("Simulation starts.")
    system_time = 0
    customers = []
    sections = [Section(service_times[_]) for _ in range(section_count)]
    operator = Operator(service_rate)

    start_time = time.time()

    while len(customers) < CUSTOMER_COUNT or not (is_empty_restaraunt(operator, sections)):
        operator.remove_tired_customers(system_time)
        for r in sections:
            r.remove_tired_customers(system_time)

        cur_customers = get_customer_group(
            system_time, arrival_rate, tolerance_avg)
        customers += cur_customers
        if len(customers) > CUSTOMER_COUNT:
            extras = len(customers) - CUSTOMER_COUNT
            customers = customers[:CUSTOMER_COUNT]
            cur_customers = cur_customers[:(len(cur_customers) - extras)]

        operator.add_customers(cur_customers)

        cur_serving = operator.service()

        for p in cur_serving:
            section_p: Section = find_shortest_queue_section(sections)
            section_p.add_customers([p])

        for r in sections:
            r.service(system_time)

        queue_log(operator, sections)

        system_time += 1

    for p in customers:
        p.calculate_waiting_time()

    end_time = time.time()

    sym_duration = end_time - start_time
    print("Simulation ended in", sym_duration)
    print("Time of system", system_time)

    return customers, sections, operator
