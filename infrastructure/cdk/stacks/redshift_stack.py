from aws_cdk import core
from aws_cdk import aws_redshift as redshift
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_kms as kms

class RedshiftStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define a VPC where Redshift will be deployed
        vpc = ec2.Vpc(self, "AnalyticsVpc", max_azs=2)

        # KMS key for encryption
        kms_key = kms.Key(self, "RedshiftKmsKey",
            description="Key for encrypting Redshift data",
            enable_key_rotation=True
        )

        # Define a security group for Redshift
        redshift_security_group = ec2.SecurityGroup(
            self, "RedshiftSG",
            vpc=vpc,
            description="Allow access to Redshift",
            allow_all_outbound=True
        )

        redshift_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(5439), "Allow Redshift access"
        )

        # Create a Redshift Cluster with encryption
        cluster = redshift.Cluster(
            self, "RedshiftCluster",
            master_user=redshift.Login(
                master_username="admin",
            ),
            vpc=vpc,
            security_groups=[redshift_security_group],
            cluster_type=redshift.ClusterType.MULTI_NODE,
            node_type=redshift.NodeType.DC2_LARGE,
            number_of_nodes=2,
            default_database_name="analytics_db",
            encrypted=True,  # Enable encryption
            encryption_key=kms_key,
            removal_policy=core.RemovalPolicy.DESTROY  # Optional: Automatically delete the cluster when the stack is destroyed
        )

        # Output the cluster endpoint and port
        core.CfnOutput(self, "RedshiftEndpoint", value=cluster.cluster_endpoint.hostname)
        core.CfnOutput(self, "RedshiftPort", value=cluster.cluster_endpoint.port)
