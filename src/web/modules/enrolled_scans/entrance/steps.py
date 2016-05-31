import operator

from django.template.context import Context

from modules.entrance import steps
from sistema.helpers import group_by
from .. import models


class EnrolledScansEntranceStep(steps.EntranceStep):
    def is_passed(self, user):
        requirements = list(models.EnrolledScanRequirement.objects.filter(for_school=self.school))
        # TODO: refactor: extract follow line to models.EnrolledScanRequirement
        requirements = list(filter(lambda r: r.is_needed_for_user(user), requirements))

        scans = group_by(
            models.EnrolledScan.objects.filter(requirement__for_school=self.school, for_user=user),
            operator.attrgetter('requirement_id')
        )

        # Return True iff user uploads scan for each requirement
        return len(scans) >= len(requirements)

    def render(self, user):
        if not self.is_available(user):
            template = self._template_factory('''
            <p>
                Отправка сканов будет доступна после заполнения раздела «{{ previous.title }}».
            </p>
            ''')
            body = template.render(Context({
                'previous': self.previous_questionnaire,
            }))
            return self.panel('Сканы документов', body, 'default')

        if self.is_passed(user):
            template = self._template_factory('''
            <p>
                Сканы загружены. Вы можете изменить что-нибудь, если хотите.
            </p>
            <div>
                <a class="btn btn-success" href="{% url 'school:entrance:enrolled_scans:scans' school.short_name %}">Править</a>
            </div>
            ''')
            body = template.render(Context({
                'school': self.school,
            }))

            return self.panel('Сканы документов', body, 'success')

        template = self._template_factory('''
        <p>
            Загрузите отсканированные документы: паспорт и медицинский полис.
            <b>Если поездку в ЛКШ оплачивает организация, загрузите скан квитанции об оплате.</b>
        </p>
        <div>
            <a class="btn btn-alert" href="{% url 'school:entrance:enrolled_scans:scans' school.short_name %}">Загрузить</a>
        </div>
        ''')
        body = template.render(Context({
            'user': user,
            'school': self.school,
        }))
        return self.panel('Сканы документов', body, 'alert')
