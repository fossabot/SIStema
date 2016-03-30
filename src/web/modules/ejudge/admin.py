from django.contrib import admin

from . import models

admin.site.register(models.ProgrammingLanguage)
admin.site.register(models.QueueElement)
admin.site.register(models.SolutionCheckingResult)
admin.site.register(models.Submission)
admin.site.register(models.TestCheckingResult)
