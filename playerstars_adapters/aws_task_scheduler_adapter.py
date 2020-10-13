import json
from datetime import datetime
from hashlib import sha256
from typing import Optional

import boto3
from playerstars_domain.utils.datetime_helper import aware_utc
from clapy_basic_classes.basic_scheduler_adapter.basic_scheduler_adapter \
    import BasicTaskSchedulerAdapter, TaskNotFoundException


class AwsTaskSchedulerAdapter(BasicTaskSchedulerAdapter):

    _task_id_name = 'task_id'

    @classmethod
    def get_task_id_name(cls):
        return cls._task_id_name

    def __init__(self,
                 name: str,
                 lambda_runner: str,
                 task_id: Optional[str] = None,
                 execution_time: Optional[datetime] = None):
        super().__init__(name, task_id, execution_time)

        self.lambda_runner = lambda_runner

        self.events_client = self._get_init_events_client()
        self.lambda_client = self._get_init_lambda_client()

    def set(self, task_identifier: str, execution_time: datetime):
        super().set(task_identifier, execution_time)
        self._set()

    def update(self, task_identifier: str, execution_time: datetime):
        super().update(task_identifier, execution_time)
        self._delete()
        self._set()

    def delete(self):
        super().delete()
        self._delete()

    @staticmethod
    def _datetime_from_cron_expression(cron_expression):
        parts = cron_expression.split('cron(')[1].split(')')[0].split(' ')
        parts.remove('?')
        int_parts = [int(p) for p in parts]
        d = datetime(int_parts[4],
                     int_parts[3],
                     int_parts[2],
                     int_parts[1],
                     int_parts[0])
        return aware_utc(d)

    @staticmethod
    def _get_target(events_client, name):
        try:
            targets = events_client.list_targets_by_rule(Rule=name)['Targets']
            return targets[0]
        except Exception as e:
            map_exc = {
                'KeyError': TaskNotFoundException('Key "Targets" not found'),
                'IndexError': TaskNotFoundException('Empty target list found'),
                'ResourceNotFoundException': TaskNotFoundException(
                    'No rule installed at this moment')
            }
            exc_class = e.__class__.__name__
            if exc_class not in map_exc:
                raise e

            raise map_exc[exc_class]

    @staticmethod
    def _get_identifier_from_target(target):
        return json.loads(target['Input'])['era_id']

    @staticmethod
    def _get_runner_from_target(target):
        return target['Id']

    @staticmethod
    def _get_exectime(events_client, name):
        rule = events_client.describe_rule(Name=name)
        schedule_expression = rule['ScheduleExpression']
        exectime = AwsTaskSchedulerAdapter._datetime_from_cron_expression(
            schedule_expression)
        return exectime

    @classmethod
    def get_current(cls, name: str):
        ev = cls._get_init_events_client()
        target = cls._get_target(ev, name)

        runner = cls._get_runner_from_target(target)
        execution_time = cls._get_exectime(ev, name)
        task_id = cls._get_identifier_from_target(target)

        return cls(name=name,
                   task_id=task_id,
                   execution_time=execution_time,
                   lambda_runner=runner)

    def _set(self):
        rule_arn = self._put_rule(self.execution_time)
        self._put_targets()
        stmt_id = self.make_stmt_id(rule_arn)
        self._add_permission(stmt_id, rule_arn)

    def _get_rule_arn(self):
        rule = self.events_client.describe_rule(Name=self.name)
        return rule['Arn']

    def _delete(self):
        rule_arn = self._get_rule_arn()
        stmt_id = self.make_stmt_id(rule_arn)
        self._remove_permission(stmt_id)
        self._remove_targets()
        self._remove_rule()

    @staticmethod
    def _get_init_lambda_client():
        lambda_client = boto3.client('lambda')
        return lambda_client

    @staticmethod
    def _get_init_events_client():
        events_client = boto3.client('events')
        return events_client

    @staticmethod
    def _make_cron_expression(event_date: datetime):
        expression = 'cron({0} {1} {2} {3} ? {4})'.format(
            event_date.minute,
            event_date.hour,
            event_date.day,
            event_date.month,
            event_date.year)
        return expression

    def _get_lambda_function_arn(self) -> str:
        fn_config = self.lambda_client.get_function_configuration(
            FunctionName=self.lambda_runner)

        return fn_config['FunctionArn']

    def _put_rule(self, execution_time: datetime) -> str:
        response = self.events_client.put_rule(
            Name=self.name,
            ScheduleExpression=self._make_cron_expression(execution_time))
        rule_arn = response['RuleArn']
        return rule_arn

    def _put_targets(self):
        scheduled_lambda = self._make_targets()
        target_response = self.events_client.put_targets(
            Rule=self.name,
            Targets=scheduled_lambda)
        return target_response

    def _make_targets(self):
        lambda_input = dict(scheduler_name=self.name,
                            era_id=self.task_id)
        lambda_arn = self._get_lambda_function_arn()
        scheduled_lambda = [{
            'Id': self.lambda_runner,
            'Arn': lambda_arn,
            'Input': json.dumps(lambda_input)
        }]
        return scheduled_lambda

    @staticmethod
    def make_stmt_id(rule_arn):
        h = sha256(rule_arn.encode('utf-8'))
        return h.hexdigest()

    @staticmethod
    def _get_policy_statement_ids(policy):
        stmts = json.loads(policy['Policy'])['Statement']
        return [x['Sid'] for x in stmts]

    @staticmethod
    def _is_resource_not_found_exception(exc):
        return exc.__class__.__name__ == 'ResourceNotFoundException'

    def _clear_permissions(self):
        try:
            policies = self._get_policy()
        except Exception as e:
            if self._is_resource_not_found_exception(e):
                return
            else:
                raise e

        self._remove_policies(policies)

    def _remove_policies(self, policy):
        for stmt in self._get_policy_statement_ids(policy):
            self.lambda_client.remove_permission(
                FunctionName=self.lambda_runner,
                StatementId=stmt
            )

    def _get_policy(self):
        policy = self.lambda_client.get_policy(
            FunctionName=self.lambda_runner)
        return policy

    def _add_permission(self, stmt_id, rule_arn):
        self._clear_permissions()
        self.lambda_client.add_permission(
            Action='lambda:InvokeFunction',
            FunctionName=self.lambda_runner,
            Principal='events.amazonaws.com',
            SourceArn=rule_arn,
            StatementId=stmt_id
        )

    def _remove_permission(self, stmt_id):
        self.lambda_client.remove_permission(
            FunctionName=self.lambda_runner,
            StatementId=stmt_id
        )

    def _remove_targets(self):
        self.events_client.remove_targets(
            Rule=self.name,
            Ids=[self.lambda_runner])

    def _remove_rule(self):
        self.events_client.delete_rule(Name=self.name)
