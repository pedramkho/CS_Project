from samples import uniform


class Client:
    def __init__(self, arrival, wait_rate):
        self.arrival_time = arrival
        self.departure_time = None
        self.priority = uniform()
        self.will_wait = wait_rate
        self.left_queue = False
        self.service_time = None
        self.section_time = None
        self.waiting_time = None

    def __str__(self):
        return "client<arrival: {}, departure: {}, service_time: {}, section_time: {}, waiting_time: {}>". \
            format(self.arrival_time, self.departure_time,
                   self.service_time, self.section_time, self.waiting_time)

    def set_departure(self, departure):
        self.departure_time = departure

    def set_service_time(self, service_time):
        self.service_time = service_time

    def is_going_to_leave(self, cur_time):
        if cur_time - self.arrival_time > self.will_wait:
            return True
        return False

    def leave(self):
        self.left_queue = True
        self.departure_time = self.arrival_time + self.will_wait

    def calculate_waiting_time(self):
        if self.left_queue:
            self.waiting_time = round(
                self.departure_time - self.arrival_time, 3)
        else:
            self.waiting_time = round(
                self.departure_time - self.arrival_time - self.service_time, 3)

    def has_priority(self, p):
        return self.priority == p
