import os
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from decimal import Decimal
from datetime import datetime
from collections import Counter


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
        new_index = (f'{len(index_lines)},{model.index()}\n')
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
        new_index = (f'{len(index_lines)},{car.index()}\n')
        index_lines.append(new_index)
        index_lines.sort()
        
        with open(self.cars_index, 'w') as f:
            f.writelines(index_lines)
        return car
 
    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        with open(self.sales, 'a') as f:
            sale_data = f"{sale.sales_number},{sale.car_vin},{sale.sales_date},{sale.cost}\n"
            f.write(sale_data)  

        with open(self.sales_index, 'a') as f:
            sale_index_data = f"{sale.sales_number},{len(open(self.sales).readlines())-1}\n"
            f.write(sale_index_data)  

        with open(self.cars, 'r+') as f:
            lines = f.readlines()

        for i in range(len(lines)):
            data = lines[i].strip().split(",")
            if data[0] == sale.car_vin:
                data[4] = 'sold' 
                lines[i] = ','.join(data) + '\n'  

        with open(self.cars, 'w') as f:
            f.writelines(lines)


    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        cars = []
        with open(self.cars, "r") as f:
            for line in f:
                data = line.strip().split(",")
                if data and len(data) >= 5 and data[4] == status.value:
                    cars.append(Car(vin=data[0], model=data[1], price=Decimal(data[2]), date_start=datetime.strptime(data[3], "%Y-%m-%d %H:%M:%S"), status=status))
        return cars



    # Задание 4: Получить информацию по VIN
    def get_car_info(self, vin: str) -> CarFullInfo | None:
            with open(self.cars, 'r') as f:
                lines = f.readlines()
            car = []    
            for line in lines:
                data = line.strip().split(',')
                if data[0] == vin:
                    car = data
                    break

            if not car:
                return None

            with open(self.models, 'r') as f:
                lines = f.readlines()
            models = []
            for line in lines:
                data = line.strip().split(',')
                models.append(data)
            model_car = models[int(car[1]) - 1]
            info_car = car + model_car

            model_name = info_car[5]
            model_brand = info_car[6]
            price = info_car[2]
            date_start = info_car[3]
            status = info_car[4]

            sales_date = None
            sales_cost = None
            if info_car[4] == 'sold':
                with open(self.sales, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    if data[1] == vin:
                        sales_date = data[2]
                        sales_cost = Decimal(data[3])

            return CarFullInfo(
                vin=vin,
                car_model_name=model_name,
                car_model_brand=model_brand,
                price=Decimal(price),
                date_start=datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S"),
                status=status,
                sales_date=sales_date,
                sales_cost=sales_cost
            )


    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
            with open(self.cars, 'r+') as f:
                lines = f.readlines()

            vin_found = False   

            for i in range(len(lines)):
                data = lines[i].strip().split(",")
                if data[0] == vin:
                    data[0] = new_vin
                    lines[i] = ','.join(data) + '\n'
                    vin_found = True
                    break  

            if vin_found:
                with open(self.cars, 'w') as f:
                    f.writelines(lines)
                return f'VIN updated from {vin} to {new_vin}.'
            else:
                return 'VIN not found.'

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        with open(self.sales, 'r') as f:
            lines = f.readlines()

        sale_found = False
        sale_car_id = sales_number[9:] 

        for i in range(len(lines)):
            data = lines[i].strip().split(",")
            if data[0] == sales_number:
                sale_found = True
                lines[i] = ''  
                break

        if sale_found:
            with open(self.sales, 'w') as f:
                f.writelines(lines)

            with open(self.cars, 'r') as f:
                lines = f.readlines()

            for i in range(len(lines)):
                data = lines[i].strip().split(",")
                if data[0] == sale_car_id:
                    data[4] = 'available'  
                    lines[i] = ','.join(data) + '\n'
                    break

            with open(self.cars, 'w') as f:
                f.writelines(lines)

        else:
            print("Sale not found.")
            return None


    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
            with open(self.cars, 'r') as f:
                lines = f.readlines()
            car = []    
            for line in lines:
                data = line.strip().split(',')
                if data[4] == 'sold':
                    car.append(data[1])
            wer = Counter(car)
            del wer['2']
            print(wer)

            with open(self.models, 'r') as f:
                lines = f.readlines()
            models = []
            for line in lines:
                data = line.strip().split(',')
                models.append(data)
            print(models)
            result = []
            for k in wer.most_common(3):
                print(k)
                car = models[int(k[0]) - 1]
                result.append(ModelSaleStats(car_model_name=car[0],
                                            brand=car[1],
                                            sales_number=wer[k[0]]))
            return result[:3]
