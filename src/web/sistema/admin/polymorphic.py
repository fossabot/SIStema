from polymorphic.admin import PolymorphicChildModelAdmin

from . import main

class SistemaPolymorphicChildModelAdmin(main.SistemaAdminMixin,
                                        PolymorphicChildModelAdmin):
    pass
