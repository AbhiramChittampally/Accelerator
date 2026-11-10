import pytest

# from calculator import add, divide


# def test_add():
#     result = add(2, 3)
#     assert result == 5


# def test_divide():
#     result = divide(10, 2)
#     assert result == 5


# def test_divide_by_zero():
#     with pytest.raises(ValueError, match="Cannot divide by zero"):
#         divide(10, 0)





# import pytest

# from calculator import add, divide


# @pytest.fixture
# def sample_numbers():
#     return (10, 2)


# def test_add():
#     assert add(2, 3) == 5


# def test_divide(sample_numbers):
#     a, b = sample_numbers
#     assert divide(a, b) == 5





# @pytest.fixture(scope="module")
# def reference_data():
#     return {"tax_rate": 0.18}



# import pytest


# @pytest.fixture
# def sample_file(tmp_path):
#     file_path = tmp_path / "example.txt"
#     file_path.write_text("Hello, pytest!", encoding="utf-8")

#     yield file_path

#     # Teardown: runs after the test finishes
#     # Add cleanup here if a resource needs explicit cleanup.








import pytest

from calculator import add, divide


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-2, 3, 1),
        (-2, -3, -5),
        (1.5, 2.5, 4.0),
    ],
)
def test_add_multiple_inputs(a, b, expected):
    assert add(a, b) == expected
    
    
    
    
    
    
    
    
import pytest


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    assert False
    
    
    
    
    
    
    
import pytest


@pytest.mark.xfail(reason="Known issue: negative inputs are unsupported")
def test_known_issue():
    assert add(-2, 3) == 100








@pytest.mark.integration
def test_database_integration():
    # Replace this placeholder with a real integration test.
    assert True