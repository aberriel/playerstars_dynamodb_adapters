from unittest.mock import patch, MagicMock

# noinspection PyPackageRequirements
import pytest

from tests.basic_adapter_utils import (
    make_mock_client, Adapter, Entity, make_mock_table,
    make_mock_table_with_update_error)


class Patches:
    BASE = 'playerstars_adapters.basic_adapter'
    BOTO3_CLIENT = f'{BASE}.boto3.client'
    GET_TABLE = f'{BASE}.BasicDynamodbAdapter.get_table'


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
def test_update(mock1, mock2, mock3):
    adapter = Adapter('tbl3')
    entity = Entity('id1', 'nome1')
    entity.set_adapter(adapter)
    saved_id = entity.save()

    assert saved_id == 'id1'
    mock2.return_value.put_item.assert_called_once()

    expected = entity.to_json()
    mock2.return_value.put_item.assert_called_with(Item=expected)
    entity = Entity('id1', 'nome4')
    entity.set_adapter(adapter)
    updated_entity = entity.update()
    new_saved_id = updated_entity.entity_id
    mock2.return_value.update_item.assert_called_with(
        ExpressionAttributeValues={':value0': {str: 'nome4'}},
        Key={'entity_id': new_saved_id},
        UpdateExpression='SET nome = :value0')
    assert updated_entity.nome == 'nome4'


# noinspection PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table_with_update_error())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_update_error(mock1, mock2, mock3):
    adapter = Adapter('tbl3')
    entity_one = Entity('id1', 'nome1')
    entity_one.set_adapter(adapter)
    saved_id = entity_one.save()

    assert saved_id == 'id1'
    mock2.return_value.put_item.assert_called_once()

    expected = entity_one.to_json()
    mock2.return_value.put_item.assert_called_with(Item=expected)
    entity_two = Entity('id4', 'nome4')
    entity_two.set_adapter(adapter)
    assert entity_two.update() is None


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
