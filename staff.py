from samples import poisson


class Staff:
    def __init__(self, service_mean):
        self.service_mean = service_mean
        self.service_count = service_mean

    def set_service_count(self):
        self.service_count = poisson(self.service_mean)
        return self.service_count

    def start_service(self, cur_time, customers):
        for p in customers:
            p.set_departure(cur_time + 1 / self.service_count + p.section_time)
            p.set_service_time(1 / self.service_count)
            cur_time += 1 / self.service_count

    def is_busy(self, cur_time):
        return False
