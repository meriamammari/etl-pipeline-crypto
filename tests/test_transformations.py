import pytest
from unittest.mock import patch

@pytest.mark.parametrize("task_id, task_category, task_priority", [
    ("test_001", "testing", "high"),
    ("test_002", "testing", "high"),
    ("test_003", "testing", "medium"),
    ("test_004", "testing", "medium"),
])
def test_task_status(task_id: str, task_category: str, task_priority: str) -> None:
    expected_status = "completed"
    with patch('your_module.check_task_status') as mock_check:
        mock_check.return_value = expected_status
        status = mock_check(task_id)
        assert status == expected_status

def test_integration_data_flow() -> None:
    with patch('your_module.extract_data') as mock_extract, \
         patch('your_module.transform_data') as mock_transform, \
         patch('your_module.load_data') as mock_load:
        mock_extract.return_value = []
        mock_transform.return_value = []
        mock_load.return_value = True
        
        result = your_module.run_pipeline()
        
        mock_extract.assert_called_once()
        mock_transform.assert_called_once()
        mock_load.assert_called_once()
        assert result is True

def test_data_validation() -> None:
    sample_data = []
    with patch('your_module.validate_data') as mock_validate:
        mock_validate.return_value = True
        
        result = your_module.validate_data(sample_data)
        
        assert result is True
        mock_validate.assert_called_once_with(sample_data)

def test_load_performance() -> None:
    full_data_volume = [i for i in range(1000000)]
    with patch('your_module.load_data') as mock_load:
        mock_load.return_value = True
        
        result = your_module.load_data(full_data_volume)
        
        assert result is True
        mock_load.assert_called_once_with(full_data_volume)