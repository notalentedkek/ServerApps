class Product:
    def __init__(self, name, price, weight, category):
        self.name = name
        self.price = price
        self.weight = weight
        self.category = category

    def __repr__(self):
        return f"{self.name} (Цена: {self.price} руб., Вес: {self.weight} кг, Категория: {self.category})"

class Van:
    def __init__(self, max_volume, max_cost):
        self.max_volume = max_volume  # объем в куб. метрах
        self.max_cost = max_cost      # сумма в рублях
        self.loaded_products = []

    def load_products(self, products):
        total_volume = 0
        total_cost = 0
        for product in products:
            # Предположим, объем товара пропорционален весу (например, 1 кг = 0.02 м3)
            volume = product.weight * 0.02
            if (total_volume + volume <= self.max_volume) and (total_cost + product.price <= self.max_cost):
                self.loaded_products.append(product)
                total_volume += volume
                total_cost += product.price

    def sort_products_by_price_weight_ratio(self):
        self.loaded_products.sort(key=lambda p: p.price / p.weight)

    def find_products_in_price_range(self, min_price, max_price):
        return [p for p in self.loaded_products if min_price <= p.price <= max_price]

# Создаем список товаров
products = [
    Product("Кофе зерно", 1500, 1, "зерно"),
    Product("Молотый кофе", 1200, 0.8, "молотый"),
    Product("Растворимый кофе", 800, 0.5, "растворимый"),
    Product("Кофе в пакетиках", 1000, 0.7, "пакетированный"),
    Product("Кофе молотый растворимый", 900, 0.6, "растворимый"),
]

# Создаем фургон с объемом 0.1 м3 и суммой 3000 руб.
van = Van(max_volume=0.1, max_cost=3000)

# Загружаем товары
van.load_products(products)

# Сортируем по соотношению цена/вес
van.sort_products_by_price_weight_ratio()

# Находим товары по диапазону цен
matched_products = van.find_products_in_price_range(800, 1500)

# Вывод результатов
print("Загруженные товары:")
for p in van.loaded_products:
    print(p)

print("\nТовары в диапазоне цен 800-1500 руб.:")
for p in matched_products:
    print(p)