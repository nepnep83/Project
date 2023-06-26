# from behave import *
#
# from PersonBuilder import PersonBuilder
#
#
# @given('a person')
# def step_impl(context):
#     context.personBuilder = PersonBuilder()
#
#
# @given('their name is Aidan Smith')
# def step_impl(context):
#     context.personBuilder.set_given_name("Aidan")
#     context.personBuilder.set_family_name("Smith")
#
#
# @given('they are 25')
# def step_impl(context):
#     context.personBuilder.set_age(25)
#     context.person1 = context.personBuilder.build()
#
#
# @then('a person called Aidan Smith exists')
# def step_impl(context):
#     assert context.person1.given_name is "Aidan"
#     assert context.person1.family_name is "Smith"
#
#
# @then('their age is {age}')
# def step_impl(context, age):
#     assert context.person1.age is int(age)
#
#
# @when('they change their name to Tom Powell')
# def step_impl(context):
#     context.person1.change_given_name('Tom')
#     context.person1.change_family_name('Powell')
#
#
# @when('their age to {age}')
# def step_impl(context, age):
#     context.person1.change_age(int(age))
#
#
# @then('a person called Tom Powell exists')
# def step_impl(context):
#     assert context.person1.given_name is 'Tom'
#     assert context.person1.family_name is 'Powell'
