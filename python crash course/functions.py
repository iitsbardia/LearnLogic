def add_numbers(a, b):
    return a + b


def greet(user_name):
    print(f"Hello, {user_name}! Welcome back!")


if __name__ == "__main__":
    greet("Bardi")  # Hello, Bardi! Welcome back!
    greet("Alice")  # Hello, Alice! Welcome back!

    result = add_numbers(5, 3)
    print(result)