from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws.instance import Instance
from imports.aws.provider import AwsProvider

class MyMultipleStacksConfig:
    environment: str
    region: str = None
    amiID: str = None
    def __init__(self, environment: str, region: str = None, amiID: str = None):
        self.environment = environment
        self.region = region
        self.amiID = amiID


class MyMultipleStacks(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: MyMultipleStacksConfig):
        super().__init__(scope, id)

        region = "eu-west-1" if config.region == None else config.region
        amiID = "ami-0d64bb532e0502c46" if config.amiID == None else config.amiID

        AwsProvider(self, "aws",
            region = region
        )

        Instance(self, "Hello",
            ami = amiID,
            instance_type = "t2.micro",
            tags = {
                "environment": config.environment,
            }
        )

multi_stack_app = App()
MyMultipleStacks(multi_stack_app, "multiple-stacks-dev", MyMultipleStacksConfig(environment = "dev"))
MyMultipleStacks(multi_stack_app, "multiple-stacks-staging", MyMultipleStacksConfig(environment = "staging"))
MyMultipleStacks(multi_stack_app, "multiple-stacks-production-uk", MyMultipleStacksConfig(environment = "staging", region = "eu-west-2", amiID="ami-0e8d228ad90af673b"))

multi_stack_app.synth()
