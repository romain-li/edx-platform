import logging

from openedx.core.lib.studio_entities import StudioEntity


logger = logging.getLogger(__name__)


class ProgramsEntity(StudioEntity):
    """Studio entity for administering Programs (e.g., XSeries)."""
    tab_text = 'Programs'
    button_text = 'New Program'
    list_view = None
    create_view = None

    @classmethod
    def is_enabled(cls, user=None):
        # TODO (RFL): Read a feature flag and verify the user has permission to administer Programs.
        return True
