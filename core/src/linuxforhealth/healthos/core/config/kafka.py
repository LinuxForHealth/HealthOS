"""
kafka.py
Pydantic models used to support external yaml configurations for Kafka Consumers and Producers
BaseModel rather than BaseSettings specifically to limit config support to a file based YAML config.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class KafkaConsumerConfig(BaseModel):
    """
    Kafka Consumer Configuration Settings
    """

    topics: str = Field(
        description="The Kafka topics to subscribe to. Multiple values are separated by commas."
    )
    bootstrap_servers: str | List = Field(
        description="host[:port] or list of host[:port] the consumer connects to."
    )
    client_id: Optional[str] = Field(
        description="The client name or identifier used to identify specific server side log entries"
    )
    group_id: Optional[str] = Field(
        description="Name of the consumer group to join, if enabled"
    )
    fetch_min_bytes: int = Field(
        default=1,
        description="Minimum amount of data the server should return for a fetch request.",
    )
    fetch_max_bytes: Optional[int] = Field(
        default=1,
        description="Maximum amount of data the server should return for a fetch request.",
    )
    max_partition_fetch_bytes: int = Field(
        default=1048576,
        description="Maximum amount of data per-partition the server will return.",
    )
    max_poll_records: int = Field(
        default=None,
        description="Maximum number of records returned in a single call to getmany(). "
        + "Defaults to None which is `no limit`",
    )
    request_timeout_ms: int = Field(
        default=40000, description="Client request timeout in milliseconds."
    )
    retry_backoff_ms: int = Field(
        default=100, description="Milliseconds to backoff when retrying on errors."
    )
    auto_offset_reset: str = Field(
        default="latest",
        description="A policy for resetting offsets on OffsetOutOfRange errors: "
        + "'earliest' will move to the oldest available message, 'latest' will "
        + "move to the most recent, and 'none' will raise an exception so "
        + "you can handle this case.",
    )
    enable_auto_commit: bool = Field(
        default=True, description="Enables consumer offset background commit."
    )
    auto_commit_interval_ms: int = Field(
        default=5000,
        description="milliseconds between automatic offset commits, if"
        + "enable_auto_commit is True",
    )
    check_crcs: bool = Field(
        default=True,
        description="Automatically check the CRC32 of the records consumed.",
    )
    metadata_max_age_ms: int = Field(
        default=300000,
        description="Specifies the number of milliseconds until metadata is refreshed.",
    )
    partition_assignment_strategy: List[str] = Field(
        default=["RoundRobinPartitionAssignor"],
        description="List of objects to use to distribute partition "
        + "ownership amongst consumer instances when group "
        + "management is used",
    )
    max_poll_interval_ms: int = Field(
        default=300000,
        description=" Maximum allowed time between calls to consume messages.",
    )
    rebalance_timeout_ms: Optional[int] = Field(
        description="The maximum time server will wait for this consumer to rejoin the group in a case of rebalance."
    )
    session_timeout_ms: int = Field(
        default=10000, description="Client group session and failure detection timeout."
    )
    heartbeat_interval_ms: int = Field(
        default=3000,
        description="The expected time in milliseconds between heartbeats to the "
        + "consumer coordinator when usin Kafka's group management feature.",
    )
    consumer_timeout_ms: int = Field(
        default=200, description="maximum wait timeout for background fetching routine."
    )
    api_version: str = Field(
        default="auto", description="specify which kafka API version to use."
    )
    security_protocol: str = Field(
        default="PLAINTEXT",
        description="Protocol used to communicate with brokers.",
        regex="^(PLAINTEXT|SSL|SASL_PLAINTEXT|SASL_SSL)$",
    )
    exclude_internal_topics: bool = Field(
        default=True,
        description="Whether records from internal topics (such as offsets) should "
        + "be exposed to the consumer",
    )
    connections_max_idle_ms: int = Field(
        default=540000,
        description="Close idle connections after the number of milliseconds "
        + "specified by this config. Set to None to disable.",
    )
    isolation_level: str = Field(
        default="read_uncommitted",
        description="Controls how to read messages written transactionally.",
        regex="^(read_uncommitted|read_committed)$",
    )
    sasl_mechanism: str = Field(
        default="PLAIN",
        description="Authentication mechanism when security_protocol is configured for "
        + "SASL_PLAINTEXT or SASL_SSL.",
        regex="^(PLAIN|GSSAPI|SCRAM-SHA-256|SCRAM-SHA-512|OAUTHBEARER)$",
    )
    sasl_plain_username: str = Field(
        default=None, description="username for sasl PLAIN authentication."
    )
    sasl_plain_password: str = Field(
        default=None, description="password for sasl PLAIN authentication."
    )
