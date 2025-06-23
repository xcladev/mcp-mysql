import pytest
from unittest.mock import patch, MagicMock
from tools import (
    list_tables,
    describe_table,
    get_foreign_keys,
    get_column_names,
    list_app_users,
    get_app_user,
)

def mock_connection(cursor_result):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = cursor_result
    mock_cursor.fetchone.return_value = cursor_result[0] if cursor_result else None
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn, mock_cursor

@patch('tools.get_db_connection')
def test_list_tables(mock_get_db_conn):
    mock_conn, mock_cursor = mock_connection([('users',), ('orders',)])
    mock_get_db_conn.return_value.__enter__.return_value = mock_conn
    result = list_tables()
    assert result == ['users', 'orders']
    mock_cursor.execute.assert_called_with('SHOW TABLES')

@patch('tools.get_db_connection')
def test_describe_table(mock_get_db_conn):
    columns = [
        ('id', 'int', 'NO', 'PRI', None, ''),
        ('name', 'varchar(255)', 'YES', '', None, ''),
    ]
    mock_conn, mock_cursor = mock_connection(columns)
    mock_get_db_conn.return_value.__enter__.return_value = mock_conn
    result = describe_table('users')
    assert result == [
        {'Field': 'id', 'Type': 'int', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': ''},
        {'Field': 'name', 'Type': 'varchar(255)', 'Null': 'YES', 'Key': '', 'Default': None, 'Extra': ''},
    ]
    mock_cursor.execute.assert_called_with('SHOW COLUMNS FROM `users`')

@patch('tools.get_db_connection')
def test_get_foreign_keys(mock_get_db_conn):
    fks = [
        ('user_id', 'users', 'id'),
        ('order_id', 'orders', 'id'),
    ]
    mock_conn, mock_cursor = mock_connection(fks)
    mock_get_db_conn.return_value.__enter__.return_value = mock_conn
    result = get_foreign_keys('orders')
    assert result == [
        {'column': 'user_id', 'referenced_table': 'users', 'referenced_column': 'id'},
        {'column': 'order_id', 'referenced_table': 'orders', 'referenced_column': 'id'},
    ]
    assert mock_cursor.execute.call_args[0][0].startswith('SELECT COLUMN_NAME')

@patch('tools.get_db_connection')
def test_get_column_names(mock_get_db_conn):
    columns = [
        ('id', 'int', 'NO', 'PRI', None, ''),
        ('name', 'varchar(255)', 'YES', '', None, ''),
    ]
    mock_conn, mock_cursor = mock_connection(columns)
    mock_get_db_conn.return_value.__enter__.return_value = mock_conn
    result = get_column_names('users')
    assert result == ['id', 'name']
    mock_cursor.execute.assert_called_with('SHOW COLUMNS FROM `users`')

@patch('tools.get_db_connection')
def test_list_app_users(mock_get_db_conn):
    columns = [('id',), ('name',), ('password',)]
    users = [(1, 'Alice'), (2, 'Bob')]
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = [columns, users]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_conn.return_value.__enter__.return_value = mock_conn
    result = list_app_users('users')
    assert result == [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'},
    ]
    assert mock_cursor.execute.call_args_list[0][0][0] == 'SHOW COLUMNS FROM `users`'

@patch('tools.get_db_connection')
def test_get_app_user(mock_get_db_conn):
    columns = [('id',), ('name',), ('password',)]
    user = (1, 'Alice')
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = columns
    mock_cursor.fetchone.return_value = user
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_conn.return_value.__enter__.return_value = mock_conn
    result = get_app_user('users', 'id', 1)
    assert result == {'id': 1, 'name': 'Alice'}
    assert mock_cursor.execute.call_args_list[0][0][0] == 'SHOW COLUMNS FROM `users`'
    assert mock_cursor.execute.call_args_list[1][0][0].startswith('SELECT id, name FROM `users` WHERE `id` = %s') 