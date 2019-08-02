import logging
from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


class BasicDynamodbAdapter:
    def __init__(self, table_name, adapted_class, logger=None):
        """
        Adapter para persistencia de um entity
        :param table_name: Nome da tabela à ser usada
        """
        self._table_name = table_name
        self._class = adapted_class
        self._db = BasicDynamodbAdapter.get_db()
        self._table = self.get_table()
        self._logger = logger if logger else logging.getLogger(table_name)

        self._create_table_if_dont_exists()

    @property
    def logger(self):
        return self._logger

    def _do_table_exists(self):
        existing_tables = boto3.client('dynamodb').list_tables()
        return self._table_name in existing_tables['TableNames']

    def _create_table_if_dont_exists(self):
        if not self._do_table_exists():
            self.logger.info(f'Creating not existent table {self._table_name}')

            table = self._db.create_table(
                TableName=self._table_name,
                KeySchema=[
                    {
                        'AttributeName': 'entity_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'entity_id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(
                TableName=self._table_name)

    @staticmethod
    def get_db():
        return boto3.resource('dynamodb')

    def get_table(self):
        return self._db.Table(self._table_name)

    def list_all(self):
        response = self._table.scan()
        objects = [self._class.from_json(x) for x in response['Items']]
        for obj in objects:
            obj.set_adapter(self)
        return objects

    def get_by_id(self, item_id):
        response = self._table.get_item(Key=dict(entity_id=item_id),
                                        ConsistentRead=True)
        if 'Item' in response:
            return self._class.from_json(response['Item'])
        else:
            return None

    @staticmethod
    def _clean_set_empty_elements(arg):
        arg = set(x for x in arg if not hasattr(x, '__len__') or
                  len(x) > 0)
        return arg

    @staticmethod
    def _clean_list_empty_elements(arg):
        result = []
        for value in arg:
            clean_value = BasicDynamodbAdapter._remove_empties(value)
            if clean_value:
                result.append(clean_value)
        return result

    @staticmethod
    def _clean_dict_empty_elements(arg):
        result = {}
        for key, value in arg.items():
            clean_value = BasicDynamodbAdapter._remove_empties(value)
            if clean_value:
                result.update({key: clean_value})
        return result

    @staticmethod
    def _remove_empties(arg):
        if isinstance(arg, set):
            return BasicDynamodbAdapter._clean_set_empty_elements(arg)

        if isinstance(arg, list):
            return BasicDynamodbAdapter._clean_list_empty_elements(arg)

        if isinstance(arg, dict):
            return BasicDynamodbAdapter._clean_dict_empty_elements(arg)

        if not hasattr(arg, '__len__') or len(arg) != 0:
            return arg
        else:
            return None

    def save(self, json_data):
        entity_id = json_data.get('entity_id', str(uuid4()))
        json_data.update(dict(entity_id=entity_id))
        self.logger.info('Saving entity with data: {}'.format(json_data))
        clean_data = BasicDynamodbAdapter._remove_empties(json_data)
        self._table.put_item(Item=clean_data)
        return entity_id

    def delete(self, entity_id):
        try:
            self._table.delete_item(Key=dict(entity_id=entity_id),
                                    ReturnValues="ALL_OLD")
        except ClientError as e:
            self._logger.info('Erro deletando entrada.')
            self._logger.info(e.response['Error']['Message'])
            return None
        return entity_id

    def filter(self, **kwargs):
        """
        Filtra objetos de acordo com o critério especificado.
        Para especificar o critérios, que por default são concatenados
        com o operador lógico *ou*, use o nome do campo junto com o operador
        desejado concatenado com um "__" (duplo sublinha).
        Exemplo: Para filtrar todos os objetos em que o campo email seja
        igual à "nome@dom.com", o filtro deverá ser chamado assim:
            result = adapter.filter(email__eq="nome@dom.com")

        :raises ValueError(Comparador inválido): se o comparador especificado
            não for um dos seguintes:
               [begins_with, between, contains, eq, exists, gt, gte, is_in, lt,
                lte, ne, not_exists]

        :return: Lista de objetos
        """
        ops = ['begins_with',
               'between',
               'contains',
               'eq',
               'exists',
               'gt',
               'gte',
               'is_in',
               'lt',
               'lte',
               'ne',
               'not_exists']
        conditions = []
        for k, v in kwargs.items():
            field, op = k.split('__')
            if op not in ops:
                raise ValueError('Comparador inválido: {}'.format(op))

            conditions.append(getattr(Attr(field), op)(kwargs[k]))
        if not conditions:
            raise ValueError('Nenhuma condição no filtro.')

        filter_cond = conditions[0]

        for condition in conditions[1:]:
            filter_cond = filter_cond | condition

        result = self._table.scan(FilterExpression=filter_cond,
                                  Select='ALL_ATTRIBUTES')

        return [self._class.from_json(x) for x in result['Items']]

    class DynamodbAdapterScanException(BaseException):
        pass
