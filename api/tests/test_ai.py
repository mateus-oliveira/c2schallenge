import pytest

from unittest.mock import Mock, patch

from app.ai import llm_interpreter
from app.models.enums import Transmission, Fuel


@pytest.fixture
def mock_openai_response():
    mock_message = Mock()
    mock_message.content = '''{
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "engine": "2.0",
        "fuel": "FLEX",
        "color": "white",
        "mileage": 50000,
        "doors": 4,
        "transmission": "AUTOMATIC",
        "price": 90000.0
    }'''

    mock_choice = Mock()
    mock_choice.message = mock_message

    mock_response = Mock()
    mock_response.choices = [mock_choice]
    return mock_response


@pytest.mark.parametrize("input_sentence,expected_output", [
    (
        "I want a white Toyota Corolla 2020",
        {
            "brand": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "engine": "2.0",
            "fuel": Fuel.FLEX.value,
            "color": "white",
            "mileage": 50000,
            "doors": 4,
            "transmission": Transmission.AUTOMATIC.value,
            "price": 90000.0
        }
    ),
])
@patch('app.ai.OpenAI')
def test_llm_interpreter_successful(mock_openai, input_sentence, expected_output, mock_openai_response):
    """ Test the llm_interpreter function with a successful OpenAI API response. """
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai.return_value = mock_client

    result = llm_interpreter(input_sentence)
    assert result == expected_output

    # Verify OpenAI client was called with correct parameters
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args['model'] == "gpt-3.5-turbo"
    assert len(call_args['messages']) == 2
    assert call_args['response_format'] == {"type": "json_object"}


@patch('app.ai.OpenAI')
def test_llm_interpreter_api_error(mock_openai):
    """ Test the llm_interpreter function when OpenAI API returns an error. """
    mock_client = Mock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai.return_value = mock_client

    result = llm_interpreter("any sentence")
    assert result == {}


@pytest.mark.parametrize("input_json,expected_output", [
    (
        '''{
            "transmission": "INVALID",
            "fuel": "INVALID"
        }''',
        {
            "transmission": None,
            "fuel": None
        }
    ),
    (
        '''{
            "transmission": "AUTOMATIC",
            "fuel": "FLEX"
        }''',
        {
            "transmission": Transmission.AUTOMATIC.value,
            "fuel": Fuel.FLEX.value
        }
    ),
])
@patch('app.ai.OpenAI')
def test_llm_interpreter_enum_validation(mock_openai, input_json, expected_output, mock_openai_response):
    """ Test the llm_interpreter function with invalid enum values. """
    mock_client = Mock()
    mock_openai_response.choices[0].message.content = input_json
    mock_client.chat.completions.create.return_value = mock_openai_response
    mock_openai.return_value = mock_client

    result = llm_interpreter("any sentence")
    assert result["transmission"] == expected_output["transmission"]
    assert result["fuel"] == expected_output["fuel"]
