from faker import Faker

faker = Faker()

def random_email():
    return faker.unique.email()

def random_email_with_spaces():
    return f"  {faker.unique.email()}  "

def random_password(min_length=5, max_length=20):
    length = faker.random_int(min=min_length, max=max_length)
    return faker.password(length=length)

def random_age(min_age=0, max_age=99):
    return faker.random_int(min=min_age, max=max_age)

def random_name():
    return faker.first_name()



def invalid_email_no_at():
    return "userexample.com"

def invalid_email_no_dot():
    return "user@examplecom"

def invalid_email_too_long():
    return "a" * 51 + "@example.com"

def invalid_email_too_short():
    return "a@example.com"[:1]

def too_short_password():
    return faker.password(length=4)

def too_long_password():
    return faker.password(length=21)

def float_age():
    return 10.5

def negative_age():
    return -1

def too_big_age():
    return 100

def age_with_letters():
    return "abc"

def age_with_symbols():
    return "@$#"

def age_with_dot():
    return "10.5"

def invalid_utf8_name():
    return "\x00\x01\x02"

def empty_string():
    return ""

def name_with_whitespace():
    return "   "
