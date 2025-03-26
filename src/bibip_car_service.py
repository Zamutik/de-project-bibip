import os
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal
from datetime import datetime


class CarService: 
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.cars = os.path.join(root_directory_path, 'cars.txt')
        self.cars_index = os.path.join(root_directory_path, 'cars_index.txt')
        self.models = os.path.join(root_directory_path, 'models.txt')
        self.models_index = os.path.join(root_directory_path, 'models_index.txt')
        self.sales = os.path.join(root_directory_path, 'sales.txt')
        self.sales_index = os.path.join(root_directory_path, 'sales_index.txt')
        self._initialize_files()

 
    def _initialize_files(self):
        if not os.path.exists(self.cars):
            with open(self.cars, 'w') as f:
                pass
        if not os.path.exists(self.cars_index):
            with open(self.cars_index, 'w') as f:
                pass
        if not os.path.exists(self.models):
            with open(self.models, 'w') as f:
                pass
        if not os.path.exists(self.models_index):
            with open(self.models_index, 'w') as f:
                pass
        if not os.path.exists(self.sales):
            with open(self.sales, 'w') as f:
                pass
        if not os.path.exists(self.sales_index):
            with open(self.sales_index, 'w') as f:
                pass

    # Задание 1. Сохранение модели 
    def add_model(self, model: Model) -> Model:
        with open(self.models, 'a') as f:
            f.write(f"{model.name},{model.brand}\n")
        with open(self.models_index, 'r') as f:
            index_lines = f.readlines()
        new_index = (f'{model.index()},{len(index_lines)}\n')
        index_lines.append(new_index)
        index_lines.sort()
        with open(self.models_index, 'w') as f:
            f.writelines(index_lines)
        return model

    # Задание 1. Сохранение автомобиля
    def add_car(self, car: Car) -> Car:
        with open(self.cars, 'a') as f:
           f.write(f"{car.vin},{car.model},{car.price},{car.date_start},{car.status}\n")
        with open(self.cars_index, 'r') as f:
            index_lines = f.readlines()
        new_index = (f'{car.index()},{len(index_lines)}\n')
        index_lines.append(new_index)
        index_lines.sort()
        with open(self.cars_index, 'w') as f:
            f.writelines(index_lines)
        return car
 
    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        with open(self.sales, 'a') as f:
            f.write(f"{sale.sales_number},{sale.car_vin},{sale.sales_date},{sale.cost}\n")
        with open(self.sales_index, 'a') as f:
            index_lines = f.readlines()
        new_index = (f'{sale.index()},{len(index_lines)}\n')
        index_lines.append(new_index)
        index_lines.sort()           






    def get_car_by_vin(self, vin: str) -> Car:
        with open(self.cars, "r") as f:
            for line in f:
                car_vin, model, price, date_start, status = line.strip().split(",")
                if car_vin == vin:
                    return Car(vin=car_vin, model=int(model), price=Decimal(price), date_start=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"), status=CarStatus(status))
        return None


    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        cars = []
        with open("cars.txt", "r") as f:
            for line in f:
                car_vin, model, price, date_start, status = line.strip().split(",")
            if status == status:
                cars.append(Car(vin=car_vin, model=model, price=Decimal(price), date_start=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"), status=status))
            return cars


    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        with open("cars.txt", "r") as f:
            for line in f:
                car_vin, model, price, date_start, status = line.strip().split(",")
            if car_vin == vin:
                return CarFullInfo(vin=car_vin, model=model, price=Decimal(price), date_start=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"), status=status)
            return None

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        with open("cars.txt", "r+") as f:
            lines = f.readlines()
            for line in lines:
                car_vin, model, price, date_start, status = line.strip().split(",")
            if car_vin == vin:
                car_vin = new_vin
            lines[0] = f"{car_vin},{model},{price},{date_start},{status}"
            f.seek(0)
            f.truncate()
            f.writelines(lines)
            return Car(vin=vin, model=model, price=Decimal(price), date_start=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"), status=status)

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        sale = self.get_sale_by_number(sales_number)  
        if sale:
            car = self.get_car_by_vin(sale.vin)
            if car:
                car.status = CarStatus.AVAILABLE
                self.sales.remove(sale)  
                return car
        raise ValueError("Sale not found")

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError

