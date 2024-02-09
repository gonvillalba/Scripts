import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biblioteca.settings")

django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker
import random
import csv
import random
import psycopg2
from biblioteca_app.models import Usuario

fake = Faker()

def create_libro_data(num_records):
    data = []
    for _ in range(num_records):
        titulo = fake.sentence(nb_words=3)
        autor = fake.name()
        genero = random.choice(['Fiction', 'Non-Fiction', 'Sci-Fi', 'Mystery', 'Thriller', 'Romance'])
        year_publication = fake.date_time_this_decade().strftime('%Y-%m-%d')
        data.append([titulo, autor, genero, year_publication])
    return data

def create_user_data():
    data = []
    arrays = [
        ['juan',  fake.email(), random.choice(['normal', 'admin']), '123456'],
        ['ana',  fake.email(), random.choice(['normal', 'admin']), '123456'],
        ['pedro',  fake.email(), random.choice(['normal', 'admin']), '123456'],
        ['gonzalo',  fake.email(), random.choice(['normal', 'admin']),'123456'],
        ['administrator', fake.email(), 'admin', '123456']
    ]
    for array in arrays:
        data.append(array)       
    return data

def export_libro_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['titulo', 'autor', 'genero', 'year_publication'])
        writer.writerows(data)

def export_user_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'email', 'tipo_usuario', 'password'])
        writer.writerows(data)

def import_libro_to_postgres(filename):
    conn = psycopg2.connect("dbname='biblioteca_test' user='bibliotecaAdmin' host='localhost' password='a.123456'")
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            cur.execute(
                "INSERT INTO biblioteca_app_libro (titulo, autor, genero, year_publication) VALUES (%s, %s, %s, %s)",
                row
            )
    conn.commit()
    conn.close()
    os.remove(filename)

def import_user_to_postgres(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            Usuario.objects.create_user(username=row[0], email=row[1], tipo_usuario=row[2], password=row[3])
    os.remove(filename)
    

if __name__ == "__main__":
    dummy_data = create_libro_data(50)
    export_libro_to_csv(dummy_data, 'dummy_libros.csv')
    import_libro_to_postgres('dummy_libros.csv')
    dummy_data = create_user_data()
    export_user_to_csv(dummy_data, 'dummy_user.csv')
    import_user_to_postgres('dummy_user.csv')