# voter_analytics/models.py
from django.db import models

# Create your models here.
class Voter(models.Model):
    ''' store/represent the data from one voter in newton, ma '''

    # personal information
    last_name = models.TextField()
    first_name = models.TextField()
    street_num = models.IntegerField()
    street_name = models.TextField()
    apt_num = models.TextField(blank=True)
    zip = models.TextField()
    dob = models.DateField()

    # voter information
    dor = models.DateField()
    party = models.TextField()
    p_num = models.TextField()

    # past elections
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()

    # voter score
    v_score = models.IntegerField(default=0)

    def __str__(self):
        ''' return a string representation of this model instance '''
        return f'{self.first_name} {self.last_name}'
    
def load_data():
    ''' load data records from a CSV file into model instances.'''

    # delete all records: clear out the database:
    Voter.objects.all().delete()
    
    # open the file for reading:
    filename = '/Users/kennajae/Desktop/cs412/django/static/files/newton_voters.csv'
    # on windows: '/C/Users/YOURNAME/Desktop/2023_chicago_results.csv'
    f = open(filename)
    headers = f.readline() # read/discard the headers
    # print(headers)

    # loop to read all the lines in the file
    for line in f:

        # provide protection around code that might generate an exception
        try:
            fields = line.split(',') # create a list of fields

            # create a new instance of Result object with this record from CSV
            voter = Voter(first_name=fields[2],
                            last_name=fields[1],
                            street_num = fields[3],
                            street_name = fields[4],
                            apt_num = fields[5],
                            zip = fields[6],
                            dob = fields[7],

                            dor = fields[8],
                            party = fields[9].strip(),
                            p_num = fields[10],
                        
                            v20state = fields[11],
                            v21town = fields[12],
                            v21primary = fields[13],
                            v22general = fields[14],
                            v23town = fields[15],

                            v_score = fields[16]
                        )
            voter.save() # save this instance to the database.
            print(f'Created result: {voter}')

        except:
            print(f"Exception on {fields}")