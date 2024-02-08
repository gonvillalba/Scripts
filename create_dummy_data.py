import csv
import random
from faker import Faker
import psycopg2

fake = Faker()

def create_dummy_data(num_records):
    data = []
    for _ in range(num_records):
        titulo = fake.sentence(nb_words=3)
        autor = fake.name()
        genero = random.choice(['Fiction', 'Non-Fiction', 'Sci-Fi', 'Mystery', 'Thriller', 'Romance'])
        year_publication = fake.date_time_this_decade().strftime('%Y-%m-%d')
        data.append([titulo, autor, genero, year_publication])
    return data

def export_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['titulo', 'autor', 'genero', 'year_publication'])
        writer.writerows(data)

def import_to_postgres(filename):
    conn = psycopg2.connect("dbname='biblioteca' user='bibliotecaAdmin' host='localhost' password='a.123456'")
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

if __name__ == "__main__":
    dummy_data = create_dummy_data(100)
    export_to_csv(dummy_data, 'dummy_libros.csv')
    import_to_postgres('dummy_libros.csv')