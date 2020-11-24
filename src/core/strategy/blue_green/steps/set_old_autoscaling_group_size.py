from src.aws import aws_autoscaling_group
from src.core.strategy.blue_green.step import BlueGreenStep


class SetOldAutoscalingGroupSizeStep(BlueGreenStep):
    def execute(self) -> bool:
        aws_autoscaling_group.set_size(
            self.active_autoscaling_group.name, desired_capacity=0, min_size=0, max_size=0,
        )

        return True

    def pre_check(self) -> bool:
        active_autoscaling_group = aws_autoscaling_group.get(self.active_autoscaling_group.name)
        inactive_autoscaling_group = aws_autoscaling_group.get(self.inactive_autoscaling_group.name)

        self.log(
            f"[PreCheck] old autoscaling property: min_size={active_autoscaling_group.min_size}, max_size={active_autoscaling_group.max_size}, desired_capacity={active_autoscaling_group.desired_capacity}"
        )
        self.log(
            f"[PreCheck] new autoscaling property: min_size={inactive_autoscaling_group.min_size}, max_size={inactive_autoscaling_group.max_size}, desired_capacity={inactive_autoscaling_group.desired_capacity}"
        )

        return True

    def post_check(self) -> bool:
        active_autoscaling_group = aws_autoscaling_group.get(self.active_autoscaling_group.name)
        inactive_autoscaling_group = aws_autoscaling_group.get(self.inactive_autoscaling_group.name)

        self.log(
            f"[PostCheck] old autoscaling property: min_size={active_autoscaling_group.min_size}, max_size={active_autoscaling_group.max_size}, desired_capacity={active_autoscaling_group.desired_capacity}"
        )
        self.log(
            f"[PostCheck] new autoscaling property: min_size={inactive_autoscaling_group.min_size}, max_size={inactive_autoscaling_group.max_size}, desired_capacity={inactive_autoscaling_group.desired_capacity}"
        )

        return True
