from staff import Staff


class Section:
    def __init__(self, mean_list):
        self.queue = []
        self.mean_list = mean_list
        self.staff = [Staff(self.mean_list[i])
                      for i in range(len(self.mean_list))]
        self.queue_lens = {
            "p0": [], "p1": [], "p2": [], "p3": [], "p4": [],
        }
        self.queue_len_log = []

    def add_customers(self, customer_list):
        self.queue += customer_list
        self.queue = sorted(self.queue, key=lambda x: (
            x.priority, x.arrival_time))

    def service(self, cur_time):
        if len(self.queue) > 0:
            for personnel in self.staff:
                if len(self.queue) == 0:
                    break
                if personnel.is_busy(cur_time):
                    continue

                count = personnel.set_service_count()
                customers = self.queue[:count]
                self.queue = self.queue[count:]
                personnel.start_service(cur_time, customers)

    def remove_tired_customers(self, cur_time):
        for customer in self.queue:
            if customer.is_going_to_leave(cur_time):
                customer.leave()
                self.queue.remove(customer)

    def is_empty(self):
        if len(self.queue) > 0:
            return False
        return True

    def queue_log(self):
        self.queue_len_log.append(len(self.queue))
        p0_queue = [0 for c in self.queue if c.priority == 0]
        p1_queue = [0 for c in self.queue if c.priority == 1]
        p2_queue = [0 for c in self.queue if c.priority == 2]
        p3_queue = [0 for c in self.queue if c.priority == 3]
        p4_queue = [0 for c in self.queue if c.priority == 4]
        self.queue_lens["p0"].append(len(p0_queue))
        self.queue_lens["p1"].append(len(p1_queue))
        self.queue_lens["p2"].append(len(p2_queue))
        self.queue_lens["p3"].append(len(p3_queue))
        self.queue_lens["p4"].append(len(p4_queue))
