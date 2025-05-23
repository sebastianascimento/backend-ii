import pytest
from season8.exercise.season.math_operations import multiply

def test_multiply_positive_numbers():
    """Test multiplication of positive numbers."""
    assert multiply(2, 3) == 6
    assert multiply(5, 7) == 35
    
def test_multiply_negative_numbers():
    """Test multiplication with negative numbers."""
    assert multiply(-2, 3) == -6
    assert multiply(-5, -5) == 25
    assert multiply(8, -4) == -32
    
def test_multiply_with_zero():
    """Test multiplication with zero."""
    assert multiply(0, 5) == 0
    assert multiply(10, 0) == 0
    assert multiply(0, 0) == 0
    
def test_multiply_decimal_numbers():
    """Test multiplication with decimal numbers."""
    assert multiply(2.5, 2) == 5.0
    assert multiply(0.1, 0.1) == pytest.approx(0.01)  

def test_multiply_large_numbers():
    """Test multiplication with large numbers."""
    assert multiply(1000000, 1000000) == 1000000000000