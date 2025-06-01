#!/usr/bin/env python3
"""
Example test file for Gemini Engineer

This file demonstrates various programming concepts and can be used
to test the AI assistant's ability to analyze and improve code.
"""

import math
import os
from typing import List, Optional

class Calculator:
    """A simple calculator class with basic operations."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        result = math.pow(base, exponent)
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def sqrt(self, number: float) -> float:
        """Calculate square root of a number."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number!")
        result = math.sqrt(number)
        self.history.append(f"√{number} = {result}")
        return result
    
    def get_history(self) -> List[str]:
        """Return calculation history."""
        return self.history.copy()
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    Note: This is a naive recursive implementation that could be optimized.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def factorial(n: int) -> int:
    """Calculate factorial of n."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers!")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def is_prime(number: int) -> bool:
    """Check if a number is prime."""
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def find_primes(limit: int) -> List[int]:
    """Find all prime numbers up to the given limit."""
    primes = []
    for num in range(2, limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def main():
    """Main function to demonstrate the calculator."""
    calc = Calculator()
    
    print("=== Calculator Demo ===")
    
    # Basic operations
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 * 7 = {calc.multiply(6, 7)}")
    print(f"15 / 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"√25 = {calc.sqrt(25)}")
    
    # Math functions
    print(f"\nFibonacci(10) = {fibonacci(10)}")
    print(f"Factorial(5) = {factorial(5)}")
    print(f"Is 17 prime? {is_prime(17)}")
    
    # Find primes up to 20
    primes = find_primes(20)
    print(f"Primes up to 20: {primes}")
    
    # Show calculation history
    print("\n=== Calculation History ===")
    for calculation in calc.get_history():
        print(calculation)

if __name__ == "__main__":
    main() 