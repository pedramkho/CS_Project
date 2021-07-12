from samples import poisson
from client import Client
import numpy as np


def get_customer_group(cur_time, arrival_rate=1.0, tolerance_rate=0.5):
    num_customers = poisson(arrival_rate)
    customers = []
    for i in range(num_customers):
        customers.append(Client(cur_time, tolerance_rate))

    return customers


def find_shortest_queue_section(section_list):
    sorted_list = sorted(section_list, key=lambda x: len(x.queue))
    shortest_queue_section = sorted_list[0]

    if len(shortest_queue_section.queue) != 0:
        return shortest_queue_section

    empty_queue_sections = list(
        filter(lambda x: len(x.queue) == 0, sorted_list))
    ind = np.random.randint(len(empty_queue_sections))

    return empty_queue_sections[ind]


def is_empty_restaraunt(section, sections):
    is_empty_sections = [r.is_empty() for r in sections]
    return all(is_empty_sections) and section.is_empty()


def queue_log(section, sections):
    for r in sections:
        r.queue_log()
    section.queue_log()
