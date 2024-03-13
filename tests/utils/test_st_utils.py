from unittest.mock import patch

import pytest
from utils.st_utils import dl_button_zip


def test_dl_button_zip():
    path_zip = "test.zip"
    with patch(
        "builtins.open", return_value=mock_open(read_data=b"test data")
    ) as mock_file:
        dl_button_zip(path_zip)
        mock_file.assert_called_once_with(path_zip, "rb")
        st.download_button.assert_called_once_with(
            label="Download results ZIP",
            data=mock_file.return_value.__enter__.return_value,
            file_name="results.zip",
            mime="application/zip",
        )

import pytest
from utils.st_utils import init_session_state

import pytest

def test_init_session_state():
    # Test case 1: dict_keys is empty
    dict_keys = {}
    init_session_state(dict_keys)
    assert st.session_state == {}

    # Test case 2: dict_keys contains keys that are already in st.session_state
    dict_keys = {'key1': 'value1', 'key2': 'value2'}
    st.session_state = {'key1': 'existing_value'}
    init_session_state(dict_keys)
    assert st.session_state == {'key1': 'existing_value', 'key2': 'value2'}

    # Test case 3: dict_keys contains keys that are not in st.session_state
    dict_keys = {'key1': 'value1', 'key2': 'value2'}
    st.session_state = {'key3': 'existing_value'}
    init_session_state(dict_keys)
    assert st.session_state == {'key3': 'existing_value', 'key1': 'value1', 'key2': 'value2'}

    # Test case 4: dict_keys contains keys with different data types
    dict_keys = {'key1': 1, 'key2': True, 'key3': 'value3'}
    st.session_state =
            