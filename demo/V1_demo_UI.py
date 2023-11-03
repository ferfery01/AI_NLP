# import random
# from pprint import pprint
from typing import List, Optional, Tuple, Union

import gradio as gr

# import ipywidgets as widgets
# import pandas as pd
# import torch
# import whisper
# from IPython.display import Audio, clear_output, display
# from transformers import logging

# from unified_desktop import RESOURCES_DIR
# from unified_desktop.core.utils.io_utils import get_matching_files_in_dir
# from unified_desktop.pipelines import (
#     UDIntentClassifier,
#     UDKeyExtraction,
#     UDSentimentDetector,
#     UDSpeechEmotionRecognizer,
#     UDSpeechRecognizer,
#     UDSummarizer,
# )

# For NLP task demonstration purposes


def demo_asr(audio: bytes) -> str:
    return "This is a mock ASR result from the audio."


def demo_ser(audio: bytes) -> str:
    return "Happy"


def demo_intent_detection(text: str) -> str:
    return "Intent: Greeting"


def demo_keyword_extraction(text: str) -> List[str]:
    return ["mock", "keywords"]


def demo_summarization(text: str) -> str:
    return "This is a mock summary of the text."


def demo_sentiment_analysis(text: str) -> str:
    return "Positive"


def NLP_task_processing(
    audio: bytes,
    intent_selected: List[str],
    keyword_selected: List[str],
    summary_selected: List[str],
    sentiment_selected: List[str],
) -> Tuple[str, str, Optional[str], Optional[List[str]], Optional[str], Optional[str]]:
    asr_result = demo_asr(audio)
    ser_result = demo_ser(audio)

    intents = demo_intent_detection(asr_result) if "Intent Detection" in intent_selected else None
    keywords = demo_keyword_extraction(asr_result) if "Keyword Extraction" in keyword_selected else None
    summary = demo_summarization(asr_result) if "Summarization" in summary_selected else None
    sentiment = demo_sentiment_analysis(asr_result) if "Sentiment Analysis" in sentiment_selected else None

    return asr_result, ser_result, intents, keywords, summary, sentiment


def create_gradio_ui_elements() -> (
    Tuple[List[Union[gr.inputs.Audio, gr.inputs.CheckboxGroup]], List[gr.outputs.Textbox]]
):
    audio_input = gr.inputs.Audio(label="Upload an audio file")
    intent_checkbox = gr.inputs.CheckboxGroup(["Intent Detection"], label="Select Tasks")
    keyword_checkbox = gr.inputs.CheckboxGroup(["Keyword Extraction"], label=" ")
    summary_checkbox = gr.inputs.CheckboxGroup(["Summarization"], label=" ")
    sentiment_checkbox = gr.inputs.CheckboxGroup(["Sentiment Analysis"], label=" ")

    inputs = [audio_input, intent_checkbox, keyword_checkbox, summary_checkbox, sentiment_checkbox]

    outputs = [
        gr.outputs.Textbox(label="ASR Result"),
        gr.outputs.Textbox(label="SER Result"),
        gr.outputs.Textbox(label="Intent Detection"),
        gr.outputs.Textbox(label="Keyword Extraction"),
        gr.outputs.Textbox(label="Summarization"),
        gr.outputs.Textbox(label="Sentiment Analysis"),
    ]

    return inputs, outputs


if __name__ == "__main__":
    inputs, outputs = create_gradio_ui_elements()

    gr.Interface(NLP_task_processing, inputs, outputs).launch()
