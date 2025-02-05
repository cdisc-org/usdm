from usdm_db.errors_and_logging.error import Error


def test_create():
    error = Error(message="XXXXX")
    assert error.message == "XXXXX"
    assert error.level == Error.ERROR


def test_create_level():
    error = Error(message="XXXXX", level=Error.WARNING)
    assert error.message == "XXXXX"
    assert error.level == Error.WARNING


def test_to_log():
    error = Error(message="Test message", level=Error.WARNING)
    assert (error.to_log()) == "Warning: Test message"


def test_to_dict():
    error = Error(message="Test message")
    assert (error.to_dict()) == {"level": "Error", "message": "Test message"}
