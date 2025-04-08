import os
import json
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


    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
            with open(self.cars, 'r+') as f:
                lines = f.readlines()
                print(lines)

            for i in range(len(lines)):
                data = lines[i].strip().split(",")
                print(data)
                if data[0] == vin:
                    data[0] = new_vin 
                    lines[i] = ','.join(data) + '\n'
            print(lines)

            with open(self.cars, 'w') as f:
                f.writelines(lines)

            with open(self.cars_index, 'r') as f:
                index_lines = f.readlines()
            for i in range(len(lines)):
                data = lines[i].strip().split(",")
            new_index = (f'{len(index_lines)},{data[0]}\n')
            index_lines.append(new_index)
            index_lines.sort()
    

    print(update_vin('KNAGM4A77D5316538', '159159159159'))


full_info_no_sale = CarFullInfo(
            vin="KNAGM4A77D5316538",
            car_model_name="Optima",
            car_model_brand="Kia",
            price=Decimal("2000"),
            date_start=datetime(2024, 2, 8),
            status=CarStatus.available,
            sales_date=None,
            sales_cost=None,
        )