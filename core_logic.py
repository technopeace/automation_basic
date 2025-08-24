# core_logic.py

def process_user_data(name, age):
    """
    Takes user's name and age, validates them, and returns a formatted
    success message string. This function contains the core business logic
    and knows nothing about web servers or desktop GUIs.
    """
    if name and age:
        # In a real application, you might save this to a database here.
        # For our test, we just format the success message.
        return f"Saved!\nName: {name}\nAge: {age}"
    else:
        # Return None or raise an error for invalid input.
        return None
