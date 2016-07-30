from django.db import models
import polymorphic.models

import schools.models


class AbstractHomePageBlock(polymorphic.models.PolymorphicModel):
    school = models.ForeignKey(schools.models.School, related_name='home_page_blocks')

    order = models.PositiveIntegerField(help_text='Блоки показываются в порядке возрастания этого параметра')

    def build(self, request):
        raise NotImplementedError()
