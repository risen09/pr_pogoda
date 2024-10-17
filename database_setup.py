import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('weather.db')
c = conn.cursor()

# Создание таблиц
c.execute('''
CREATE TABLE IF NOT EXISTS Account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS RegionType (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Region (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    region_type_id INTEGER,
    FOREIGN KEY (region_type_id) REFERENCES RegionType(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    wind_speed REAL NOT NULL,
    weather_condition TEXT NOT NULL,
    measurement_date_time TEXT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Region(id)
)
''')

# Добавление данных в таблицы
accounts = [
    ('John', 'Doe', 'john.doe@example.com', 'hash1'),
    ('Jane', 'Doe', 'jane.doe@example.com', 'hash2'),
    ('Jim', 'Beam', 'jim.beam@example.com', 'hash3'),
    ('Jack', 'Daniels', 'jack.daniels@example.com', 'hash4'),
    ('Johnny', 'Walker', 'johnny.walker@example.com', 'hash5'),
    ('Jessie', 'Pinkman', 'jessie.pinkman@example.com', 'hash6'),
    ('Walter', 'White', 'walter.white@example.com', 'hash7'),
    ('Clark', 'Kent', 'clark.kent@example.com', 'hash8'),
    ('Bruce', 'Wayne', 'bruce.wayne@example.com', 'hash9'),
    ('Peter', 'Parker', 'peter.parker@example.com', 'hash10')
]
c.executemany('INSERT INTO Account (first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?)', accounts)

region_types = [
    ('City',), ('Countryside',), ('Mountain',), ('Coastal',), ('Desert',),
    ('Forest',), ('Tundra',), ('Swamp',), ('River',), ('Lake',)
]

c.executemany('INSERT INTO RegionType (type_name) VALUES (?)', region_types)

regions = [
    ('New York', 1), ('Los Angeles', 1), ('Chicago', 1), ('Houston', 1), ('Phoenix', 1),
    ('Philadelphia', 1), ('San Antonio', 1), ('San Diego', 1), ('Dallas', 1), ('San Jose', 1)
]
c.executemany('INSERT INTO Region (name, region_type_id) VALUES (?, ?)', regions)

weathers = [
    (1, 75.0, 50.0, 5.0, 'Clear', '2021-07-01T12:00:00Z'),
    (2, 85.0, 40.0, 10.0, 'Sunny', '2021-07-01T13:00:00Z'),
    (3, 60.0, 30.0, 2.0, 'Cloudy', '2021-07-01T14:00:00Z'),
    (4, 70.0, 45.0, 20.0, 'Rainy', '2021-07-01T15:00:00Z'),
    (5, 90.0, 10.0, 0.0, 'Windy', '2021-07-01T16:00:00Z'),
    (6, 88.0, 25.0, 15.0, 'Snow', '2021-07-01T17:00:00Z'),
    (7, 77.0, 35.0, 5.0, 'Foggy', '2021-07-01T18:00:00Z'),
    (8, 66.0, 55.0, 6.0, 'Hail', '2021-07-01T19:00:00Z'),
    (9, 59.0, 60.0, 12.0, 'Storm', '2021-07-01T20:00:00Z'),
    (10, 80.0, 20.0, 9.0, 'Blizzard', '2021-07-01T21:00:00Z')
]
c.executemany('INSERT INTO Weather (region_id, temperature, humidity, wind_speed, weather_condition, measurement_date_time) VALUES (?, ?, ?, ?, ?, ?)', weathers)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
