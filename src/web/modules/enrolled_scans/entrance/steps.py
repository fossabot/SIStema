from modules.entrance.models import steps
from .. import models


__all__ = ['EnrolledScansEntranceStep']


class EnrolledScansEntranceStep(
    steps.AbstractEntranceStep,
    steps.EntranceStepTextsMixIn
):
    template_file = 'enrolled_scans/scans.html'

    def is_passed(self, user):
        requirements = list(self.school.enrolled_scan_requirements.all())
        requirements = [r for r in requirements if r.is_needed_for_user(user)]

        scans_count = len(set(models.EnrolledScan.objects.filter(
            requirement__school=self.school,
            user=user
        ).values_list('requirement_id', flat=True)))

        # Return True iff user uploads scan for each requirement
        return scans_count >= len(requirements)

    def __str__(self):
        return 'Шаг отправки сканов для %s' % self.school
