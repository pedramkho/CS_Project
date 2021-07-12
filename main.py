import numpy as np
from matplotlib import pyplot as plt
import argparse
import os

from simulation import run_simulation

CUSTOMER_COUNT = 10 ** 7

parser = argparse.ArgumentParser()

parser.add_argument("--address", type=str, help="figures address", default='./')
args = parser.parse_args()
print(args.address)

os.makedirs(args.address, exist_ok=True)

print("Input: section_count, arrival_rate, tolerance_avg and service_rate")
section_count, arrival_rate, tolerance_avg, service_rate = list(
    map(int, input().split()))
service_times = [list(map(int, input().split())) for _ in range(section_count)]

customers, sections, operator = run_simulation(
    section_count, arrival_rate, tolerance_avg, service_rate, service_times)

print("Simulation results.")
print("Q1 _______________________________________________________________")
spent_time_0 = [round(p.departure_time - p.arrival_time)
                for p in customers if p.has_priority(0)]
spent_time_1 = [round(p.departure_time - p.arrival_time)
                for p in customers if p.has_priority(1)]
spent_time_2 = [round(p.departure_time - p.arrival_time)
                for p in customers if p.has_priority(2)]
spent_time_3 = [round(p.departure_time - p.arrival_time)
                for p in customers if p.has_priority(3)]
spent_time_4 = [round(p.departure_time - p.arrival_time)
                for p in customers if p.has_priority(4)]

spent_time_all = [round(p.departure_time - p.arrival_time) for p in customers]

print("Mean spent time of p0 customers : ", np.mean(spent_time_0))
print("Mean spent time of p1 customers : ", np.mean(spent_time_1))
print("Mean spent time of p2 customers : ", np.mean(spent_time_2))
print("Mean spent time of p3 customers : ", np.mean(spent_time_3))
print("Mean spent time of p4 customers : ", np.mean(spent_time_4))

print("Mean spent time of all customers : ", np.mean(spent_time_all))

print("Q2 _______________________________________________________________")

waiting_time_0 = [round(p.waiting_time)
                  for p in customers if p.has_priority(0)]
waiting_time_1 = [round(p.waiting_time)
                  for p in customers if p.has_priority(1)]
waiting_time_2 = [round(p.waiting_time)
                  for p in customers if p.has_priority(2)]
waiting_time_3 = [round(p.waiting_time)
                  for p in customers if p.has_priority(3)]
waiting_time_4 = [round(p.waiting_time)
                  for p in customers if p.has_priority(4)]

waiting_time_all = [round(p.waiting_time) for p in customers]

print("Mean waiting time of p0 customers : ", np.mean(waiting_time_0))
print("Mean waiting time of p1 customers : ", np.mean(waiting_time_1))
print("Mean waiting time of p2 customers : ", np.mean(waiting_time_2))
print("Mean waiting time of p3 customers : ", np.mean(waiting_time_3))
print("Mean waiting time of p4 customers : ", np.mean(waiting_time_4))

print("Mean waiting time of all customers : ", np.mean(waiting_time_all))

print("Q3 _______________________________________________________________")
left_queue_num = len([p for p in customers if p.left_queue])

print("Number of tired customers who left the queue: ", left_queue_num)

print("Q4 _______________________________________________________________")
mean_queue_len_section = np.mean(operator.queue_len_log)
mean_queue_len_sections = [np.mean(r.queue_len_log) for r in sections]

print("Mean length of section queue: ", mean_queue_len_section)
for i in range(len(mean_queue_len_sections)):
    print("Mean length of queue for section" +
          str(i + 1) + ": ", mean_queue_len_sections[i])

print("Q5 _______________________________________________________________")
accuracy = 1
num_customers = 10
while accuracy > 0.05:
    num_customers += 10
    customers_prim, sections_prim, section_prim = run_simulation(section_count, arrival_rate, tolerance_avg, service_rate,
                                                                 service_times, num_customers)

    waiting_time = [p.waiting_time for p in customers_prim]
    sigma = np.std(waiting_time)
    mean = np.mean(waiting_time)
    accuracy = (1.96 * sigma) / (num_customers * mean)
