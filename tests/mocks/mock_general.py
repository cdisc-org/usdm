def mock_called(mock, count=1):
  return mock.call_count == count

def mock_parameters_correct(mock, params):
  result = mock.assert_has_calls(params)
  print(f"RESULT: {result}")
  return result
