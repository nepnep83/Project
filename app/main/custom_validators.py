

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
