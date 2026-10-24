---
title: "Still: bedtime stories without another subscription"
published: false
tags: [devchallenge, opensource, ai, python]
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19).*

## What I Built

Still is a small bedtime-story app for people who would rather read something quiet than spend another half hour choosing what to read.

Pick a woodland cottage, a seaside village, a night train, or a quiet bookshop. Choose a mood and an approximate reading length. Add a detail if you want: a sleepy cat, a familiar name, the smell of bread. Still asks a local model to write the story and saves it to a little library.

The reader has larger-text controls and a plain-text download. There are no accounts, streaks, recommendations, or next-story countdowns. Closing the app is a perfectly good outcome.

## Demo

Run the project with `python server.py` and open `http://localhost:3000`.

The included sample lets you try the reader without installing a model. It is labeled as a prewritten sample. New stories require Ollama and the downloaded model; the sample is not a pretend generation result.

For a short walkthrough:

1. Open the sample and increase the text size.
2. Connect Ollama and choose a setting, mood, and length.
3. Add a small detail and create a story.
4. Return to the library, reopen the story, and download it.

<!-- Before publishing: add your permanent deployed demo URL or upload/embed a recording of the local walkthrough. A local URL is not a publicly accessible demo. Upload docs/still-desktop.png through DEV's image uploader if you want a screenshot here. -->

## Code

The project contains a Python server, a plain HTML/CSS/JavaScript interface, tests, setup instructions, and an MIT license. There is no frontend build step and no Python package installation.

<!-- Before publishing: add the public repository URL here. No repository has been published as part of this workspace build. -->

## How I Built It

The core is **Qwen2.5 1.5B Instruct**, an open-weight model served through **Ollama**. Still calls Ollama's `/api/generate` endpoint with a prompt assembled from the selected setting, mood, reading length, and optional detail.

The prompt asks for an unhurried story with concrete sensory details and a quiet ending. It avoids suspense and danger. JSON output separates the title from the story body. The server checks that both are present before saving anything.

Python's standard library handles the HTTP server and SQLite database. The interface uses system fonts and inline SVG illustrations, so there are no external assets to fetch at bedtime. Generated text is inserted as text rather than interpreted as HTML.

The default model is deliberately small. A bedtime app should not demand an expensive GPU before it can be useful. The model is configurable through `STILL_MODEL`, so a machine with more memory can use a larger one without changing the reader or storage code. Generation speed and writing quality will vary with the model and hardware.

There is also a connection check and a setup guide in the app. If Ollama is missing, Still says so. It does not silently send the request to a hosted provider.

Five backend tests pass, including the generation/save/delete flow using a mocked model response and the main error paths. Desktop and mobile browser smoke tests also pass. Real Qwen inference was not run in the build workspace because Ollama was not installed; local inference and offline operation still need a hardware verification run before claiming measured results.

## Why Does Open Innovation Matter?

The personal detail field is small, but it can be personal. A name, a place, or a familiar routine should not have to become part of a third-party API request just to get a bedtime story.

With Still and Ollama running on the same laptop, that detail stays on the laptop. The model download needs internet once; subsequent generation is designed to work without it. The saved shelf works without a running model, too.

A closed API could write these stories. It would not give this version of the project its defining property: no hosted inference dependency. There is no API key to renew, no per-story inference bill, and no provider account required. That does not make inference literally free; the computer and electricity still count.

Open weights also leave room to change the project. The prompt is a function in the server, not a hidden product setting. The model can be swapped. The interface can be simplified further. Qwen2.5 1.5B Instruct's model card lists Apache-2.0 licensing; Ollama and this app use MIT licenses. The pieces can be inspected rather than taken on trust.

There is one important boundary: local means local to the server. Hosting Still on someone else's machine moves prompts and saved stories to that machine. The private version is the one you run yourself. The README makes that distinction explicit.

For this theme, I wanted the automation to do something modest: remove the choosing, searching, and scrolling between deciding to wind down and actually doing it. A short story is enough.
