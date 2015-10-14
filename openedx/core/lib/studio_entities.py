"""Studio entity plugin manager and API."""
import abc

from openedx.core.lib.api.plugins import PluginError, PluginManager


class StudioEntityPluginManager(PluginManager):
    """Manager for all available Studio entities.

    Examples of Studio entities include Courses, Libraries, and Programs. All Studio
    entities should implement `StudioEntity`.
    """
    NAMESPACE = 'openedx.studio_entity'


# TODO (RFL): Where's the right place for this?
class StudioEntity(object):
    """Abstract class used to represent Studio entities.

    Examples of Studio entities include Courses, Libraries, and Programs.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def tab_text(self):
        """Text to display in a tab used to navigate to a list of instances of this entity.

        Should be internationalized using `ugettext_noop` since the user won't be available in this context.
        """
        pass

    @abc.abstractproperty
    def button_text(self):
        """Text to display in a button used to create a new instance of this entity.

        Should be internationalized using `ugettext_noop` since the user won't be available in this context.
        """
        pass

    # TODO (RFL): Should this be a template or a view?
    @abc.abstractproperty
    def list_view(self):
        """Name of the view used to render a list of instances of this entity."""
        pass

    # TODO (RFL): Should this be a template or a view?
    @abc.abstractproperty
    def create_view(self):
        """Name of the view used to create a new instance of this entity."""
        pass

    @abc.abstractmethod
    def is_enabled(cls, user=None):  # pylint: disable=unused-argument
        """Indicates whether this entity should be enabled.

        This is a class method; override with @classmethod.

        Keyword Arguments:
            user (User): The user signed in to Studio.
        """
        pass
