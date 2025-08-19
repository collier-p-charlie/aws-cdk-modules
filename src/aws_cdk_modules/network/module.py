# -*- encode: utf-8 -*-

import logging

from aws_cdk import Fn
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from aws_cdk_modules.base import BaseModule
from aws_cdk_modules.network.variables import NetworkParameters

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NetworkModule(BaseModule, Construct):
    """CDK module relating to network infrastructure."""

    def __init__(
        self,
        construct_id: str,
        scope: Construct,
        *,
        name_prefix: str | None = None,
        vpc_cidr: str | None = None,
        azs: list[str] | None = None,
        subnet_size_mask: int | None = None,
        **kwargs: dict,
    ) -> None:
        """Network construct initializer.

        Args:
            id_:    X
            scope:  X

        Attributes:
            vpc

        Examples:
            Basic usage:
                ```python
                >>> NetworkModule(
                >>>
                >>> )
                ```
        """
        super(Construct, self).__init__(
            scope=scope,
            id=construct_id,
            **kwargs,
        )

        # Parameter validation
        params = NetworkParameters(
            name_prefix=name_prefix,
            vpc_cidr=vpc_cidr,
            azs=azs,
            subnet_size_mask=subnet_size_mask,
        )

        self.vpc = ec2.CfnVPC(
            scope,
            f"{construct_id}Vpc",
            cidr_block=params.vpc_cidr,
            enable_dns_hostnames=True,
            enable_dns_support=True,
        )

        # Public subnets
        self.public_subnets: list[str] = []
        azs = params.azs or []
        for az in azs:
            ec2.CfnSubnet(
                scope,
                f"{construct_id}PublicSubnet",
                vpc_id=self.vpc.attr_cidr_block,
            )

            Fn.cidr()
