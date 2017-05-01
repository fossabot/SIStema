import frontend.icons
import sistema.staff
from . import views
import groups.api


@sistema.staff.register_staff_interface
class EntranceStaffInterface(sistema.staff.StaffInterface):
    def __init__(self, request):
        super().__init__(request)
        self._filled_an_application_count = len(
            views.get_enrolling_users_ids(request.school)
        )

        self.is_entrance_admin = groups.api.is_user_in_group(
            request.user,
            request.school,
            'entrance__admins'
        )
        self.can_check = groups.api.is_user_in_group(
            request.user,
            request.school,
            'entrance__can_check'
        )

    def get_sidebar_menu(self):
        filled_an_application = sistema.staff.MenuItem(
            self.request,
            'Подавшие заявку',
            'school:entrance:enrolling',
            frontend.icons.FaIcon('envelope-o'),
            label=sistema.staff.MenuItemLabel(self._filled_an_application_count, 'system')
        )

        exam_tasks = sistema.staff.MenuItem(
            self.request,
            'Задания',
            '',
            frontend.icons.GlyphIcon('book')
        )

        exam_checking = sistema.staff.MenuItem(
            self.request,
            'Проверка',
            'school:entrance:check',
            frontend.icons.FaIcon('desktop')
        )

        exam_results = sistema.staff.MenuItem(
            self.request,
            'Результаты',
            'school:entrance:results',
            frontend.icons.GlyphIcon('equalizer')
        )

        ejudge_stats = sistema.staff.MenuItem(
            self.request,
            'Статистика по практике',
            'school:ejudge:show_ejudge_stats',
            frontend.icons.GlyphIcon('equalizer')
        )

        exam = sistema.staff.MenuItem(
            self.request,
            'Вступительная',
            '',
            frontend.icons.FaIcon('columns'),
            child=[exam_tasks, exam_checking, ejudge_stats, exam_results]
        )

        items = []
        if self.is_entrance_admin:
            items.append(filled_an_application)
        if self.can_check:
            items.append(exam)

        return items
