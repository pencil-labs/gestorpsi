# -*- coding: utf-8 -*-
"""
    Original Author:    Simon Johnston
    Date:               2007-08-01
    Site:               http://www.ibm.com/developerworks/blogs/page/johnston?entry=cool_django
    Modified by:        Sergio Durand
    Date:               2008-07-29
"""
import uuid

from django.db.models.fields import CharField

class UuidField(CharField):
    """ A field which stores a UUID value, this may also have the Boolean
        attribute 'auto' which will set the value on initial save to a new
        UUID value (calculated using the UUID1 method). Note that while all
        UUIDs are expected to be unique we enforce this with a DB constraint.
    """
    def __init__(self, verbose_name=None, name=None, auto=True, **kwargs):
        self.auto = auto
        # Set this as a fixed value, we store UUIDs in text.
        kwargs['max_length'] = 36
        if auto:
            # Do not let the user edit UUIDs if they are auto-assigned.
            kwargs['editable'] = False
            kwargs['blank'] = True
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        """ see CharField.get_internal_type
            Need to override this, or the type mapping for table creation fails.
        """
        return CharField.__name__

    def pre_save(self, model_instance, add):
        """ see CharField.pre_save
            This is used to ensure that we auto-set values if required.
        """
        value = super(UuidField, self).pre_save(model_instance, add)
        if (not value) and self.auto:
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
        return value