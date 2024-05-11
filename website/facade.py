from website.repository import ManagerRepository, CarRepository, ResRepository

class CarRentalFacade:
    def __init__(self):
        self.manager_repository = ManagerRepository()
        self.car_repository = CarRepository()
        self.res_repository = ResRepository()

    def get_all_managers(self):
        return self.manager_repository.get_all_managers()

    def get_all_cars(self):
        return self.car_repository.get_all_cars()

    def get_all_reservations(self):
        return self.res_repository.get_all_reservations()
