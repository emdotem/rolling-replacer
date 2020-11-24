import boto3

from src.aws import aws_load_balancer
from src.core.strategy.blue_green.step import BlueGreenStep

client = boto3.client("elbv2")


class ReRouteTrafficStep(BlueGreenStep):
    def execute(self) -> bool:
        aws_load_balancer.set_rules_priority(
            self.listener_rule_blue.arn,
            self.listener_rule_green.priority,
            self.listener_rule_green.arn,
            self.listener_rule_blue.priority,
        )

        return True