print("Accuracy of 0.95 is reached with", num_customers, "customers.")

print("Q6 _______________________________________________________________")
mean_queue_len_all = np.mean(mean_queue_len_sections)
iteration = 1
mean_queue_len_list = [mean_queue_len_all]

while mean_queue_len_all > 10 ** -5:
    new_service_times = [[service_times[i][j] + (iteration * int(np.log10(CUSTOMER_COUNT)))
                          for j in range(len(service_times[i]))] for i in range(len(service_times))]
    new_customers, new_sections, new_section = run_simulation(
        section_count, arrival_rate, tolerance_avg, service_rate, new_service_times)
    mean_queue_len_all = np.mean(
        [np.mean(r.queue_len_log) for r in new_sections])
    mean_queue_len_list.append(mean_queue_len_all)
    iteration += 1


else:
    plt.plot([i + 1 for i in range(len(mean_queue_len_list))],
             mean_queue_len_list)
    plt.title('Q6')
    plt.ylabel('mean queue len')
    plt.xlabel('iteration')
    plt.savefig(args.address + 'Q6.pdf')
    plt.clf()

    print("No queue will exist if:")
    for i in range(len(new_service_times)):
        print("Service time of doctors of section" +
              str(i + 1) + ": ", new_service_times[i])


print("Q7.1 _______________________________________________________________")
colors = {'p0': 'r',
          'p1': 'r',
          'p2': 'r',
          'p3': 'r',
          'p4': 'r',
          'all': 'b'}
response_time_0 = [round(p.service_time + p.section_time)
                   for p in customers if (p.has_priority(0) and not p.left_queue)]

response_time_1 = [round(p.service_time + p.section_time)
                   for p in customers if (p.has_priority(1) and not p.left_queue)]

response_time_2 = [round(p.service_time + p.section_time)
                   for p in customers if (p.has_priority(2) and not p.left_queue)]

response_time_3 = [round(p.service_time + p.section_time)
                   for p in customers if (p.has_priority(3) and not p.left_queue)]

response_time_4 = [round(p.service_time + p.section_time)
                   for p in customers if (p.has_priority(4) and not p.left_queue)]


try:
    plt.hist(response_time_0, bins=max(
        response_time_0), color=colors['p0'])
    plt.title("Response time frequency of p0 customers")
    plt.savefig(args.address + 'Q7.1.1.pdf')
    plt.clf()
except Exception:
    print("There is no response list for t1 customers")

try:
    plt.hist(response_time_1, bins=max(
        response_time_1), color=colors['p0'])
    plt.title("Response time frequency of p1 customers")
    plt.savefig(args.address + 'Q7.1.2.pdf')
    plt.clf()
except Exception:
    print("There is no response list for p2 customers")

try:
    plt.hist(response_time_2, bins=max(
        response_time_2), color=colors['p2'])
    plt.title("Response time frequency of p2 customers")
    plt.savefig(args.address + 'Q7.1.3.pdf')
    plt.clf()
except Exception:
    print("There is no response list for p2 customers")

try:
    plt.hist(response_time_3, bins=max(
        response_time_3), color=colors['p3'])
    plt.title("Response time frequency of p3 customers")
    plt.savefig(args.address + 'Q7.1.4.pdf')
    plt.clf()
except Exception:
    print("There is no response list for p3 customers")

try:
    plt.hist(response_time_4, bins=max(
        response_time_4), color=colors['p4'])
    plt.title("Response time frequency of p4 customers")
    plt.savefig(args.address + 'Q7.1.5.pdf')
    plt.clf()
except Exception:
    print("There is no response list for p4 customers")

print("Q7.2 _______________________________________________________________")

