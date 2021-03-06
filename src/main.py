import logging

import click

from src.core.rolling import Rolling
from src.core.strategy.blue_green.strategy import BlueGreenStrategy
from src.decorators import configure_logging

logger = logging.getLogger(__name__)


@click.group()
def rolling_replacer() -> None:
    pass


@rolling_replacer.command(name="blue-green")
@click.argument("autoscaling_group_blue_name")
@click.argument("target_group_blue_name")
@click.argument("listener_rule_blue_arn")
@click.argument("autoscaling_group_green_name")
@click.argument("target_group_green_name")
@click.argument("listener_rule_green_arn")
@click.argument("load_balancer_name")
@click.option("-v", "--verbose", count=True)
@configure_logging
def blue_green(
    autoscaling_group_blue_name: str,
    target_group_blue_name: str,
    listener_rule_blue_arn: str,
    autoscaling_group_green_name: str,
    target_group_green_name: str,
    listener_rule_green_arn: str,
    load_balancer_name: str,
    verbose: int,
) -> None:
    rolling = Rolling(
        BlueGreenStrategy(
            load_balancer_name,
            autoscaling_group_blue_name,
            target_group_blue_name,
            listener_rule_blue_arn,
            autoscaling_group_green_name,
            target_group_green_name,
            listener_rule_green_arn,
        ),
    )

    rolling.execute()


@rolling_replacer.command()
def hello() -> None:
    click.echo("Hello, desperate AWS Dev Ops.")


if __name__ == "__main__":
    rolling_replacer()
