# -*- encode: utf-8 -*-

import logging
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NetworkParameters(BaseModel):
    """Parameters for the NetworkModule."""

    name_prefix: Annotated[
        str,
        Field(
            default="network",
            description="Prefix for naming resources in this module.",
        ),
    ]

    vpc_cidr: Annotated[
        str,
        Field(
            "10.0.0.0/16",
            description="CIDR block for the VPC.",
            pattern=r"^([0-9]{1,3}\.){3}[0-9]{1,3}/\d{1,2}$",
        ),
    ]

    azs: Annotated[
        list[str] | None,
        Field(
            default=None,
            description="Availability Zones to use for the VPC.",
        ),
    ]

    subnet_size_mask: Annotated[
        int,
        Field(
            ...,
            description="Subnet size mask for the VPC subnets; must be between 16 and 28.",
            ge=16,
            le=28,
        ),
    ]

    @model_validator(mode="after")
    def check_subnet_size_mask(self) -> "NetworkParameters":
        """Ensure subnet size mask is valid relative to CIDR block."""
        vpc_cidr_mask = int(self.vpc_cidr.split("/")[-1])
        if self.subnet_size_mask <= vpc_cidr_mask:
            raise ValueError("Subnet size mask must be greater than that of the VPC CIDR.")
        return self

    @model_validator(mode="after")
    def check_sufficient_subnet_space(self) -> "NetworkParameters":
        """Ensure there is sufficient IP space within the VPC for all subnets."""
        vpc_cidr_mask = int(self.vpc_cidr.split("/")[-1])
        if self.subnet_size_mask <= vpc_cidr_mask:
            raise ValueError("Subnet size mask must be greater than that of the VPC CIDR.")
        return self
