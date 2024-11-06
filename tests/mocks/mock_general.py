def mock_called(mock, count=1):
  return mock.call_count == count

def mock_parameters_correct(mock, params):
  return mock.assert_has_calls(params)
