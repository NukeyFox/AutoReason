from autoreason.core import example  # Import the C++ extension module

def test_add_function():
    # Test the add function from the C++ extension module
    result = example.add(2, 3)
    print(f"Result of example.add(2, 3): {result}")
    assert result == 5, "The add function did not return the correct result."

if __name__ == "__main__":
    test_add_function()