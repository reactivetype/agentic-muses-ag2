# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Portions derived from  https://github.com/microsoft/autogen are under the MIT License.
# SPDX-License-Identifier: MIT
# !/usr/bin/env python3 -m pytest

from autogen.agentchat.contrib.agent_eval.task import Task


def test_parse_json_str():
    task = Task(**{
        "name": "Math problem solving",
        "description": "Given any question, the system needs to solve the problem as consisely and accurately as possible",
        "successful_response": '{"message": "The answer is 5", "is_correct": True}',
        "failed_response": '{"message": "I don\'t know the answer", "is_correct": False}',
    })
    assert task
    assert task.name == "Math problem solving"
    assert (
        task.description
        == "Given any question, the system needs to solve the problem as consisely and accurately as possible"
    )
    assert task.successful_response == '{"message": "The answer is 5", "is_correct": True}'
    assert task.failed_response == '{"message": "I don\'t know the answer", "is_correct": False}'
