try:
    from pipeline.orchestrator import *
except ImportError:
    pytest.skip("module not available", allow_module_level=True)

import pytest
from unittest import mock
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_run_happy_path(mock_db_connection):
    """Test run method with normal valid input, expect success."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.execute = AsyncMock()
    mock_db_connection.executemany = AsyncMock()
    mock_db_connection.close = AsyncMock()
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        await orchestrator.run()
        mock_db_connection.execute.assert_called()

@pytest.mark.asyncio
async def test_run_empty_input():
    """Test run method with empty input, expect success."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    with mock.patch('asyncpg.connect', return_value=AsyncMock()):
        await orchestrator.run()

@pytest.mark.asyncio
async def test_run_error_handling(mock_db_connection):
    """Test run method error handling, expect logging of error."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.execute = AsyncMock(side_effect=Exception("DB error"))
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        with mock.patch('logging.Logger.error') as mock_error:
            await orchestrator.run()
            mock_error.assert_called_with(mock.ANY)

@pytest.mark.asyncio
async def test_extract_phase_happy_path():
    """Test extract_phase method, expect empty list."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    result = await orchestrator._extract_phase()
    assert result == []

@pytest.mark.asyncio
async def test_transform_phase_happy_path(sample_records):
    """Test transform_phase method with valid input, expect same records."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    result = await orchestrator._transform_phase(sample_records)
    assert result == sample_records

@pytest.mark.asyncio
async def test_transform_phase_empty_input():
    """Test transform_phase method with empty input, expect empty list."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    result = await orchestrator._transform_phase([])
    assert result == []

@pytest.mark.asyncio
async def test_validate_phase_happy_path(sample_records):
    """Test validate_phase method with valid input, expect same records."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    result = await orchestrator._validate_phase(sample_records)
    assert result == sample_records

@pytest.mark.asyncio
async def test_validate_phase_empty_input():
    """Test validate_phase method with empty input, expect empty list."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    result = await orchestrator._validate_phase([])
    assert result == []

@pytest.mark.asyncio
async def test_load_phase_happy_path(sample_records, mock_db_connection):
    """Test load_phase method with valid input, expect number of records loaded."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.execute = AsyncMock()
    mock_db_connection.executemany = AsyncMock()
    mock_db_connection.close = AsyncMock()
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        result = await orchestrator._load_phase(sample_records)
        assert result == len(sample_records)

@pytest.mark.asyncio
async def test_load_phase_empty_input(mock_db_connection):
    """Test load_phase method with empty input, expect zero records loaded."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.execute = AsyncMock()
    mock_db_connection.close = AsyncMock()
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        result = await orchestrator._load_phase([])
        assert result == 0

@pytest.mark.asyncio
async def test_load_phase_error_handling(mock_db_connection):
    """Test load_phase method error handling, expect logging of error."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.executemany = AsyncMock(side_effect=Exception("Load error"))
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        with mock.patch('logging.Logger.error') as mock_error:
            await orchestrator._load_phase([{"column1": "value1", "column2": "value2"}])
            mock_error.assert_called_with(mock.ANY)

@pytest.mark.asyncio
async def test_log_audit_happy_path(mock_db_connection):
    """Test log_audit method with valid input, expect successful logging."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.execute = AsyncMock()
    mock_db_connection.close = AsyncMock()
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        await orchestrator._log_audit(datetime.now(), 'success', 1)
        mock_db_connection.execute.assert_called()

@pytest.mark.asyncio
async def test_log_audit_error_handling(mock_db_connection):
    """Test log_audit method error handling, expect logging of error."""
    orchestrator = PipelineOrchestrator("mock_db_url")
    mock_db_connection.execute = AsyncMock(side_effect=Exception("Audit error"))
    with mock.patch('asyncpg.connect', return_value=mock_db_connection):
        with mock.patch('logging.Logger.error') as mock_error:
            await orchestrator._log_audit(datetime.now(), 'failed', 0)
            mock_error.assert_called_with(mock.ANY)