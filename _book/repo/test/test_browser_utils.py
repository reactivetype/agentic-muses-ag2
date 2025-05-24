# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Portions derived from  https://github.com/microsoft/autogen are under the MIT License.
# SPDX-License-Identifier: MIT
# !/usr/bin/env python3 -m pytest

import hashlib
import math
import os
import re
from tempfile import TemporaryDirectory

import pytest
import requests

from autogen.browser_utils import SimpleTextBrowser
from autogen.import_utils import optional_import_block, skip_on_missing_imports

BLOG_POST_URL = "https://docs.ag2.ai/latest/docs/blog/2023/04/21/LLM-tuning-math/"
BLOG_POST_TITLE = "Does Model and Inference Parameter Matter in LLM Applications? - A Case Study for MATH - AG2"
BLOG_POST_STRING = "Large language models (LLMs) are powerful tools that can generate natural language texts for various applications, such as chatbots, summarization, translation, and more. GPT-4 is currently the state of the art LLM in the world. Is model selection irrelevant? What about inference parameters?"

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Microsoft"
WIKIPEDIA_TITLE = "Microsoft - Wikipedia"
WIKIPEDIA_STRING = "Redmond"

PLAIN_TEXT_URL = "https://raw.githubusercontent.com/ag2ai/ag2/main/README.md"
IMAGE_URL = "https://github.com/afourney.png"

PDF_URL = "https://arxiv.org/pdf/2308.08155.pdf"
PDF_STRING = "Figure 1: AutoGen enables diverse LLM-based applications using multi-agent conversations."

BING_QUERY = "Microsoft"
BING_TITLE = f"{BING_QUERY} - Search"
BING_STRING = f"A Bing search for '{BING_QUERY}' found"


with optional_import_block() as result:
    import requests


try:
    BING_API_KEY = os.environ["BING_API_KEY"]
except KeyError:
    skip_bing = True
else:
    skip_bing = False


# def _rm_folder(path):
#     """Remove all the regular files in a folder, then deletes the folder. Assumes a flat file structure, with no subdirectories."""
#     for fname in os.listdir(path):
#         fpath = os.path.join(path, fname)
#         if os.path.isfile(fpath):
#             os.unlink(fpath)
#     os.rmdir(path)


@pytest.fixture
def downloads_folder():
    with TemporaryDirectory() as downloads_folder:
        yield downloads_folder


@skip_on_missing_imports(["markdownify", "pathvalidate", "requests", "bs4"], "websurfer")
def test_simple_text_browser(downloads_folder: str):
    # Instantiate the browser
    user_agent = "python-requests/" + requests.__version__
    viewport_size = 1024
    browser = SimpleTextBrowser(
        downloads_folder=downloads_folder,
        viewport_size=viewport_size,
        request_kwargs={
            "headers": {"User-Agent": user_agent},
        },
    )

    # Test that we can visit a page and find what we expect there
    top_viewport = browser.visit_page(BLOG_POST_URL)
    assert browser.viewport == top_viewport
    assert browser.page_title.strip() == BLOG_POST_TITLE.strip()
    assert BLOG_POST_STRING in browser.page_content.replace("\n\n", " ").replace("\\", "")

    # Check if page splitting works
    approx_pages = math.ceil(len(browser.page_content) / viewport_size)  # May be fewer, since it aligns to word breaks
    assert len(browser.viewport_pages) <= approx_pages
    assert abs(len(browser.viewport_pages) - approx_pages) <= 1  # allow only a small deviation
    assert browser.viewport_pages[0][0] == 0
    assert browser.viewport_pages[-1][1] == len(browser.page_content)

    # Make sure we can reconstruct the full contents from the split pages
    buffer = ""
    for bounds in browser.viewport_pages:
        buffer += browser.page_content[bounds[0] : bounds[1]]
    assert buffer == browser.page_content

    # Test scrolling (scroll all the way to the bottom)
    for i in range(1, len(browser.viewport_pages)):
        browser.page_down()
        assert browser.viewport_current_page == i
    # Test scrolloing beyond the limits
    for i in range(0, 5):
        browser.page_down()
        assert browser.viewport_current_page == len(browser.viewport_pages) - 1

    # Test scrolling (scroll all the way to the bottom)
    for i in range(len(browser.viewport_pages) - 2, 0, -1):
        browser.page_up()
        assert browser.viewport_current_page == i
    # Test scrolloing beyond the limits
    for i in range(0, 5):
        browser.page_up()
        assert browser.viewport_current_page == 0

    # Test Wikipedia handling
    assert WIKIPEDIA_STRING in browser.visit_page(WIKIPEDIA_URL)
    assert WIKIPEDIA_TITLE.strip() == browser.page_title.strip()

    # Visit a plain-text file
    response = requests.get(PLAIN_TEXT_URL)
    response.raise_for_status()
    expected_results = response.text

    browser.visit_page(PLAIN_TEXT_URL)
    assert browser.page_content.strip() == expected_results.strip()

    # Directly download an image, and compute its md5
    response = requests.get(IMAGE_URL, stream=True)
    response.raise_for_status()
    expected_md5 = hashlib.md5(response.raw.read()).hexdigest()

    # Visit an image causing it to be downloaded by the SimpleTextBrowser, then compute its md5
    viewport = browser.visit_page(IMAGE_URL)
    m = re.search(r"Downloaded '(.*?)' to '(.*?)'", viewport)
    fetched_url = m.group(1)
    download_loc = m.group(2)
    assert fetched_url == IMAGE_URL

    with open(download_loc, "rb") as fh:
        downloaded_md5 = hashlib.md5(fh.read()).hexdigest()

    # MD%s should match
    assert expected_md5 == downloaded_md5

    # Fetch a PDF
    viewport = browser.visit_page(PDF_URL)
    assert PDF_STRING in viewport


@pytest.mark.skipif(
    skip_bing,
    reason="do not run bing tests if key is missing",
)
@skip_on_missing_imports(["markdownify", "pathvalidate", "requests", "bs4"], "websurfer")
def test_bing_search():
    # Instantiate the browser
    user_agent = "python-requests/" + requests.__version__
    browser = SimpleTextBrowser(
        bing_api_key=BING_API_KEY,
        viewport_size=1024,
        request_kwargs={
            "headers": {"User-Agent": user_agent},
        },
    )

    assert BING_STRING in browser.visit_page("bing: " + BING_QUERY)
    assert browser.page_title == BING_TITLE
    assert len(browser.viewport_pages) == 1
    assert browser.viewport_pages[0] == (0, len(browser.page_content))


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_simple_text_browser()
    test_bing_search()
