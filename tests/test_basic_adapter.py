#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch, MagicMock

# noinspection PyPackageRequirements
import pytest
from pytest import raises

from playerstars_adapters.basic_adapter import BasicDynamodbAdapter
from tests.basic_adapter_utils import (
    make_mock_client, Adapter, Entity, make_mock_table, raise_if_empty,
    Patches)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource', return_value='ok')  # _db
@patch(Patches.GET_TABLE, return_value=MagicMock)  # _table
@patch.object(Adapter, '_create_table_if_dont_exists')
def test_get_db(mock, mgt, mocked_resource):
    adapter = Adapter('tbl_adapter')
    db = adapter.get_db()
    assert db == 'ok'


# noinspection PyProtectedMember,PyUnusedLocal
@patch('boto3.resource', return_value='ok')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
@patch.object(Adapter, '_create_table_if_dont_exists')
def test_do_table_exists(mock0, mock1, mock2, moack3):
    adapter = Adapter('tbl1')
    assert adapter._do_table_exists()


# noinspection PyProtectedMember,PyUnusedLocal
@patch('boto3.resource', return_value='ok')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
@patch.object(Adapter, '_create_table_if_dont_exists')
def test_do_table_not_exists(mock0, mock1, mock2, mock3):
    adapter = Adapter('tblX')

    assert not adapter._do_table_exists()


# noinspection PyProtectedMember,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_create_table_if_not_exists(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    assert not adapter._do_table_exists()
    adapter._create_table_if_dont_exists()


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_list_all(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    result = adapter.list_all()

    assert isinstance(result[0], Entity)
    assert isinstance(result[1], Entity)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_delete(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    result = adapter.delete('id1')

    assert result == 'id1'


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_delete_raises(mock1, mock2, mock3):
    adapter = Adapter('tbl3')
    result = adapter.delete('id1')
    assert result is None


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_get_by_id(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    result = adapter.get_by_id('id1')

    assert isinstance(result, Entity)
    assert result.nome == 'nome1'


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_get_by_id_not_found(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    result = adapter.get_by_id('id2')

    assert result is None


# noinspection PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_save(mock1, mock2, mock3):
    adapter = Adapter('tbl3')
    entity = Entity('id1', 'nome1')
    entity.set_adapter(adapter)
    saved_id = entity.save()

    assert saved_id == 'id1'
    mock2.return_value.put_item.assert_called_once()

    expected = entity.to_json()
    mock2.return_value.put_item.assert_called_with(Item=expected)


# noinspection PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_filter(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    adapter.filter(id__eq='id1', nome__eq='eu mesmo')

    assert mock2.filter.called_once()


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_filter_invalid_operator(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    with pytest.raises(ValueError) as excinfo:
        adapter.filter(id__invalid='id1')

    assert 'Comparador inválido' in str(excinfo.value)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_filter_no_conditions(mock1, mock2, mock3):
    adapter = Adapter('tbl3')

    with pytest.raises(ValueError) as excinfo:
        adapter.filter()

    assert str(excinfo.value) == 'Nenhuma condição no filtro.'


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_get_table(mock1, mock2):
    adapter = Adapter('tbl3')
    assert adapter.get_table()


# noinspection PyProtectedMember
def test_remove_empties_set():
    arg = {1, 2, 3, ''}
    result = BasicDynamodbAdapter._remove_empties(arg)

    assert result == {1, 2, 3}


# noinspection PyProtectedMember
def test_remove_empties_list():
    arg = [1, 2, 3, '', dict(), []]
    result = BasicDynamodbAdapter._remove_empties(arg)

    assert result == [1, 2, 3]


# noinspection PyProtectedMember
def test_remove_empties_complexo():
    arg = dict(k1='fica', k2=dict(sk1='fica2', sk2=['', ''], sk3={1, 2, ''}))
    result = BasicDynamodbAdapter._remove_empties(arg)

    assert result == dict(k1='fica', k2=dict(sk1='fica2', sk3={1, 2}))


def test_raise_if_empty_raises():
    arg = [1, 2, '']

    with raises(ValueError) as excinfo:
        raise_if_empty(arg)

    assert 'Item vazio encontrado' in str(excinfo.value)


def test_raise_if_empty_raises_with_dict():
    arg = [1, 2, dict(a=1, b='')]

    with raises(ValueError) as excinfo:
        raise_if_empty(arg)

    assert 'Item vazio encontrado' in str(excinfo.value)