counter = 1
try:
    plt.hist(waiting_time_0, bins=max(
        waiting_time_0), color=colors['p0'])
    plt.title("Waiting time frequency of p0 customers")
    plt.savefig(args.address + 'Q7.2.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no waiting list for p0 customers")

try:
    plt.hist(waiting_time_1, bins=max(
        waiting_time_1), color=colors['p1'])
    plt.title("Waiting time frequency of p1 customers")
    plt.savefig(args.address + 'Q7.2.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no waiting list for p1 customers")


try:
    plt.hist(waiting_time_2, bins=max(
        waiting_time_2), color=colors['p2'])
    plt.title("Waiting time frequency of p2 customers")
    plt.savefig(args.address + 'Q7.2.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no waiting list for p2 customers")

try:
    plt.hist(waiting_time_3, bins=max(
        waiting_time_3), color=colors['p3'])
    plt.title("Waiting time frequency of p3 customers")
    plt.savefig(args.address + 'Q7.2.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no waiting list for p3 customers")


try:
    plt.hist(waiting_time_4, bins=max(
        waiting_time_4), color=colors['p4'])
    plt.title("Waiting time frequency of p4 customers")
    plt.savefig(args.address + 'Q7.2.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no waiting list for p4 customers")

print("Q7.3 _______________________________________________________________")
counter = 1
try:
    plt.hist(spent_time_0, bins=max(spent_time_0), color=colors['p0'])
    plt.title("Spent time frequency of p0 customers")
    plt.savefig(args.address + 'Q7.3.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no spent time list for p0 customers")

try:
    plt.hist(spent_time_1, bins=max(spent_time_1), color=colors['p1'])
    plt.title("Spent time frequency of p1 customers")
    plt.savefig(args.address + 'Q7.3.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no spent time list for p1 customers")

try:
    plt.hist(spent_time_2, bins=max(spent_time_2), color=colors['p2'])
    plt.title("Spent time frequency of p2 customers")
    plt.savefig(args.address + 'Q7.3.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no spent time list for p2 customers")


try:
    plt.hist(spent_time_3, bins=max(spent_time_3), color=colors['p3'])
    plt.title("Spent time frequency of p3 customers")
    plt.savefig(args.address + 'Q7.3.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no spent time list for p3 customers")

try:
    plt.hist(spent_time_4, bins=max(spent_time_4), color=colors['p4'])
    plt.title("Spent time frequency of p4 customers")
    plt.savefig(args.address + 'Q7.3.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no spent time list for p4 customers")

# TILL HERE AMIRREZA
print("Q7.4 _______________________________________________________________")
presence_times_0 = []
presence_times_1 = []
presence_times_2 = []
presence_times_3 = []
presence_times_4 = []

counter = 1

for p in customers:
    if p.has_priority(0):
        presence_times_0 += [i for i in range(
            p.arrival_time, round(p.departure_time) + 1)]

    elif p.has_priority(1):
        presence_times_1 += [i for i in range(
            p.arrival_time, round(p.departure_time) + 1)]

    elif p.has_priority(2):
        presence_times_2 += [i for i in range(
            p.arrival_time, round(p.departure_time) + 1)]

    elif p.has_priority(3):
        presence_times_3 += [i for i in range(
            p.arrival_time, round(p.departure_time) + 1)]

    elif p.has_priority(4):
        presence_times_4 += [i for i in range(
            p.arrival_time, round(p.departure_time) + 1)]

presence_times = presence_times_0 + presence_times_1 + \
    presence_times_2 + presence_times_3 + presence_times_4

try:
    plt.hist(presence_times_0, bins=max(presence_times_0),
             color=colors['p0'], histtype='step')
    plt.title("Presence time of p0 customers")
    plt.savefig(args.address + 'Q7.4.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no Presence time list for p0 customers")

try:
    plt.hist(presence_times_1, bins=max(presence_times_1),
             color=colors['p1'], histtype='step')
    plt.title("Presence time of p1 customers")
    plt.savefig(args.address + 'Q7.4.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no Presence time list for p1 customers")

try:
    plt.hist(presence_times_2, bins=max(presence_times_2),
             color=colors['p2'], histtype='step')
    plt.title("Presence time of p2 customers")
    plt.savefig(args.address + 'Q7.4.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no Presence time list for p2 customers")

try:
    plt.hist(presence_times_3, bins=max(presence_times_3),
             color=colors['p3'], histtype='step')
    plt.title("Presence time of p3 customers")
    plt.savefig(args.address + 'Q7.4.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no Presence time list for p3 customers")

try:
    plt.hist(presence_times_4, bins=max(presence_times_4),
             color=colors['p4'], histtype='step')
    plt.title("Presence time of p4 customers")
    plt.savefig(args.address + 'Q7.4.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no Presence time list for p4 customers")

try:
    plt.hist(presence_times, bins=max(presence_times),
             color=colors['all'], histtype='step')
    plt.title("Presence time of all customers")
    plt.savefig(args.address + 'Q7.4.' + str(counter) + '.pdf')
    coutner += 1
    plt.clf()
except Exception:
    print("There is no Presence time list for all customers")

print("Q7.5 _______________________________________________________________")
counter = 1

overall_queue = [l for l in operator.queue_len_log]

plt.plot(operator.queue_lens["p0"], label='t1', color=colors['p0'])
plt.title('Q7.5')
plt.ylabel('Queue len section of p0 customers')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()

overall_queue = [l for l in operator.queue_len_log]
plt.plot(operator.queue_lens["p1"], label='t1', color=colors['p1'])
plt.title('Q7.5')
plt.ylabel('Queue len section of p1 customers')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()

overall_queue = [l for l in operator.queue_len_log]
plt.plot(operator.queue_lens["p2"], label='t1', color=colors['p2'])
plt.title('Q7.5')
plt.ylabel('Queue len section of p2 customers')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()

overall_queue = [l for l in operator.queue_len_log]
plt.plot(operator.queue_lens["p3"], label='t1', color=colors['p3'])
plt.title('Q7.5')
plt.ylabel('Queue len section of p3 customers')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()

plt.plot(operator.queue_lens["p4"], label='t1', color=colors['p4'])
plt.title('Q7.5')
plt.ylabel('Queue len section of p4 customers')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()

plt.plot(operator.queue_len_log, label='all', color=colors['all'])
plt.title('Q7.5')
plt.ylabel('Queue len section of all customers')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()

for i in range(len(sections)):
    r = sections[i]
    overall_queue = [overall_queue[i] + r.queue_len_log[i]
                     for i in range(len(overall_queue))]

    plt.plot(r.queue_lens["p0"], label='p0', color=colors['p1'])
    plt.title('Q7.5')
    plt.ylabel('Queue len of p0 customers of section' + str(i+1))
    plt.xlabel('time')
    plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
    counter += 1
    plt.clf()

    plt.plot(r.queue_lens["p1"], label='p1', color=colors['p1'])
    plt.title('Q7.5')
    plt.ylabel('Queue len of p1 customers of section' + str(i+1))
    plt.xlabel('time')
    plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
    counter += 1
    plt.clf()

    plt.plot(r.queue_lens["p2"], label='p2', color=colors['p2'])
    plt.title('Q7.5')
    plt.ylabel('Queue len of p2 customers of section' + str(i+1))
    plt.xlabel('time')
    plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
    counter += 1
    plt.clf()

    plt.plot(r.queue_lens["p3"], label='p3', color=colors['p3'])
    plt.title('Q7.5')
    plt.ylabel('Queue len of p3 customers of section' + str(i+1))
    plt.xlabel('time')
    plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
    counter += 1
    plt.clf()

    plt.plot(r.queue_lens["p4"], label='p4', color=colors['p4'])
    plt.title('Q7.5')
    plt.ylabel('Queue len of t1 customers of section' + str(i+1))
    plt.xlabel('time')
    plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
    counter += 1
    plt.clf()

    plt.plot(r.queue_len_log, label='all', color=colors['all'])
    plt.title('Q7.5')
    plt.ylabel('Queue len of all customers of section' + str(i+1))
    plt.xlabel('time')
    plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
    counter += 1
    plt.clf()

plt.plot(overall_queue, label='all', color=colors['all'])
plt.title('Q7.5')
plt.ylabel('Queue len of all customers of sections & section')
plt.xlabel('time')
plt.savefig(args.address + 'Q7.5.' + str(counter) + '.pdf')
counter += 1
plt.clf()
