# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Optional, Union
from unittest.mock import MagicMock, _Call, call
from uuid import UUID

import pytest
import termcolor.termcolor

from autogen.agentchat.conversable_agent import ConversableAgent
from autogen.agentchat.group import ContextVariables
from autogen.coding.base import CodeBlock
from autogen.events.agent_events import (
    ClearAgentsHistoryEvent,
    ClearConversableAgentHistoryEvent,
    ClearConversableAgentHistoryWarningEvent,
    ConversableAgentUsageSummaryEvent,
    ConversableAgentUsageSummaryNoCostIncurredEvent,
    EventRole,
    ExecuteCodeBlockEvent,
    ExecuteFunctionEvent,
    ExecutedFunctionEvent,
    FunctionCallEvent,
    FunctionResponseEvent,
    GenerateCodeExecutionReplyEvent,
    GroupChatResumeEvent,
    GroupChatRunChatEvent,
    PostCarryoverProcessingEvent,
    RunCompletionEvent,
    SelectSpeakerEvent,
    SelectSpeakerInvalidInputEvent,
    SelectSpeakerTryCountExceededEvent,
    SpeakerAttemptFailedMultipleAgentsEvent,
    SpeakerAttemptFailedNoAgentsEvent,
    SpeakerAttemptSuccessfulEvent,
    TerminationAndHumanReplyNoInputEvent,
    TerminationEvent,
    TextEvent,
    ToolCallEvent,
    ToolResponseEvent,
    UsingAutoReplyEvent,
    create_received_event_model,
)
from autogen.events.base_event import get_event_classes
from autogen.import_utils import optional_import_block, run_for_optional_imports

with optional_import_block():
    import PIL


EVENT_CLASSES = get_event_classes()


@pytest.fixture(autouse=True)
def enable_color_in_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_can_do_colour(*args: Any, **kwargs: Any) -> bool:
        return True

    monkeypatch.setattr(termcolor.termcolor, "_can_do_colour", mock_can_do_colour)


