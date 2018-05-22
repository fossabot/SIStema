import frontend.icons
import sistema.staff


@sistema.staff.register_staff_interface
class GroupsStaffInterface(sistema.staff.StaffInterface):
    def get_sidebar_menu(self):
        return [
            sistema.staff.MenuItem(
                self.request,
                'Группы',
                'school:groups:list',
                frontend.icons.FaIcon('group')
            )
        ]
