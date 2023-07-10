from wtforms.validators import StopValidation


class ConditionalValidation:
    """
    Conditional Validation of elements

    :param other_field_name:
        The field which the validation is dependent on.
    :param other_field_value:
        The value that is required to validate.
    :param validators:
        A list of validators.
    """
    def __init__(self, other_field_name, other_field_value, validators):
        self.other_field_name = other_field_name
        self.other_field_value = other_field_value
        self.validations = validators

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)

        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)

        if other_field.data == self.other_field_value:
            for validation in self.validations:
                validation.__call__(form, field)


class OneInputRequired:
    def __init__(self, other_required_fields, form_name, message=None):
        self.other_required_fields = other_required_fields
        self.required_input_name = form_name
        self.message = message

    def __call__(self, form, field):
        if field.raw_data and field.raw_data[0]:
            return

        for other_field_name in self.other_required_fields:
            other_field = form._fields.get(other_field_name)

            if other_field is None:
                raise Exception('no field named "%s" in form' % other_field_name)

            if other_field.raw_data and other_field.raw_data[0]:
                return

        if self.message is None:
            message = field.gettext("At least one %s is required." % self.required_input_name)
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)