# Content formatting for images

## Overview

Content formatting for images refers to the structured representation and processing of visual data within multimodal systems, particularly when working with Large Language Models (LLMs) that support vision capabilities. This involves integrating images with text (such as captions, descriptions, and metadata), handling image inputs and outputs, and ensuring that agents can understand, generate, and utilize images effectively within their workflows.

## Explanation

When working with multimodal agents, images are treated as first-class content types alongside text and other modalities. Effective content formatting allows these agents to:

- **Accept images as input**: Users or other systems can provide images for analysis, captioning, or further processing.
- **Generate images as output**: Agents can create images using generative models and return them in a structured format.
- **Associate metadata**: Images are often accompanied by captions, annotations, or detailed descriptions to provide context and enhance understanding.
- **Format multimodal messages**: Agents must deliver responses that combine text and images in a coherent, structured way—often using standardized formats such as JSON objects, Markdown, or HTML.

### Example Scenarios

- **Image Captioning**: An agent receives an image and returns a descriptive caption in structured output.
- **Image Generation**: Given a text prompt, the agent generates an image and returns both the image and an accompanying caption.
- **Multimodal Tool Use**: Agents invoke tools that process images, such as OCR, object detection, or image editing, and return results in a unified format.

## Examples

### 1. Image Input with Structured Output

```json
{
  "input_type": "image",
  "image_url": "https://example.com/cat.jpg",
  "tasks": ["caption"]
}
```

**Agent Output:**

```json
{
  "image_url": "https://example.com/cat.jpg",
  "caption": "A fluffy gray cat sitting on a windowsill, looking outside."
}
```

### 2. Generating Images with Captions

Suppose you use a tool-calling LLM to generate an image from a prompt:

```json
{
  "tool": "image_generation",
  "parameters": {
    "prompt": "A futuristic cityscape at sunset"
  }
}
```

**Agent Output:**

```json
{
  "generated_image_url": "https://generated.example.com/cityscape.png",
  "caption": "A vibrant futuristic city with tall skyscrapers and flying vehicles at sunset."
}
```

### 3. Multimodal Markdown Formatting

Agents can present images alongside text in Markdown:

```markdown
![A futuristic city at sunset](https://generated.example.com/cityscape.png)

A vibrant futuristic city with tall skyscrapers and flying vehicles at sunset.
```

### 4. Tool Call Output with Multimodal Content

```json
{
  "tool_call": "object_detection",
  "input_image": "https://example.com/street.jpg",
  "output": {
    "objects": [
      {"label": "car", "bounding_box": [100, 200, 300, 400]},
      {"label": "bicycle", "bounding_box": [350, 220, 400, 290]}
    ],
    "image_with_annotations": "https://example.com/street_annotated.jpg"
  }
}
```

## Best Practices

- **Use Structured Formats**: Always return images with structured metadata (e.g., captions, context) in JSON or Markdown for clarity and machine-readability.
- **Link Images Clearly**: Use URLs or data URIs for images, and include alt text or captions for accessibility.
- **Keep Modalities Synchronized**: Ensure that image outputs are logically paired with corresponding textual content.
- **Handle Errors Gracefully**: If an image is missing or cannot be processed, return a clear error message or fallback text.
- **Maintain Consistency**: Use consistent field names (e.g., `image_url`, `caption`) across outputs for easier parsing and downstream processing.
- **Respect Privacy and Copyright**: Only process and display images that are authorized for use; include attribution where required.

## Related Concepts

- [Structured Outputs and Tool Calling with LLMs](./structured-outputs-tool-calling.md)
- [Image Captioning](https://en.wikipedia.org/wiki/Image_captioning)
- [Multimodal Learning](https://en.wikipedia.org/wiki/Multimodal_learning)
- [Markdown Image Syntax](https://www.markdownguide.org/basic-syntax/#images-1)
- [Vision Capabilities in LLMs](./vision-capabilities.md)
- [Agent Design Patterns for Multimodal Systems](./agent-design-multimodal.md)

---

By following these guidelines, you can efficiently integrate and format images within multimodal agent systems, enabling more powerful and user-friendly applications that leverage both vision and language capabilities.