from collections import namedtuple
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

import pytest
from playerstars_domain.utils.datetime_helper import aware_utc
from pytest import raises, fixture
from clapy_basic_classes.basic_scheduler_adapter.basic_scheduler_adapter import \
    TaskNotFoundException
from playerstars_adapters import AwsTaskSchedulerAdapter


def test_get_task_id():
    assert AwsTaskSchedulerAdapter.get_task_id_name() == 'task_id'


@fixture(scope='class')
def atsa_factory(request):
    Atsa = namedtuple('Atsa', 'atsa, mock_name, mock_ident, mock_exec_time, '
                              'mock_runner')

    def factory(name=MagicMock(),
                identifier=MagicMock(),
                exec_time=MagicMock(),
                runner=MagicMock()):
        atsa = AwsTaskSchedulerAdapter(
            name=name,
            task_id=identifier,
            execution_time=exec_time,
            lambda_runner=runner)
        return Atsa(atsa, name, identifier, exec_time, runner)

    request.cls.atsa_factory = factory


prefix = 'chalicelib.era_labs'


@pytest.mark.usefixtures('atsa_factory')
class TestAtsa(TestCase):
    def setUp(self):
        self.boto_patcher = patch(f'{prefix}.boto3')
        self.mock_boto = self.boto_patcher.start()

    def tearDown(self):
        self.boto_patcher.stop()

    @patch.object(AwsTaskSchedulerAdapter, '_set')
    def test_set(self, mock_set):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_task_id = MagicMock()
        mock_exec_time = MagicMock()
        atsa.set(mock_task_id, mock_exec_time)

        mock_set.assert_called_once()

    @patch.object(AwsTaskSchedulerAdapter, '_delete')
    @patch.object(AwsTaskSchedulerAdapter, '_set')
    def test_update(self, mock_set, mock_delete):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_task_id = MagicMock()
        mock_exec_time = MagicMock()
        atsa.update(mock_task_id, mock_exec_time)

        mock_delete.assert_called_once()
        mock_set.assert_called_once()

    @patch.object(AwsTaskSchedulerAdapter, '_delete')
    def test_delete(self, mock_delete):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.delete()
        mock_delete.assert_called_once()

    def test_datetime_from_cron_expression(self):
        cron_expression = 'cron(45 9 16 8 ? 2020)'
        result = AwsTaskSchedulerAdapter._datetime_from_cron_expression(
            cron_expression)

        expected = aware_utc(datetime(2020, 8, 16, 9, 45, 0))
        self.assertEqual(result, expected)

    def test_get_target(self):
        mock_ev = MagicMock()
        mock_name = MagicMock()
        result = AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        mock_ev.list_targets_by_rule.assert_called_with(Rule=mock_name)

        mock_list_result = mock_ev.list_targets_by_rule()
        mock_list_result.__getitem__.assert_called_with('Targets')

        mock_targets = mock_list_result.__getitem__()
        mock_targets.__getitem__.assert_called_with(0)

        self.assertEqual(result, mock_targets.__getitem__())

    def test_get_target_key_not_found(self):
        mock_ev = MagicMock(list_targets_by_rule=MagicMock(return_value={}))
        mock_name = MagicMock()

        with raises(TaskNotFoundException) as excinfo:
            AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        self.assertEqual(str(excinfo.value), 'Key "Targets" not found')

    def test_get_target_error(self):
        mock_ev = MagicMock(list_targets_by_rule=MagicMock(
            side_effect=ValueError('error')))
        mock_name = MagicMock()

        with raises(ValueError) as excinfo:
            AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        self.assertEqual(str(excinfo.value), 'error')

    def test_get_target_empty_targets(self):
        mock_ev = MagicMock(list_targets_by_rule=MagicMock(
            return_value={'Targets': []}))
        mock_name = MagicMock()

        with raises(TaskNotFoundException) as excinfo:
            AwsTaskSchedulerAdapter._get_target(mock_ev, mock_name)

        self.assertEqual(str(excinfo.value), 'Empty target list found')

    def test_get_identifier_from_target(self):
        mock_target = {'Input': '{"era_id": "Ident"}', 'Id': 'meu id'}
        result = AwsTaskSchedulerAdapter._get_identifier_from_target(
            mock_target)
        assert result == 'Ident'

    def test_get_runner_from_target(self):
        mock_target = {'Input': '{"identifier": "asdf"}', 'Id': 'meu id'}
        result = AwsTaskSchedulerAdapter._get_runner_from_target(
            mock_target)
        assert result == 'meu id'

    @patch.object(AwsTaskSchedulerAdapter, '_datetime_from_cron_expression')
    def test_get_exectime(self, mock_datetime_from_cron):
        mock_ev = MagicMock()
        mock_name = MagicMock()
        result = AwsTaskSchedulerAdapter._get_exectime(mock_ev, mock_name)

        mock_ev.describe_rule.assert_called_with(Name=mock_name)
        mock_rule = mock_ev.describe_rule()
        mock_rule.__getitem__.assert_called_with('ScheduleExpression')
        mock_expression = mock_rule.__getitem__()
        mock_datetime_from_cron.assert_called_with(mock_expression)

        self.assertEqual(result, mock_datetime_from_cron())

    @patch.object(AwsTaskSchedulerAdapter, '_get_target')
    @patch.object(AwsTaskSchedulerAdapter, '_get_init_events_client')
    @patch.object(AwsTaskSchedulerAdapter, '_get_identifier_from_target')
    @patch.object(AwsTaskSchedulerAdapter, '_get_runner_from_target')
    @patch.object(AwsTaskSchedulerAdapter, '_get_exectime')
    def test_get_current(self,
                         mock_get_exectime,
                         mock_get_runner,
                         mock_get_ident,
                         mock_get_ev,
                         mock_get_target):
        mock_name = MagicMock()
        mock_get_target.return_value = {'Input': '{"identifier": "asdf"}',
                                        'Id': 'meu id'}
        result = AwsTaskSchedulerAdapter.get_current(mock_name)

        mock_get_target.assert_called_with(mock_get_ev(), mock_name)
        mock_get_ident.assert_called_with(mock_get_target())
        mock_get_runner.assert_called_with(mock_get_target())
        mock_get_exectime.assert_called_with(mock_get_ev(), mock_name)

        self.assertIsInstance(result, AwsTaskSchedulerAdapter)

        self.assertEqual(result.name, mock_name)
        self.assertEqual(result.task_id, mock_get_ident())
        self.assertEqual(result.execution_time, mock_get_exectime())
        self.assertEqual(result.lambda_runner, mock_get_runner())

    @patch.object(AwsTaskSchedulerAdapter, '_put_rule')
    @patch.object(AwsTaskSchedulerAdapter, '_put_targets')
    @patch.object(AwsTaskSchedulerAdapter, 'make_stmt_id')
    @patch.object(AwsTaskSchedulerAdapter, '_add_permission')
    def test__set(self,
                  mock_add_permission,
                  mock_make_stmt,
                  mock_put_targets,
                  mock_put_rule):
        atsa = self.atsa_factory().atsa

        atsa._set()
        mock_put_rule.assert_called_once()
        mock_put_targets.assert_called_once()
        mock_make_stmt.assert_called_with(mock_put_rule())
        mock_add_permission.assert_called_with(mock_make_stmt(),
                                               mock_put_rule())

    @patch.object(AwsTaskSchedulerAdapter, '_remove_permission')
    @patch.object(AwsTaskSchedulerAdapter, '_remove_targets')
    @patch.object(AwsTaskSchedulerAdapter, '_remove_rule')
    @patch.object(AwsTaskSchedulerAdapter, '_get_rule_arn')
    @patch.object(AwsTaskSchedulerAdapter, 'make_stmt_id')
    def test__delete(self,
                     mock_make_stmt,
                     mock_get_rule,
                     mock_remove_rule,
                     mock_remove_targets,
                     mock_remove_permission):
        atsa = self.atsa_factory().atsa

        atsa._delete()

        mock_get_rule.assert_called_once()
        mock_make_stmt.assert_called_with(mock_get_rule())
        mock_remove_permission.assert_called_with(mock_make_stmt())
        mock_remove_targets.assert_called_once()
        mock_remove_rule.assert_called_once()

    def test_make_cron_expression(self):
        mock_date = datetime(2020, 1, 2, 3, 4)
        result = AwsTaskSchedulerAdapter._make_cron_expression(mock_date)

        self.assertEqual(result, 'cron(4 3 2 1 ? 2020)')

    def test_get_lambda_function_arn(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa.lambda_client.get_function_configuration = MagicMock(
            return_value={'FunctionArn': 'fnconfig'})

        result = atsa._get_lambda_function_arn()

        atsa.lambda_client.get_function_configuration.assert_called_with(
            FunctionName=atsa.lambda_runner)

        self.assertEqual(result, 'fnconfig')

    @patch.object(AwsTaskSchedulerAdapter, '_make_cron_expression')
    def test_put_rule(self, mock_make_cron):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_put_rule = MagicMock(return_value={'RuleArn': 'the rule arn!'})
        atsa.events_client.put_rule = mock_put_rule
        mock_exec_time = MagicMock()
        result = atsa._put_rule(mock_exec_time)

        mock_put_rule.assert_called_with(Name=atsa.name,
                                         ScheduleExpression=mock_make_cron())

        self.assertEqual(result, 'the rule arn!')

    @patch.object(AwsTaskSchedulerAdapter, '_make_targets')
    def test_put_targets(self, mock_make_targets):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa.events_client = MagicMock()
        result = atsa._put_targets()

        atsa.events_client.put_targets.assert_called_with(
            Rule=atsa.name,
            Targets=mock_make_targets()
        )
        self.assertEqual(result, atsa.events_client.put_targets())

    @patch.object(AwsTaskSchedulerAdapter, '_get_lambda_function_arn')
    def test_make_targets(self, mock_glfa):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory(
            identifier='sou eu').atsa

        atsa.name = 'scheduler_name'
        result = atsa._make_targets()

        mock_glfa.assert_called_once()

        expected = [{
            'Id': atsa.lambda_runner,
            'Arn': mock_glfa(),
            'Input': '{"scheduler_name": "scheduler_name", "era_id": "sou eu"}'
        }]

        self.assertEqual(result, expected)

    def test_make_stmt_id(self):
        result = AwsTaskSchedulerAdapter.make_stmt_id('um role arn qualquer')
        self.assertEqual(result, '13ad085fd6c4e295090a8238d852d1ea'
                                 '2af5b5f618efbf7255c48ad9de0507e4')

    def test__get_policy_statement_ids(self):
        mock_policy = dict(Policy='{"Statement": [{"Sid": 1}, {"Sid": 2}]}')
        result = AwsTaskSchedulerAdapter._get_policy_statement_ids(mock_policy)

        self.assertListEqual(result, [1, 2])

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy')
    @patch.object(AwsTaskSchedulerAdapter, '_remove_policies')
    def test_clear_permissions(self, mock_remove_policies, mock_get_policy):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa._clear_permissions()

        mock_get_policy.assert_called_once()
        mock_remove_policies.assert_called_with(mock_get_policy())

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy',
                  side_effect=ValueError('nada'))
    @patch.object(AwsTaskSchedulerAdapter, '_remove_policies')
    @patch.object(AwsTaskSchedulerAdapter, '_is_resource_not_found_exception',
                  return_value=True)
    def test_clear_permissions_empty(self,
                                     mock_is_resource_not_found,
                                     mock_remove_policies,
                                     mock_get_policy):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        atsa._clear_permissions()

        mock_is_resource_not_found.assert_called_once()
        mock_get_policy.assert_called_once()
        mock_remove_policies.assert_not_called()

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy',
                  side_effect=ValueError('Erro mesmo'))
    @patch.object(AwsTaskSchedulerAdapter, '_remove_policies')
    @patch.object(AwsTaskSchedulerAdapter, '_is_resource_not_found_exception',
                  return_value=False)
    def test_clear_permissions_error(
            self, _mock_is_resource_not_found, _mock_remove_policies,
            _mock_get_policy):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        with raises(ValueError) as excinfo:
            atsa._clear_permissions()

        self.assertEqual(str(excinfo.value), 'Erro mesmo')

    def test_is_resource_not_found_exception(self):
        mock = MagicMock(
            __class__=MagicMock(
                __name__='ResourceNotFoundException'))
        result = AwsTaskSchedulerAdapter._is_resource_not_found_exception(mock)
        self.assertTrue(result)

    def test_not_is_resource_not_found_exception(self):
        mock = ValueError('oops')
        result = AwsTaskSchedulerAdapter._is_resource_not_found_exception(mock)
        self.assertFalse(result)

    @patch.object(AwsTaskSchedulerAdapter, '_get_policy_statement_ids',
                  return_value=[17, 42])
    def test_remove_policies(self, mock_gpsi):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa

        mock_policies = MagicMock()
        atsa.lambda_client = MagicMock()
        atsa._remove_policies(mock_policies)

        mock_gpsi.assert_called_with(mock_policies)

        atsa.lambda_client.remove_permission.assert_has_calls(
            [call(FunctionName=atsa.lambda_runner, StatementId=17),
             call(FunctionName=atsa.lambda_runner, StatementId=42)])

    def test__get_policy(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.lambda_client = MagicMock()
        result = atsa._get_policy()

        atsa.lambda_client.get_policy.assert_called_with(
            FunctionName=atsa.lambda_runner)

        self.assertEqual(result, atsa.lambda_client.get_policy())

    @patch.object(AwsTaskSchedulerAdapter, '_clear_permissions')
    def test__add_permission(self, mock_clear_permission):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.lambda_client = MagicMock()
        mock_stmt_id = MagicMock()
        mock_rule_arn = MagicMock()
        atsa._add_permission(mock_stmt_id, mock_rule_arn)

        mock_clear_permission.assert_called_once()
        atsa.lambda_client.add_permission.assert_called_with(
            Action='lambda:InvokeFunction',
            FunctionName=atsa.lambda_runner,
            Principal='events.amazonaws.com',
            SourceArn=mock_rule_arn,
            StatementId=mock_stmt_id
        )

    def test__remove_permission(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.lambda_client = MagicMock()
        mock_stmt = MagicMock()
        atsa._remove_permission(mock_stmt)
        atsa.lambda_client.remove_permission.assert_called_with(
            FunctionName=atsa.lambda_runner,
            StatementId=mock_stmt
        )

    def test__remove_targets(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.events_client = MagicMock()
        atsa._remove_targets()

        atsa.events_client.remove_targets.assert_called_with(
            Rule=atsa.name,
            Ids=[atsa.lambda_runner])

    def test__remove_rule(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.events_client = MagicMock()
        atsa._remove_rule()
        atsa.events_client.delete_rule.assert_called_with(Name=atsa.name)

    def test__get_rule_arn(self):
        atsa: AwsTaskSchedulerAdapter = self.atsa_factory().atsa
        atsa.events_client = MagicMock()
        result = atsa._get_rule_arn()
        atsa.events_client.describe_rule.assert_called_with(Name=atsa.name)
        mock_describe_rule = atsa.events_client.describe_rule()
        mock_describe_rule.__getitem__.assert_called_with('Arn')
        assert result == mock_describe_rule.__getitem__()
