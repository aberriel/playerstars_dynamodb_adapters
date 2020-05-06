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
    adapter = Adapter('tbl_adapter', 'localhost-db')
    db = adapter.get_db()
    assert db == 'ok'


# noinspection PyProtectedMember,PyUnusedLocal
@patch('boto3.resource', return_value='ok')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
@patch.object(Adapter, '_create_table_if_dont_exists')
def test_do_table_exists(mock0, mock1, mock2, moack3):
    adapter = Adapter('tbl1', 'localhost-db')
    assert adapter._do_table_exists()


# noinspection PyProtectedMember,PyUnusedLocal
@patch('boto3.resource', return_value='ok')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
@patch.object(Adapter, '_create_table_if_dont_exists')
def test_do_table_not_exists(mock0, mock1, mock2, mock3):
    adapter = Adapter('tblX', 'localhost-db')

    assert not adapter._do_table_exists()


# noinspection PyProtectedMember,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_create_table_if_not_exists(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')

    assert not adapter._do_table_exists()
    adapter._create_table_if_dont_exists()


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_list_all(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')

    result = adapter.list_all()

    assert isinstance(result[0], Entity)
    assert isinstance(result[1], Entity)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE)
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_delete(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')

    result = adapter.delete('id1')

    assert result == 'id1'


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_delete_raises(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')
    result = adapter.delete('id1')
    assert result is None


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_get_by_id(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')

    result = adapter.get_by_id('id1')

    assert isinstance(result, Entity)
    assert result.nome == 'nome1'


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_get_by_id_not_found(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')

    result = adapter.get_by_id('id2')

    assert result is None


# noinspection PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.GET_TABLE, return_value=make_mock_table())
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_save(mock1, mock2, mock3):
    adapter = Adapter('tbl3', 'localhost-db')
    entity = Entity('id1', 'nome1')
    entity.set_adapter(adapter)
    saved_id = entity.save()

    assert saved_id == 'id1'
    mock2.return_value.put_item.assert_called_once()

    expected = entity.to_json()
    mock2.return_value.put_item.assert_called_with(Item=expected)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
@patch('boto3.resource')
@patch(Patches.BOTO3_CLIENT, return_value=make_mock_client())
def test_get_table(mock1, mock2):
    adapter = Adapter('tbl3', 'localhost-db')
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


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_filter(mock_boto):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())

    with patch.object(adapter, '_table') as mock:
        adapter.filter(campo__eq=42, campo2__gt=42)

    mock.scan.assert_called_once()


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_filter_between(mock_boto):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())

    with patch.object(adapter, '_table') as mock:
        adapter.filter(campo__between=[40, 50])

    mock.scan.assert_called_once()


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_filter_exists(mock_boto):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())

    with patch.object(adapter, '_table') as mock:
        adapter.filter(campo__exists=None)

    mock.scan.assert_called_once()


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_filter_projection(mock_boto):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())

    with patch.object(adapter, '_table') as mock:
        adapter.filter(campo__exists=None, ProjectionExpression='campo')

    mock.scan.assert_called_once()


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_filter_invalid_op(mock_boto):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())

    with patch.object(adapter, '_table'):
        with raises(ValueError) as excinfo:
            adapter.filter(campo__oops=42)

    assert 'Comparador inválido: oops' == str(excinfo.value)


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_filter_no_conditions(mock_boto):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())

    with patch.object(adapter, '_table'):
        with raises(ValueError) as excinfo:
            adapter.filter()

    assert 'Nenhuma condição no filtro.' == str(excinfo.value)


# noinspection PyUnusedLocal
@patch('playerstars_adapters.basic_adapter.boto3')
def test_desserialize(mock_boto3):
    adapter = BasicDynamodbAdapter('tabela', None, MagicMock(), MagicMock())
    mock_class = MagicMock(
        from_json=MagicMock())
    mock_table = MagicMock(
        scan=MagicMock(
            return_value=dict(Items=[1, 2, 3, 4, 5])))
    with patch.multiple(adapter,
                        _class=mock_class,
                        _table=mock_table):
        result = adapter.filter(field__eq=1)

    for r in result:
        r.set_adapter.assert_called()
