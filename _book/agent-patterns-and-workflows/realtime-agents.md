# Realtime Agents


## Quality Check

```yaml
quality_check:
  score: 8
  issues:
    - type: "Accuracy"
      description: "The description of observers and audio adapters is generally correct, but the documentation could clarify how observer registration works (e.g., expected event names, signature of callbacks)."
      severity: "medium"
      suggestion: "Provide explicit details or a link/reference to valid observer event names and callback signatures."
    - type: "Clarity"
      description: "Some terminology (e.g., 'send_and_stream_tokens') is used in code without explanation, and it's unclear if this is part of the documented API."
      severity: "medium"
      suggestion: "Clarify whether 'send_and_stream_tokens' is a public method, and briefly explain its usage or alternatives."
    - type: "Completeness"
      description: "Edge cases like error handling during streaming, or what happens if LLM provider doesn't support streaming, are not addressed."
      severity: "low"
      suggestion: "Add a note on error handling and provider compatibility, or link to more detailed sections."
    - type: "Code Example Quality"
      description: "The code examples do not show full working context (e.g., the UI example does not define 'chatbox', and audio handler is not wired to any event loop or input stream)."
      severity: "medium"
      suggestion: "Provide more complete code snippets or clarify what is assumed to be defined elsewhere."
    - type: "Best Practices"
      description: "Best practices are solid but could benefit from briefly explaining why unregistering observers is important."
      severity: "low"
      suggestion: "Add one sentence explaining the risks of leaving observers registered."
  strengths:
    - "Clear distinction between traditional and realtime agent workflows."
    - "Good coverage of core abstractions (ConversableAgent, Observers, Audio Adapters) and their roles."
    - "Practical, focused code examples that illustrate key concepts."
    - "Best practices section highlights important operational considerations."
  recommendations:
    - "Expand code examples with more context, especially for UI and audio workflows."
    - "Add a troubleshooting or FAQ subsection for common issues with streaming or audio integration."
```



## Content

```yaml
content:
  overview: |
    Realtime agents enable interactive, low-latency agentic workflows by integrating with streaming APIs, live observers, and audio adapters. They allow agents to process input (text or audio) as it arrives, generate partial or incremental responses, and react to events in real time. This is essential for conversational interfaces, live chatbots, voice assistants, and agent-driven streaming applications.

  explanation: |
    Traditional agent workflows process full user messages in batch, waiting for an entire prompt before responding. In contrast, realtime agents leverage streaming APIs (such as OpenAI's streaming endpoints), observer hooks, and audio adapters to handle data as it arrives—enabling responsive, interactive experiences.

    Key abstractions for realtime agents include:

    - **ConversableAgent (and Agent Protocols):** Provides the foundation for sending/receiving messages and registering tools, supporting async and streaming interactions.
    - **Observers:** Components that monitor events (e.g., message received, token generated) and trigger callbacks, enabling real-time updates and UI refreshes.
    - **Audio Adapters:** Interfaces that handle conversion between audio streams and text, supporting speech-to-text (STT) and text-to-speech (TTS) for voice-enabled agents.

    A typical realtime agent workflow involves:
      1. Receiving streaming input (from a user or another agent).
      2. Processing and possibly emitting partial responses as the LLM generates tokens.
      3. Using observers to update UIs or trigger other logic on new data.
      4. Optionally converting audio to text for input, or generating audio output for responses.

    The agent framework supports streaming via model configuration (e.g., `llm_config={"stream": True}`), observer registration, and audio adapter integration, enabling seamless development of conversational and voice-first applications.

  examples:
    - title: "Streaming Chat Response with ConversableAgent"
      description: |
        Create an agent configured for streaming, and register an observer to process tokens as they are generated.
      code: |
        from autogen import ConversableAgent

        def on_token(token, **kwargs):
            print(f"Received token: {token}", end="", flush=True)

        agent = ConversableAgent(
            name="assistant",
            system_message="You are a helpful, streaming AI.",
            llm_config={"model": "gpt-4", "api_key": "...", "stream": True}
        )
        agent.register_observer("on_token", on_token)

        # Initiate a chat; tokens will be printed as they arrive
        agent.initiate_chat(None, message="Tell me a long story.")

    - title: "Realtime Voice Agent with Audio Adapter"
      description: |
        Connect an audio adapter for speech-to-text (STT) and text-to-speech (TTS), enabling voice interactions in real time.
      code: |
        from autogen import ConversableAgent
        from autogen.audio.adapters import WhisperAdapter, ElevenLabsAdapter

        # Configure agent for streaming
        agent = ConversableAgent(
            name="voice_assistant",
            system_message="You are a helpful voice AI.",
            llm_config={"model": "gpt-4", "api_key": "...", "stream": True}
        )

        # Register audio adapters
        agent.register_audio_adapter("stt", WhisperAdapter())
        agent.register_audio_adapter("tts", ElevenLabsAdapter(api_key="..."))

        # This function would be called when new audio arrives
        def on_audio_chunk(audio_chunk):
            text = agent.audio_adapters["stt"].transcribe(audio_chunk)
            # Stream response as audio
            for token in agent.send_and_stream_tokens(text):
                agent.audio_adapters["tts"].play(token)

    - title: "Observer for Realtime UI Updates"
      description: |
        Use observers to update a frontend UI as tokens are generated.
      code: |
        def ui_update(token, **kwargs):
            # Append token to a UI element (e.g., chatbox)
            chatbox.append(token)

        agent.register_observer("on_token", ui_update)
        agent.initiate_chat(None, message="Summarize the news today.")

  best_practices:
    - "Always set `llm_config['stream'] = True` for agents intended for realtime/streaming interactions."
    - "Use observers for side effects (UI updates, logging) instead of modifying agent state directly."
    - "When working with audio adapters, handle errors and silence input gracefully to avoid blocking the main loop."
    - "Keep observer callbacks fast and non-blocking to avoid introducing latency."
    - "Test streaming with both short and long responses to ensure stable token handling."
    - "Explicitly unregister observers when they are no longer needed to prevent memory leaks or redundant callbacks."

  related_concepts:
    - name: "ConversableAgent"
      description: "The base abstraction for all agent communication—supports streaming and observer patterns for realtime operation."
    - name: "Observers"
      description: "Mechanism for triggering callbacks on agent events (e.g., message/token received), enabling realtime updates."
    - name: "Audio Adapters"
      description: "Interfaces for integrating speech-to-text and text-to-speech in agent workflows, essential for voice-based realtime agents."
    - name: "LLMConfig"
      description: "Model configuration object; set `stream=True` to enable realtime streaming from compatible LLM providers."
    - name: "Tool and Toolkit"
      description: "Tools may be used in realtime by agents as part of their streaming or incremental response logic."
    - name: "GroupChatManager"
      description: "Manages multi-agent streaming conversations, coordinating which agent responds in real time."
```
