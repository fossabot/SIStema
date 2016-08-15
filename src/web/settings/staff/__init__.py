import frontend.icons
import sistema.staff


@sistema.staff.register_staff_interface
class SettingsStaffInterface(sistema.staff.StaffInterface):
    def __init__(self, request):
        super().__init__(request)

    def get_sidebar_menu(self):
        return [sistema.staff.MenuItem( self.request,
                                        'Настройки',
                                        'school:school_settings_list',
                                        frontend.icons.GlyphIcon('cog'))]
