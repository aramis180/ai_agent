from collections.abc import Callable

class Calculator:
    def __init__(self) -> None:
        self.operators: dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence: dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> float | None:
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: list[str]) -> float:
        values: list[float] = []
        operators: list[str] = []

        for token in tokens:
            if token in self.operators:
                while (operators and operators[-1] in self.operators and self.precedence[operators[-1]] >= self.precedence[token]):
                    b = values.pop()
                    a = values.pop()
                    op = operators.pop()
                    values.append(self.operators[op](a, b))
                operators.append(token)
            else:
                values.append(float(token))

        while operators:
            b = values.pop()
            a = values.pop()
            op = operators.pop()
            values.append(self.operators[op](a, b))

        return values[0] if values else None

if __name__ == "__main__":
    # Keep this for testing
    pass
