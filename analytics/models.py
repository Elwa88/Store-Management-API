from django.db import models

class GeneralAnalytics(models.Model):

    TIME_PERIOD_CHOICES = [('monthly', "Monthly"),
                           ('quarterly', "Quartertly"),
                           'Yearly', "Yearly",]
    time_period = models.CharField(choices=TIME_PERIOD_CHOICES, max_length=10)
    start_date = models.DateField()


