from typing import List, Tuple

import gradio as gr
import numpy as np

from unified_desktop.pipelines import (
    UDIntentClassifier,
    UDKeyExtractor,
    UDSentimentDetector,
    UDSpeechEmotionRecognizer,
    UDSpeechRecognizer,
    UDSummarizer,
)

# Ud_Audio to upload for the demo:
# https://walgreens-my.sharepoint.com/:f:/p/zeinab_takbiri/EpKsj2-WSwFLhApq7pHi1Q0BwDXMT-CizP50h3gpqD6WHA?e=tHr4rc


asrObj = UDSpeechRecognizer(model_id="openai/whisper-base.en")
serObj = UDSpeechEmotionRecognizer()
summarizer = UDSummarizer()
intentObj = UDIntentClassifier()
KeyObj = UDKeyExtractor()


def demo_asr(audio: str) -> str:
    # Transcribe the audio file to text
    return asrObj(audio)


def demo_ser(audio: str) -> str:
    return serObj(audio).label


def demo_intent_detection(text: str) -> List[Tuple[str, float]]:
    # Input text for keywords extraction
    top_k = 3
    intent_results = intentObj(text, top_k)
    list_intent = []
    for item in intent_results:
        list_intent.append((item["label"], np.round(item["score"], 3)))
    return list_intent


def demo_keyword_extraction(text: str) -> str:
    key_results = KeyObj(text)
    return ", ".join(key_results)


def demo_summarization(text: str) -> str:
    summary = summarizer(text)
    return summary


def demo_sentiment_analysis(text: str) -> str:
    sentiment_obj = UDSentimentDetector()
    output_sentiment = sentiment_obj(input_text=text)
    return output_sentiment.sentiment


def NLP_task_processing(
    audio: str,
) -> tuple[str, str, List[Tuple[str, float]], list[str], str, str]:
    asr_result = demo_asr(audio)
    ser_result = demo_ser(audio)
    summary = demo_summarization(asr_result)
    intents = demo_intent_detection(summary)
    keywords = demo_keyword_extraction(asr_result)
    sentiment = demo_sentiment_analysis(asr_result)
    return asr_result, ser_result, intents, keywords, summary, sentiment  # type: ignore


def create_gradio_ui_elements():
    audio_input = gr.Audio(type="filepath", label="Upload an audio file")
    inputs = [audio_input]

    outputs = [
        gr.Textbox(label="ASR Result"),
        gr.Textbox(label="SER Result"),
        gr.Textbox(label="Top 3 Intent Detection"),
        gr.Textbox(label="Keyword Extraction"),
        gr.Textbox(label="Summarization"),
        gr.Textbox(label="Sentiment Analysis"),
    ]
    return inputs, outputs


if __name__ == "__main__":
    inputs, outputs = create_gradio_ui_elements()
    gr.Interface(NLP_task_processing, inputs, outputs).launch()
