from usdm_db.errors_and_logging.errors_and_logging import ErrorsAndLogging
from usdm_db.errors_and_logging.errors import Errors
from usdm_db.errors_and_logging.error import Error

def test_create():
  error = ErrorsAndLogging()
  assert error._errors is not None
  assert error._logger is not None

def test_errors():
  error = ErrorsAndLogging()
  assert isinstance(error.errors(), Errors) 

def test_debug(caplog):
  error = ErrorsAndLogging()
  with caplog.at_level(Errors.DEBUG):
    error.debug("Debug message")
  assert caplog.records[-1].message == "Debug message"
  assert caplog.records[-1].levelname == "DEBUG"
  assert error.errors().count() == 0
  
def test_info(caplog):
  error = ErrorsAndLogging()
  with caplog.at_level(Errors.INFO):
    error.info("Debug message")
  assert caplog.records[-1].message == "Debug message"
  assert caplog.records[-1].levelname == "INFO"
  assert error.errors().count() == 0

def test_exception(caplog, mocker):
  mock_error = mocker.patch("usdm_db.errors_and_logging.errors.Errors.add")
  error = ErrorsAndLogging()
  e = Exception()
  with caplog.at_level(Errors.ERROR):
    error.exception("Debug message", e)
  assert caplog.records[-1].message == "Exception '' raised\n\nDebug message\n\nNoneType: None\n"
  assert caplog.records[-1].levelname == "ERROR"
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == 'Exception. Debug message. See log for additional details.'
  assert mock_error.call_args[0][1] == Errors.ERROR

def test_warning(caplog, mocker):
  mock_error = mocker.patch("usdm_db.errors_and_logging.errors.Errors.add")
  error = ErrorsAndLogging()
  with caplog.at_level(Errors.WARNING):
    error.warning("Debug message")
  assert caplog.records[-1].message == "Debug message"
  assert caplog.records[-1].levelname == "WARNING"
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == 'Debug message'
  assert mock_error.call_args[0][1] == Errors.WARNING

def test_error(caplog, mocker):
  mock_error = mocker.patch("usdm_db.errors_and_logging.errors.Errors.add")
  error = ErrorsAndLogging()
  with caplog.at_level(Errors.ERROR):
    error.error("Debug message")
  assert caplog.records[-1].message == "Debug message"
  assert caplog.records[-1].levelname == "ERROR"
  mock_error.assert_called()
  assert mock_error.call_args[0][0] == 'Debug message'
  assert mock_error.call_args[0][1] == Errors.ERROR