@pytest.fixture
def sender() -> ConversableAgent:
    return ConversableAgent("sender", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER")


@pytest.fixture
def recipient() -> ConversableAgent:
    return ConversableAgent("recipient", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER")


class TestToolResponseEvent:
    event = {
        "role": "tool",
        "tool_responses": [
            {"tool_call_id": "call_rJfVpHU3MXuPRR2OAdssVqUV", "role": "tool", "content": "Timer is done!"},
            {"tool_call_id": "call_zFZVYovdsklFYgqxttcOHwlr", "role": "tool", "content": "Stopwatch is done!"},
        ],
        "content": "Timer is done!\\n\\nStopwatch is done!",
    }

    expected = {
        "type": "tool_response",
        "content": {
            "role": "tool",
            "sender": "sender",
            "recipient": "recipient",
            "content": "Timer is done!\\n\\nStopwatch is done!",
            "tool_responses": [
                {"tool_call_id": "call_rJfVpHU3MXuPRR2OAdssVqUV", "role": "tool", "content": "Timer is done!"},
                {"tool_call_id": "call_zFZVYovdsklFYgqxttcOHwlr", "role": "tool", "content": "Stopwatch is done!"},
            ],
        },
    }

    def test_print(self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent) -> None:
        actual = create_received_event_model(uuid=uuid, event=self.event, sender=sender, recipient=recipient)
        assert isinstance(actual, ToolResponseEvent)

        self.expected["content"]["uuid"] = uuid

        assert actual.model_dump() == self.expected

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("\x1b[33msender\x1b[0m (to recipient):\n", flush=True),
            call("\x1b[32m***** Response from calling tool (call_rJfVpHU3MXuPRR2OAdssVqUV) *****\x1b[0m", flush=True),
            call("Timer is done!", flush=True),
            call("\x1b[32m**********************************************************************\x1b[0m", flush=True),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
            call("\x1b[32m***** Response from calling tool (call_zFZVYovdsklFYgqxttcOHwlr) *****\x1b[0m", flush=True),
            call("Stopwatch is done!", flush=True),
            call("\x1b[32m**********************************************************************\x1b[0m", flush=True),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        actual = create_received_event_model(uuid=uuid, event=self.event, sender=sender, recipient=recipient)
        assert isinstance(actual, ToolResponseEvent)

        # Test serialization
        self.expected["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected

        # Test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestFunctionResponseEvent:
    @pytest.mark.parametrize(
        "event",
        [
            {"name": "get_random_number", "role": "function", "content": "76"},
            {"name": "get_random_number", "role": "function", "content": 2},
        ],
    )
    def test_print(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent, event: dict[str, Any]
    ) -> None:
        actual = create_received_event_model(uuid=uuid, event=event, sender=sender, recipient=recipient)
        assert isinstance(actual, FunctionResponseEvent)

        expected_model_dump = {
            "type": "function_response",
            "content": {
                "name": "get_random_number",
                "role": "function",
                "content": event["content"],
                "sender": "sender",
                "recipient": "recipient",
                "uuid": uuid,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("\x1b[33msender\x1b[0m (to recipient):\n", flush=True),
            call("\x1b[32m***** Response from calling function (get_random_number) *****\x1b[0m", flush=True),
            call(event["content"], flush=True),
            call("\x1b[32m**************************************************************\x1b[0m", flush=True),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        event = {
            "name": "get_random_number",
            "role": "function",
            "content": 76,
        }
        actual = create_received_event_model(uuid=uuid, event=event, sender=sender, recipient=recipient)
        assert isinstance(actual, FunctionResponseEvent)

        expected = {
            "type": "function_response",
            "content": {
                "name": "get_random_number",
                "role": "function",
                "content": event["content"],
                "sender": "sender",
                "recipient": "recipient",
                "uuid": uuid,
            },
        }

        # Test serialization
        assert actual.model_dump() == expected

        # Test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestFunctionCallEvent:
    fc_event = {
        "content": "Let's play a game.",
        "function_call": {"name": "get_random_number", "arguments": "{}"},
    }

    expected = {
        "type": "function_call",
        "content": {
            "content": "Let's play a game.",
            "sender": "sender",
            "recipient": "recipient",
            "function_call": {"name": "get_random_number", "arguments": "{}"},
        },
    }

    def test_print(self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent) -> None:
        event = create_received_event_model(uuid=uuid, event=self.fc_event, sender=sender, recipient=recipient)

        assert isinstance(event, FunctionCallEvent)

        actual = event.model_dump()
        self.expected["content"]["uuid"] = uuid
        assert actual == self.expected, actual

        mock = MagicMock()
        event.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("\x1b[33msender\x1b[0m (to recipient):\n", flush=True),
            call("Let's play a game.", flush=True),
            call("\x1b[32m***** Suggested function call: get_random_number *****\x1b[0m", flush=True),
            call("Arguments: \n", "{}", flush=True, sep=""),
            call("\x1b[32m******************************************************\x1b[0m", flush=True),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        event = create_received_event_model(uuid=uuid, event=self.fc_event, sender=sender, recipient=recipient)
        assert isinstance(event, FunctionCallEvent)

        self.expected["content"]["uuid"] = uuid
        # Test serialization
        assert event.model_dump() == self.expected

        # Test deserialization
        d = event.model_dump()
        assert event == EVENT_CLASSES[d["type"]].model_validate(d)


class TestToolCallEvent:
    event = {
        "content": None,
        "refusal": None,
        "audio": None,
        "function_call": None,
        "tool_calls": [
            {
                "id": "call_rJfVpHU3MXuPRR2OAdssVqUV",
                "function": {"arguments": '{"num_seconds": "1"}', "name": "timer"},
                "type": "function",
            },
            {
                "id": "call_zFZVYovdsklFYgqxttcOHwlr",
                "function": {"arguments": '{"num_seconds": "2"}', "name": "stopwatch"},
                "type": "function",
            },
        ],
    }

    expected = {
        "type": "tool_call",
        "content": {
            "content": None,
            "refusal": None,
            "audio": None,
            "function_call": None,
            "sender": "sender",
            "recipient": "recipient",
            "tool_calls": [
                {
                    "id": "call_rJfVpHU3MXuPRR2OAdssVqUV",
                    "function": {"arguments": '{"num_seconds": "1"}', "name": "timer"},
                    "type": "function",
                },
                {
                    "id": "call_zFZVYovdsklFYgqxttcOHwlr",
                    "function": {"arguments": '{"num_seconds": "2"}', "name": "stopwatch"},
                    "type": "function",
                },
            ],
        },
    }

    @pytest.mark.parametrize(
        "role",
        ["assistant", None],
    )
    def test_print(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent, role: Optional[EventRole]
    ) -> None:
        self.event["role"] = role

        actual = create_received_event_model(uuid=uuid, event=self.event, sender=sender, recipient=recipient)
        assert isinstance(actual, ToolCallEvent)

        self.expected["content"]["uuid"] = uuid
        self.expected["content"]["role"] = role
        assert actual.model_dump() == self.expected

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("\x1b[33msender\x1b[0m (to recipient):\n", flush=True),
            call("\x1b[32m***** Suggested tool call (call_rJfVpHU3MXuPRR2OAdssVqUV): timer *****\x1b[0m", flush=True),
            call("Arguments: \n", '{"num_seconds": "1"}', flush=True, sep=""),
            call("\x1b[32m**********************************************************************\x1b[0m", flush=True),
            call(
                "\x1b[32m***** Suggested tool call (call_zFZVYovdsklFYgqxttcOHwlr): stopwatch *****\x1b[0m", flush=True
            ),
            call("Arguments: \n", '{"num_seconds": "2"}', flush=True, sep=""),
            call(
                "\x1b[32m**************************************************************************\x1b[0m", flush=True
            ),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        self.event["role"] = None

        actual = create_received_event_model(uuid=uuid, event=self.event, sender=sender, recipient=recipient)
        assert isinstance(actual, ToolCallEvent)

        self.expected["content"]["uuid"] = uuid
        self.expected["content"]["role"] = None
        # Test serialization
        assert actual.model_dump() == self.expected

        # Test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestTextEvent:
    @pytest.mark.parametrize(
        "event, expected_content",
        [
            (
                {"content": "hello {name}", "context": {"name": "there"}},
                "hello {name}",
            ),
            (
                {
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract table from the following image and convert it to Markdown.",
                        }
                    ]
                },
                "Please extract table from the following image and convert it to Markdown.",
            ),
            (
                {
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://media.githubusercontent.com/media/ag2ai/ag2/refs/heads/main/website/static/img/autogen_agentchat.png"
                            },
                        }
                    ]
                },
                "<image>",
            ),
        ],
    )
    def test_print_events(
        self,
        uuid: UUID,
        sender: ConversableAgent,
        recipient: ConversableAgent,
        event: dict[str, Any],
        expected_content: str,
    ) -> None:
        actual = create_received_event_model(uuid=uuid, event=event, sender=sender, recipient=recipient)

        assert isinstance(actual, TextEvent)
        expected_model_dump = {
            "type": "text",
            "content": {
                "uuid": uuid,
                "content": event["content"],
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        expected_call_args_list = [
            call("\x1b[33msender\x1b[0m (to recipient):\n", flush=True),
            call(expected_content, flush=True),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_print_context_lambda_event(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        event = {
            "content": lambda context: f"hello {context['name']}",
            "context": {
                "name": "there",
            },
        }

        actual = create_received_event_model(uuid=uuid, event=event, sender=sender, recipient=recipient)

        assert isinstance(actual, TextEvent)
        expected_model_dump = {
            "type": "text",
            "content": {
                "uuid": uuid,
                "content": "hello there",
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("\x1b[33msender\x1b[0m (to recipient):\n", flush=True),
            call("hello there", flush=True),
            call(
                "\n",
                "--------------------------------------------------------------------------------",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    @run_for_optional_imports("PIL", "unknown")
    def test_serialization(self) -> None:
        image = PIL.Image.new(mode="RGB", size=(200, 200))
        content = [
            {"type": "text", "text": "What's the breed of this dog?\n"},
            {"type": "image_url", "image_url": {"url": image}},
            {"type": "text", "text": "."},
        ]
        uuid = UUID("f1b9b3b4-0b3b-4b3b-8b3b-0b3b3b3b3b3b")
        text_event = TextEvent(content=content, sender="sender", recipient="recipient", uuid=uuid)

        result = text_event.model_dump_json()

        expected = (
            '{"type":"text","content":{"uuid":"f1b9b3b4-0b3b-4b3b-8b3b-0b3b3b3b3b3b",'
            '"content":[{"type":"text","text":"What\'s the breed of this dog?\\n"},'
            '{"type":"image_url","image_url":{"url":"<image>"}},'
            '{"type":"text","text":"."}],"sender":"sender","recipient":"recipient"}}'
        )
        assert str(result) == expected, result

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        event = {
            "content": "hello {name}",
            "context": {"name": "there"},
        }
        actual = create_received_event_model(uuid=uuid, event=event, sender=sender, recipient=recipient)

        assert isinstance(actual, TextEvent)
        expected_model_dump = {
            "type": "text",
            "content": {
                "uuid": uuid,
                "content": event["content"],
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestPostCarryoverProcessingEvent:
    chat_info = {
        "carryover": ["This is a test event 1", "This is a test event 2"],
        "message": "Start chat",
        "verbose": True,
        "summary_method": "last_msg",
        "max_turns": 5,
    }

    expected = {
        "type": "post_carryover_processing",
        "content": {
            "chat_info": {
                "carryover": ["This is a test event 1", "This is a test event 2"],
                "message": "Start chat",
                "verbose": True,
                "sender": "sender",
                "recipient": "recipient",
                "summary_method": "last_msg",
                "summary_args": None,
                "max_turns": 5,
            },
        },
    }

    def test_print(self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent) -> None:
        self.chat_info["sender"] = sender
        self.chat_info["recipient"] = recipient

        self.expected["content"]["uuid"] = uuid

        actual = PostCarryoverProcessingEvent(uuid=uuid, chat_info=self.chat_info)
        assert isinstance(actual, PostCarryoverProcessingEvent)

        assert actual.model_dump() == self.expected, f"{actual.model_dump()} != {self.expected}"

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call(
                "\x1b[34m\n********************************************************************************\x1b[0m",
                flush=True,
                sep="",
            ),
            call("\x1b[34mStarting a new chat....\x1b[0m", flush=True),
            call("\x1b[34mEvent:\nStart chat\x1b[0m", flush=True),
            call("\x1b[34mCarryover:\nThis is a test event 1\nThis is a test event 2\x1b[0m", flush=True),
            call(
                "\x1b[34m\n********************************************************************************\x1b[0m",
                flush=True,
                sep="",
            ),
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        self.chat_info["sender"] = sender
        self.chat_info["recipient"] = recipient

        actual = PostCarryoverProcessingEvent(uuid=uuid, chat_info=self.chat_info)
        assert isinstance(actual, PostCarryoverProcessingEvent)

        self.expected["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)

    @pytest.mark.parametrize(
        "carryover, expected",
        [
            ("This is a test event 1", "This is a test event 1"),
            (
                ["This is a test event 1", "This is a test event 2"],
                "This is a test event 1\nThis is a test event 2",
            ),
            (
                [
                    {"content": "This is a test event 1"},
                    {"content": "This is a test event 2"},
                ],
                "This is a test event 1\nThis is a test event 2",
            ),
            ([1, 2, 3], "1\n2\n3"),
        ],
    )
    def test__process_carryover(
        self,
        carryover: Union[str, list[Union[str, dict[str, Any], Any]]],
        expected: str,
        uuid: UUID,
        sender: ConversableAgent,
        recipient: ConversableAgent,
    ) -> None:
        chat_info = {
            "carryover": carryover,
            "message": "Start chat",
            "verbose": True,
            "sender": sender,
            "recipient": recipient,
            "summary_method": "last_msg",
            "max_turns": 5,
        }

        post_carryover_processing = PostCarryoverProcessingEvent(uuid=uuid, chat_info=chat_info)
        expected_model_dump = {
            "type": "post_carryover_processing",
            "content": {
                "uuid": uuid,
                "chat_info": {
                    "carryover": carryover,
                    "message": "Start chat",
                    "verbose": True,
                    "sender": "sender",
                    "recipient": "recipient",
                    "summary_method": "last_msg",
                    "summary_args": None,
                    "max_turns": 5,
                },
            },
        }
        assert post_carryover_processing.model_dump() == expected_model_dump

        actual = post_carryover_processing.content._process_carryover()  # type: ignore[attr-defined]
        assert actual == expected


class TestClearAgentsHistoryEvent:
    @pytest.mark.parametrize(
        "agent, nr_events_to_preserve, expected",
        [
            (None, None, "Clearing history for all agents."),
            (None, 5, "Clearing history for all agents except last 5 events."),
            (
                ConversableAgent(
                    "clear_agent", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"
                ),
                None,
                "Clearing history for clear_agent.",
            ),
            (
                ConversableAgent(
                    "clear_agent", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"
                ),
                5,
                "Clearing history for clear_agent except last 5 events.",
            ),
        ],
    )
    def test_print(
        self, agent: Optional[ConversableAgent], nr_events_to_preserve: Optional[int], expected: str, uuid: UUID
    ) -> None:
        actual = ClearAgentsHistoryEvent(uuid=uuid, agent=agent, nr_events_to_preserve=nr_events_to_preserve)
        assert isinstance(actual, ClearAgentsHistoryEvent)

        expected_model_dump = {
            "type": "clear_agents_history",
            "content": {
                "uuid": uuid,
                "agent": "clear_agent" if agent else None,
                "nr_events_to_preserve": nr_events_to_preserve,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [call(expected)]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        agent = ConversableAgent(
            "clear_agent", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"
        )
        nr_events_to_preserve = 5
        actual = ClearAgentsHistoryEvent(uuid=uuid, agent=agent, nr_events_to_preserve=nr_events_to_preserve)
        assert isinstance(actual, ClearAgentsHistoryEvent)

        expected_model_dump = {
            "type": "clear_agents_history",
            "content": {
                "uuid": uuid,
                "agent": "clear_agent" if agent else None,
                "nr_events_to_preserve": nr_events_to_preserve,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestSpeakerAttemptSuccessfulEvent:
    @pytest.mark.parametrize(
        "mentions, expected",
        [
            ({"agent_1": 1}, "\x1b[32m>>>>>>>> Select speaker attempt 1 of 3 successfully selected: agent_1\x1b[0m"),
        ],
    )
    def test_print(self, mentions: dict[str, int], expected: str, uuid: UUID) -> None:
        attempt = 1
        attempts_left = 2
        verbose = True

        actual = SpeakerAttemptSuccessfulEvent(
            uuid=uuid,
            mentions=mentions,
            attempt=attempt,
            attempts_left=attempts_left,
            select_speaker_auto_verbose=verbose,
        )
        assert isinstance(actual, SpeakerAttemptSuccessfulEvent)

        expected_model_dump = {
            "type": "speaker_attempt_successful",
            "content": {
                "uuid": uuid,
                "mentions": mentions,
                "attempt": attempt,
                "attempts_left": attempts_left,
                "select_speaker_auto_verbose": verbose,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [call(expected, flush=True)]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        mentions = {"agent_1": 1}
        attempt = 1
        attempts_left = 2
        verbose = True

        actual = SpeakerAttemptSuccessfulEvent(
            uuid=uuid,
            mentions=mentions,
            attempt=attempt,
            attempts_left=attempts_left,
            select_speaker_auto_verbose=verbose,
        )
        assert isinstance(actual, SpeakerAttemptSuccessfulEvent)

        expected_model_dump = {
            "type": "speaker_attempt_successful",
            "content": {
                "uuid": uuid,
                "mentions": mentions,
                "attempt": attempt,
                "attempts_left": attempts_left,
                "select_speaker_auto_verbose": verbose,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestSpeakerAttemptFailedMultipleAgentsEvent:
    @pytest.mark.parametrize(
        "mentions, expected",
        [
            (
                {"agent_1": 1, "agent_2": 2},
                "\x1b[31m>>>>>>>> Select speaker attempt 1 of 3 failed as it included multiple agent names.\x1b[0m",
            ),
        ],
    )
    def test_print(self, mentions: dict[str, int], expected: str, uuid: UUID) -> None:
        attempt = 1
        attempts_left = 2
        verbose = True

        actual = SpeakerAttemptFailedMultipleAgentsEvent(
            uuid=uuid,
            mentions=mentions,
            attempt=attempt,
            attempts_left=attempts_left,
            select_speaker_auto_verbose=verbose,
        )
        assert isinstance(actual, SpeakerAttemptFailedMultipleAgentsEvent)

        expected_model_dump = {
            "type": "speaker_attempt_failed_multiple_agents",
            "content": {
                "uuid": uuid,
                "mentions": mentions,
                "attempt": attempt,
                "attempts_left": attempts_left,
                "select_speaker_auto_verbose": verbose,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [call(expected, flush=True)]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        mentions = {"agent_1": 1, "agent_2": 2}
        attempt = 1
        attempts_left = 2
        verbose = True

        actual = SpeakerAttemptFailedMultipleAgentsEvent(
            uuid=uuid,
            mentions=mentions,
            attempt=attempt,
            attempts_left=attempts_left,
            select_speaker_auto_verbose=verbose,
        )
        assert isinstance(actual, SpeakerAttemptFailedMultipleAgentsEvent)

        expected_model_dump = {
            "type": "speaker_attempt_failed_multiple_agents",
            "content": {
                "uuid": uuid,
                "mentions": mentions,
                "attempt": attempt,
                "attempts_left": attempts_left,
                "select_speaker_auto_verbose": verbose,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestSpeakerAttemptFailedNoAgentsEvent:
    @pytest.mark.parametrize(
        "mentions, expected",
        [
            ({}, "\x1b[31m>>>>>>>> Select speaker attempt #1 failed as it did not include any agent names.\x1b[0m"),
        ],
    )
    def test_print(self, mentions: dict[str, int], expected: str, uuid: UUID) -> None:
        attempt = 1
        attempts_left = 2
        verbose = True

        actual = SpeakerAttemptFailedNoAgentsEvent(
            uuid=uuid,
            mentions=mentions,
            attempt=attempt,
            attempts_left=attempts_left,
            select_speaker_auto_verbose=verbose,
        )
        assert isinstance(actual, SpeakerAttemptFailedNoAgentsEvent)

        expected_model_dump = {
            "type": "speaker_attempt_failed_no_agents",
            "content": {
                "uuid": uuid,
                "mentions": mentions,
                "attempt": attempt,
                "attempts_left": attempts_left,
                "select_speaker_auto_verbose": verbose,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [call(expected, flush=True)]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        mentions = {}
        attempt = 1
        attempts_left = 2
        verbose = True

        actual = SpeakerAttemptFailedNoAgentsEvent(
            uuid=uuid,
            mentions=mentions,
            attempt=attempt,
            attempts_left=attempts_left,
            select_speaker_auto_verbose=verbose,
        )
        assert isinstance(actual, SpeakerAttemptFailedNoAgentsEvent)

        expected_model_dump = {
            "type": "speaker_attempt_failed_no_agents",
            "content": {
                "uuid": uuid,
                "mentions": mentions,
                "attempt": attempt,
                "attempts_left": attempts_left,
                "select_speaker_auto_verbose": verbose,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # test deserialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestGroupChatResumeEvent:
    last_speaker_name = "Coder"
    events = [
        {"content": "You are an expert at coding.", "role": "system", "name": "chat_manager"},
        {"content": "Let's get coding, should I use Python?", "name": "Coder", "role": "assistant"},
    ]
    silent = False

    def test_print(self, uuid: UUID) -> None:
        actual = GroupChatResumeEvent(
            uuid=uuid, last_speaker_name=self.last_speaker_name, events=self.events, silent=self.silent
        )
        assert isinstance(actual, GroupChatResumeEvent)

        expected_model_dump = {
            "type": "group_chat_resume",
            "content": {
                "uuid": uuid,
                "last_speaker_name": self.last_speaker_name,
                "events": self.events,
                "silent": self.silent,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("Prepared group chat with 2 events, the last speaker is", "\x1b[33mCoder\x1b[0m", flush=True)
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        actual = GroupChatResumeEvent(
            uuid=uuid, last_speaker_name=self.last_speaker_name, events=self.events, silent=self.silent
        )
        assert isinstance(actual, GroupChatResumeEvent)

        expected_model_dump = {
            "type": "group_chat_resume",
            "content": {
                "uuid": uuid,
                "last_speaker_name": self.last_speaker_name,
                "events": self.events,
                "silent": self.silent,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestGroupChatRunChatEvent:
    speaker = ConversableAgent(
        "assistant_uno", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"
    )
    silent = False
    expected_model_dump = {
        "type": "group_chat_run_chat",
        "content": {
            "speaker": "assistant_uno",
            "silent": False,
        },
    }

    def test_print(self, uuid: UUID) -> None:
        actual = GroupChatRunChatEvent(uuid=uuid, speaker=self.speaker, silent=self.silent)
        assert isinstance(actual, GroupChatRunChatEvent)

        self.expected_model_dump["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected_model_dump
        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [call("\x1b[32m\nNext speaker: assistant_uno\n\x1b[0m", flush=True)]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        actual = GroupChatRunChatEvent(uuid=uuid, speaker=self.speaker, silent=self.silent)
        assert isinstance(actual, GroupChatRunChatEvent)

        self.expected_model_dump["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestTerminationAndHumanReplyEvent:
    def test_print(self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent) -> None:
        no_human_input_msg = "NO HUMAN INPUT RECEIVED."

        actual = TerminationAndHumanReplyNoInputEvent(
            uuid=uuid,
            no_human_input_msg=no_human_input_msg,
            sender=sender,
            recipient=recipient,
        )
        assert isinstance(actual, TerminationAndHumanReplyNoInputEvent)

        expected_model_dump = {
            "type": "termination_and_human_reply_no_input",
            "content": {
                "uuid": uuid,
                "no_human_input_msg": no_human_input_msg,
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [call("\x1b[31m\n>>>>>>>> NO HUMAN INPUT RECEIVED.\x1b[0m", flush=True)]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        no_human_input_msg = "NO HUMAN INPUT RECEIVED."

        actual = TerminationAndHumanReplyNoInputEvent(
            uuid=uuid,
            no_human_input_msg=no_human_input_msg,
            sender=sender,
            recipient=recipient,
        )
        assert isinstance(actual, TerminationAndHumanReplyNoInputEvent)

        expected_model_dump = {
            "type": "termination_and_human_reply_no_input",
            "content": {
                "uuid": uuid,
                "no_human_input_msg": no_human_input_msg,
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestTerminationEvent:
    def test_print(self, uuid: UUID) -> None:
        termination_reason = "User requested to end the conversation."

        actual = TerminationEvent(
            uuid=uuid,
            termination_reason=termination_reason,
        )
        assert isinstance(actual, TerminationEvent)

        expected_model_dump = {
            "type": "termination",
            "content": {
                "uuid": uuid,
                "termination_reason": termination_reason,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [
            call(
                "\x1b[31m\n>>>>>>>> TERMINATING RUN (" + str(uuid) + "): " + termination_reason + "\x1b[0m", flush=True
            )
        ]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        termination_reason = "User requested to end the conversation."

        actual = TerminationEvent(
            uuid=uuid,
            termination_reason=termination_reason,
        )
        assert isinstance(actual, TerminationEvent)

        expected_model_dump = {
            "type": "termination",
            "content": {
                "uuid": uuid,
                "termination_reason": termination_reason,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestUsingAutoReplyEvent:
    def test_print(self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent) -> None:
        human_input_mode = "ALWAYS"

        actual = UsingAutoReplyEvent(
            uuid=uuid,
            human_input_mode=human_input_mode,
            sender=sender,
            recipient=recipient,
        )
        assert isinstance(actual, UsingAutoReplyEvent)

        expected_model_dump = {
            "type": "using_auto_reply",
            "content": {
                "uuid": uuid,
                "human_input_mode": human_input_mode,
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [call("\x1b[31m\n>>>>>>>> USING AUTO REPLY...\x1b[0m", flush=True)]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        human_input_mode = "ALWAYS"

        actual = UsingAutoReplyEvent(
            uuid=uuid,
            human_input_mode=human_input_mode,
            sender=sender,
            recipient=recipient,
        )
        assert isinstance(actual, UsingAutoReplyEvent)

        expected_model_dump = {
            "type": "using_auto_reply",
            "content": {
                "uuid": uuid,
                "human_input_mode": human_input_mode,
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestExecuteCodeBlockEvent:
    def test_print(self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent) -> None:
        code = """print("hello world")"""
        language = "python"
        code_block_count = 0

        actual = ExecuteCodeBlockEvent(
            uuid=uuid, code=code, language=language, code_block_count=code_block_count, recipient=recipient
        )
        assert isinstance(actual, ExecuteCodeBlockEvent)

        expected_model_dump = {
            "type": "execute_code_block",
            "content": {
                "uuid": uuid,
                "code": code,
                "language": language,
                "code_block_count": code_block_count,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        expected_call_args_list = [
            call("\x1b[31m\n>>>>>>>> EXECUTING CODE BLOCK 0 (inferred language is python)...\x1b[0m", flush=True)
        ]

        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self, uuid: UUID, sender: ConversableAgent, recipient: ConversableAgent
    ) -> None:
        code = """print("hello world")"""
        language = "python"
        code_block_count = 0

        actual = ExecuteCodeBlockEvent(
            uuid=uuid, code=code, language=language, code_block_count=code_block_count, recipient=recipient
        )
        assert isinstance(actual, ExecuteCodeBlockEvent)

        expected_model_dump = {
            "type": "execute_code_block",
            "content": {
                "uuid": uuid,
                "code": code,
                "language": language,
                "code_block_count": code_block_count,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestExecuteFunctionEvent:
    def test_print(self, uuid: UUID, recipient: ConversableAgent) -> None:
        func_name = "add_num"
        call_id = "call_12345xyz"
        arguments = {"num_to_be_added": 5}

        actual = ExecuteFunctionEvent(
            uuid=uuid, func_name=func_name, call_id=call_id, arguments=arguments, recipient=recipient
        )
        assert isinstance(actual, ExecuteFunctionEvent)

        expected_model_dump = {
            "type": "execute_function",
            "content": {
                "uuid": uuid,
                "func_name": func_name,
                "call_id": call_id,
                "arguments": arguments,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [
            call(
                "\x1b[35m\n>>>>>>>> EXECUTING FUNCTION add_num...\nCall ID: call_12345xyz\nInput arguments: {'num_to_be_added': 5}\x1b[0m",
                flush=True,
            )
        ]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID, recipient: ConversableAgent) -> None:
        func_name = "add_num"
        call_id = "call_12345xyz"
        arguments = {"num_to_be_added": 5}

        actual = ExecuteFunctionEvent(
            uuid=uuid, func_name=func_name, call_id=call_id, arguments=arguments, recipient=recipient
        )
        assert isinstance(actual, ExecuteFunctionEvent)

        expected_model_dump = {
            "type": "execute_function",
            "content": {
                "uuid": uuid,
                "func_name": func_name,
                "call_id": call_id,
                "arguments": arguments,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestExecutedFunctionEvent:
    def test_print(self, uuid: UUID, recipient: ConversableAgent) -> None:
        func_name = "add_num"
        call_id = "call_12345xyz"
        arguments = {"num_to_be_added": 5}
        content = "15"

        actual = ExecutedFunctionEvent(
            uuid=uuid, func_name=func_name, call_id=call_id, arguments=arguments, content=content, recipient=recipient
        )
        assert isinstance(actual, ExecutedFunctionEvent)

        expected_model_dump = {
            "type": "executed_function",
            "content": {
                "uuid": uuid,
                "func_name": func_name,
                "is_exec_success": True,
                "call_id": call_id,
                "arguments": arguments,
                "content": content,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [
            call(
                "\x1b[35m\n>>>>>>>> EXECUTED FUNCTION add_num...\nCall ID: call_12345xyz\nInput arguments: {'num_to_be_added': 5}\nOutput:\n15\x1b[0m",
                flush=True,
            )
        ]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID, recipient: ConversableAgent) -> None:
        func_name = "add_num"
        call_id = "call_12345xyz"
        arguments = {"num_to_be_added": 5}
        content = "15"

        actual = ExecutedFunctionEvent(
            uuid=uuid, func_name=func_name, call_id=call_id, arguments=arguments, content=content, recipient=recipient
        )
        assert isinstance(actual, ExecutedFunctionEvent)

        expected_model_dump = {
            "type": "executed_function",
            "content": {
                "uuid": uuid,
                "func_name": func_name,
                "is_exec_success": True,
                "call_id": call_id,
                "arguments": arguments,
                "content": content,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestSelectSpeakerEvent:
    agents = [
        ConversableAgent("bob", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"),
        ConversableAgent("charlie", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"),
    ]
    expected_model_dump = {
        "type": "select_speaker",
        "content": {
            "agents": ["bob", "charlie"],
        },
    }

    def test_print(self, uuid: UUID) -> None:
        actual = SelectSpeakerEvent(uuid=uuid, agents=self.agents)  # type: ignore [arg-type]
        assert isinstance(actual, SelectSpeakerEvent)

        self.expected_model_dump["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [
            call("Please select the next speaker from the following list:"),
            call("1: bob"),
            call("2: charlie"),
        ]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        actual = SelectSpeakerEvent(uuid=uuid, agents=self.agents)
        assert isinstance(actual, SelectSpeakerEvent)
        self.expected_model_dump["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected_model_dump
        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestSelectSpeakerTryCountExceededEvent:
    agents = [
        ConversableAgent("bob", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"),
        ConversableAgent("charlie", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"),
    ]

    def test_print(self, uuid: UUID) -> None:
        try_count = 3

        actual = SelectSpeakerTryCountExceededEvent(uuid=uuid, try_count=try_count, agents=self.agents)  # type: ignore [arg-type]
        assert isinstance(actual, SelectSpeakerTryCountExceededEvent)

        expected_model_dump = {
            "type": "select_speaker_try_count_exceeded",
            "content": {
                "uuid": uuid,
                "try_count": try_count,
                "agents": ["bob", "charlie"],
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [call("You have tried 3 times. The next speaker will be selected automatically.")]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        try_count = 3

        actual = SelectSpeakerTryCountExceededEvent(uuid=uuid, try_count=try_count, agents=self.agents)
        assert isinstance(actual, SelectSpeakerTryCountExceededEvent)
        expected_model_dump = {
            "type": "select_speaker_try_count_exceeded",
            "content": {
                "uuid": uuid,
                "try_count": try_count,
                "agents": ["bob", "charlie"],
            },
        }
        assert actual.model_dump() == expected_model_dump
        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestSelectSpeakerInvalidInputEvent:
    agents = [
        ConversableAgent("bob", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"),
        ConversableAgent("charlie", max_consecutive_auto_reply=0, llm_config=False, human_input_mode="NEVER"),
    ]
    expected_model_dump = {
        "type": "select_speaker_invalid_input",
        "content": {
            "agents": ["bob", "charlie"],
        },
    }

    def test_print(self, uuid: UUID) -> None:
        actual = SelectSpeakerInvalidInputEvent(uuid=uuid, agents=self.agents)  # type: ignore [arg-type]
        assert isinstance(actual, SelectSpeakerInvalidInputEvent)

        self.expected_model_dump["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [call("Invalid input. Please enter a number between 1 and 2.")]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID) -> None:
        actual = SelectSpeakerInvalidInputEvent(uuid=uuid, agents=self.agents)
        assert isinstance(actual, SelectSpeakerInvalidInputEvent)
        self.expected_model_dump["content"]["uuid"] = uuid
        assert actual.model_dump() == self.expected_model_dump
        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestClearConversableAgentHistoryEvent:
    def test_print(self, uuid: UUID, recipient: ConversableAgent) -> None:
        no_events_preserved = 5

        actual = ClearConversableAgentHistoryEvent(uuid=uuid, agent=recipient, no_events_preserved=no_events_preserved)
        assert isinstance(actual, ClearConversableAgentHistoryEvent)

        expected_model_dump = {
            "type": "clear_conversable_agent_history",
            "content": {
                "uuid": uuid,
                "agent": "recipient",
                "no_events_preserved": no_events_preserved,
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [
            call("Preserving one more event for recipient to not divide history between tool call and tool response."),
            call("Preserving one more event for recipient to not divide history between tool call and tool response."),
            call("Preserving one more event for recipient to not divide history between tool call and tool response."),
            call("Preserving one more event for recipient to not divide history between tool call and tool response."),
            call("Preserving one more event for recipient to not divide history between tool call and tool response."),
        ]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID, recipient: ConversableAgent) -> None:
        no_events_preserved = 5

        actual = ClearConversableAgentHistoryEvent(uuid=uuid, agent=recipient, no_events_preserved=no_events_preserved)
        assert isinstance(actual, ClearConversableAgentHistoryEvent)

        expected_model_dump = {
            "type": "clear_conversable_agent_history",
            "content": {
                "uuid": uuid,
                "agent": "recipient",
                "no_events_preserved": no_events_preserved,
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestClearConversableAgentHistoryWarningEvent:
    def test_print(self, uuid: UUID, recipient: ConversableAgent) -> None:
        actual = ClearConversableAgentHistoryWarningEvent(uuid=uuid, recipient=recipient)
        assert isinstance(actual, ClearConversableAgentHistoryWarningEvent)

        expected_model_dump = {
            "type": "clear_conversable_agent_history_warning",
            "content": {
                "uuid": uuid,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)
        # print(mock.call_args_list)
        expected_call_args_list = [
            call(
                "\x1b[33mWARNING: `nr_preserved_events` is ignored when clearing chat history with a specific agent.\x1b[0m",
                flush=True,
            )
        ]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(self, uuid: UUID, recipient: ConversableAgent) -> None:
        actual = ClearConversableAgentHistoryWarningEvent(uuid=uuid, recipient=recipient)
        assert isinstance(actual, ClearConversableAgentHistoryWarningEvent)

        expected_model_dump = {
            "type": "clear_conversable_agent_history_warning",
            "content": {
                "uuid": uuid,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestGenerateCodeExecutionReplyEvent:
    @pytest.mark.parametrize(
        "code_blocks, expected",
        [
            (
                [
                    CodeBlock(code="print('hello world')", language="python"),
                ],
                [call("\x1b[31m\n>>>>>>>> EXECUTING CODE BLOCK (inferred language is python)...\x1b[0m", flush=True)],
            ),
            (
                [
                    CodeBlock(code="print('hello world')", language="python"),
                    CodeBlock(code="print('goodbye world')", language="python"),
                ],
                [
                    call(
                        "\x1b[31m\n>>>>>>>> EXECUTING 2 CODE BLOCKS (inferred languages are [python, python])...\x1b[0m",
                        flush=True,
                    )
                ],
            ),
        ],
    )
    def test_print(
        self,
        code_blocks: list[CodeBlock],
        expected: list[_Call],
        uuid: UUID,
        sender: ConversableAgent,
        recipient: ConversableAgent,
    ) -> None:
        actual = GenerateCodeExecutionReplyEvent(uuid=uuid, code_blocks=code_blocks, sender=sender, recipient=recipient)
        assert isinstance(actual, GenerateCodeExecutionReplyEvent)

        expected_model_dump = {
            "type": "generate_code_execution_reply",
            "content": {
                "uuid": uuid,
                "code_blocks": [x.language for x in code_blocks],
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)

        assert mock.call_args_list == expected

    def test_serialization_and_deserialization(
        self,
        uuid: UUID,
        sender: ConversableAgent,
        recipient: ConversableAgent,
    ) -> None:
        code_blocks = [
            CodeBlock(code="print('hello world')", language="python"),
            CodeBlock(code="print('goodbye world')", language="python"),
        ]

        actual = GenerateCodeExecutionReplyEvent(uuid=uuid, code_blocks=code_blocks, sender=sender, recipient=recipient)
        assert isinstance(actual, GenerateCodeExecutionReplyEvent)

        expected_model_dump = {
            "type": "generate_code_execution_reply",
            "content": {
                "uuid": uuid,
                "code_blocks": [x.language for x in code_blocks],
                "sender": "sender",
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestConversableAgentUsageSummaryNoCostIncurredEvent:
    def test_print(
        self,
        uuid: UUID,
        recipient: ConversableAgent,
    ) -> None:
        actual = ConversableAgentUsageSummaryNoCostIncurredEvent(uuid=uuid, recipient=recipient)
        assert isinstance(actual, ConversableAgentUsageSummaryNoCostIncurredEvent)

        expected_model_dump = {
            "type": "conversable_agent_usage_summary_no_cost_incurred",
            "content": {
                "uuid": uuid,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)
        expected_call_args_list = [call("No cost incurred from agent 'recipient'.")]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self,
        uuid: UUID,
        recipient: ConversableAgent,
    ) -> None:
        actual = ConversableAgentUsageSummaryNoCostIncurredEvent(uuid=uuid, recipient=recipient)
        assert isinstance(actual, ConversableAgentUsageSummaryNoCostIncurredEvent)

        expected_model_dump = {
            "type": "conversable_agent_usage_summary_no_cost_incurred",
            "content": {
                "uuid": uuid,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestConversableAgentUsageSummaryEvent:
    def test_print(
        self,
        uuid: UUID,
        recipient: ConversableAgent,
    ) -> None:
        actual = ConversableAgentUsageSummaryEvent(uuid=uuid, recipient=recipient)
        assert isinstance(actual, ConversableAgentUsageSummaryEvent)

        expected_model_dump = {
            "type": "conversable_agent_usage_summary",
            "content": {
                "uuid": uuid,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        mock = MagicMock()
        actual.print(f=mock)

        # print(mock.call_args_list)
        expected_call_args_list = [call("Agent 'recipient':")]
        assert mock.call_args_list == expected_call_args_list

    def test_serialization_and_deserialization(
        self,
        uuid: UUID,
        recipient: ConversableAgent,
    ) -> None:
        actual = ConversableAgentUsageSummaryEvent(uuid=uuid, recipient=recipient)
        assert isinstance(actual, ConversableAgentUsageSummaryEvent)

        expected_model_dump = {
            "type": "conversable_agent_usage_summary",
            "content": {
                "uuid": uuid,
                "recipient": "recipient",
            },
        }
        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)


class TestRunCompletionEvent:
    def test_serialization_and_deserialization(
        self,
        uuid: UUID,
        recipient: ConversableAgent,
    ) -> None:
        actual = RunCompletionEvent(
            uuid=uuid,
            summary="some summary",
            history=[],
            cost={"cost": 0.0},
            last_speaker="assistant",
            context_variables=ContextVariables(data={"context_var_1": "value_1"}),
        )
        assert isinstance(actual, RunCompletionEvent)

        expected_model_dump = {
            "type": "run_completion",
            "content": {
                "uuid": uuid,
                "summary": "some summary",
                "history": [],
                "cost": {"cost": 0.0},
                "last_speaker": "assistant",
                "context_variables": {"data": {"context_var_1": "value_1"}},
            },
        }

        assert actual.model_dump() == expected_model_dump

        # Test serialization
        d = actual.model_dump()
        assert actual == EVENT_CLASSES[d["type"]].model_validate(d)
