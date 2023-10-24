import csv
from django.utils import timezone
from polls.models import Question, Choice

def run():
    print("=== Polls Loader")

    Choice.objects.all().delete()
    Question.objects.all().delete()
    print("=== Objects deleted")

    fhand = open('polls/dj4e_batch.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    for row in reader:
        print(row)
        
        q = Question(question_text=row[0], pub_date=timezone.now())
        q.save()
        
        c = q.choice_set

        for choice_text in row[1:]:
            c.create(choice_text=choice_text)

    print("=== Load Complete")