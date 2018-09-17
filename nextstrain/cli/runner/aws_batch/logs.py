"""
Log handling for AWS Batch jobs.
"""

import boto3
import threading
from typing import Callable, Generator, Mapping, MutableSet


def fetch_stream(stream: str, start_time: int = None) -> Generator[dict, None, None]:
    """
    Fetch all log entries from the named AWS Batch job *stream*.  Returns a
    generator.

    If the *start_time* argument is given, only entries with timestamps on or
    after the given value are fetched.
    """

    log_events = boto3.client("logs").get_paginator("filter_log_events")

    query = {
        "logGroupName": "/aws/batch/job",
        "logStreamNames": [ stream ],
    } # type: dict

    if start_time:
        query["startTime"] = start_time

    for page in log_events.paginate(**query):
        yield from page.get("events", [])


class LogWatcher(threading.Thread):
    """
    Monitor an AWS Batch job log stream and call a supplied function (the
    *consumer*) with each log entry.

    This is a Thread.  Call start() to begin monitoring the log stream and
    stop() (and then join()) to stop.
    """

    def __init__(self, stream: str, consumer: Callable[[dict], None]) -> None:
        super().__init__(name = "log-watcher")
        self.stream   = stream
        self.consumer = consumer
        self.stopped  = threading.Event()

    def stop(self) -> None:
        """
        Tell the log watcher to cease watching for new logs.

        You must call the watcher's join() method after calling stop() to wait
        for the watcher thread to exit.
        """
        self.stopped.set()

    def run(self) -> None:
        """
        Watch for new logs and pass each log entry to the "consumer" function.
        """

        # Track the last timestamp we see.  When we fetch_stream() again on the
        # next iteration, we'll start from that timestamp onwards to avoid
        # fetching every single page again.  The last event or two will be
        # still be in the response, but our de-duping will ignore those.
        last_timestamp = None

        # Keep track of what log entries we've consumed so that we suppress
        # duplicates.  Duplicates will arise in our stream due to the way we
        # watch for new entries.
        consumed = set()    # type: MutableSet

        while not self.stopped.wait(0.2):
            for entry in fetch_stream(self.stream, start_time = last_timestamp):
                if entry["eventId"] not in consumed:
                    consumed.add(entry["eventId"])

                    last_timestamp = entry["timestamp"]

                    self.consumer(entry)
