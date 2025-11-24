"""Model abstraction layer for AI CareFlow.

This module defines light-weight wrappers around one or more model
providers (e.g., OpenAI). The goal is to keep the rest of the
application agnostic to provider-specific details.
"""

from typing import Any, Dict, List

import base64
from io import BytesIO

from openai import OpenAI


class OpenAIChatModelClient:
    """Wrapper around the OpenAI chat completions API.

    The client exposes a small, provider-agnostic interface via the
    :meth:`generate` method so that the rest of the application does
    not depend directly on the OpenAI SDK.
    """

    def __init__(self, model_name: str) -> None:
        """Create a new client wrapper.

        Parameters
        ----------
        model_name:
            Identifier of the underlying chat model (e.g., ``"gpt-4o-mini"``).
        """
        self.model_name = model_name
        # The OpenAI client will read the API key from environment
        # variables such as ``OPENAI_API_KEY``.
        self._client = OpenAI()

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """Generate a chat completion and return the raw content string.

        Parameters
        ----------
        messages:
            A list of OpenAI-style chat messages, each with ``role`` and
            ``content`` keys.

        Returns
        -------
        str
            The raw content of the first choice from the model.
        """
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )

        content = response.choices[0].message.content
        # Defensive: ensure we always return a string.
        return content if isinstance(content, str) else str(content)


def get_default_model_client() -> OpenAIChatModelClient:
    """Return a default model client instance.

    The default model name can be adjusted in :mod:`app.config.settings`.
    """
    return OpenAIChatModelClient(model_name="gpt-4o-mini")


class VisionModelClient:
    """Client wrapper for OpenAI Vision / OCR use cases.

    This client is restricted to text extraction only. It uses a fixed
    system prompt that instructs the model to behave like an OCR engine
    and return only raw text, with no interpretation or clinical
    reasoning.
    """

    def __init__(self, model_name: str = "gpt-4o-mini") -> None:
        self.model_name = model_name
        self._client = OpenAI()

    def _to_data_url(self, image_bytes: bytes) -> str:
        """Encode image bytes as a data URL suitable for the Vision API."""

        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    def extract_text(self, image: BytesIO | bytes) -> str:
        """Extract raw text from an image using an OpenAI vision model.

        Parameters
        ----------
        image:
            Image content as ``bytes`` or a ``BytesIO``-like object.
        """

        if isinstance(image, BytesIO):
            image_bytes = image.getvalue()
        else:
            image_bytes = image

        data_url = self._to_data_url(image_bytes)

        system_prompt = (
            "You are an OCR engine. Extract ALL readable text from the image. "
            "Do NOT interpret, summarize, or add any explanations. "
            "Return only the raw extracted text."
        )

        # Using the Responses API for multimodal input
        response = self._client.responses.create(
            model=self.model_name,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": data_url,
                        }
                    ],
                },
            ],
        )

        # Extract the first text output from the response
        try:
            output = response.output
            if output and output[0].content and output[0].content[0].type == "output_text":
                text = output[0].content[0].text
            else:
                text = ""
        except Exception:
            text = ""

        return text if isinstance(text, str) else str(text)
