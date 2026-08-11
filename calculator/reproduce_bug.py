from pkg.calculator import Calculator

def test_calculator():
    calc = Calculator()
    result = calc.evaluate("2 + 2 * 2")
    print(f"Result: {result}")
    assert result == 6, f"Expected 6, but got {result}"

if __name__ == "__main__":
    test_calculator()
