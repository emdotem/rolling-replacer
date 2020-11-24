from time import sleep

from src.aws import aws_autoscaling_group
from src.core.strategy.blue_green.step import BlueGreenStep


class WaitUntilNewInstancesAreHealthyStep(BlueGreenStep):
    def execute(self) -> bool:
        all_healthy = False

        while not all_healthy:
            asg = aws_autoscaling_group.get(self.new_autoscaling_group.name)

            pending_instance_ids = [
                i.id
                for i in asg.provisioning_instances
                if i.health_status != "Healthy" or i.lifecycle_state != "InService"
            ]

            all_healthy = all(
                i.health_status == "Healthy" and i.lifecycle_state == "InService"
                for i in asg.provisioning_instances
            )

            if not all_healthy:
                self.log(
                    f"{len(pending_instance_ids)} instances are unhealthy ({', '.join(pending_instance_ids)}). Waiting.."
                )
                sleep(3)

        return True

    def post_check(self) -> bool:
        asg = aws_autoscaling_group.get(self.new_autoscaling_group.name)

        if all(
            i.health_status == "Healthy" and i.lifecycle_state == "InService"
            for i in asg.provisioning_instances
        ):
            self.log(f"[PostCheck] All instances are healthy.")

        return True
