

# Testing

```bash
# activate virtual environment
source htpc/.venv/bin/activate

# Run all tests using discover
python -m unittest discover

# Run specific test
python -m unittest test.test_lambda_function.FunctionTest
python -m unittest test.test_lambda_function.FunctionTest.test_failed_send_to_slack
```