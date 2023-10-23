import csv
from cats.models import Breed, Cat

def run():
    file_handle = open("cats/meow.csv")
    reader = csv.reader(file_handle)
    next(reader) # skip the column name

    # reset the cats database
    Cat.objects.all().delete()
    Breed.objects.all().delete()
    
    for row in reader:
        print(row)

        b, created = Breed.objects.get_or_create(breed_name=row[1])
        Cat.objects.create(cat_name=row[1], weight=float(row[2]), breed=b).save()