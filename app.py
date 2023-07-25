from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import sys, os
from time import sleep
from llama_cpp import Llama
from whispercpp import Whisper

basedir = os.path.dirname(__file__)


class OpsWorker(QObject):
    def run_loading(self):
        ...

    def run_recognizing(self):
        ...

    def run_summarizing(self):
        ...


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Listen and Summarize")
        self.resize(800, 400)

        global_layout = QVBoxLayout()

        asr_content = QLabel("Asr content dummy")
        asr_content.setMargin(10)

        sum_content = QLabel("Sum content dummy")
        sum_content.setMargin(10)
        
        global_layout.addWidget(asr_content)
        global_layout.addWidget(sum_content)

        button_panel = QHBoxLayout()
        button1 = QPushButton("Listen")
        button1.setIcon(QIcon(os.path.join(basedir, "icons/start.png")))
        button1.pressed.connect(self.lower)
        button_panel.addWidget(button1)

        button2 = QPushButton("Summarize")
        button2.setIcon(QIcon(os.path.join(basedir, "icons/complete.png")))
        button2.pressed.connect(self.close)
        button_panel.addWidget(button2)

        global_layout.addLayout(button_panel)
        container = QWidget()
        container.setLayout(global_layout)

        self.setCentralWidget(container)

        self.show()

    def load_models(self):
        self.llm = Llama(
            model_path=os.path.join(
                basedir, "models/llama2/llama-2-13b-chat.ggmlv3.q4_K_M.bin"
            )
        )
        self.whisper = Whisper.from_pretrained(
            os.path.join(basedir, "models/whisper/ggml-tiny.en.bin")
        )

        content_to_sum = "This man is so fast. Once upon a time I saw him running around in flash time. One day, I found him dead."

    def summarize(self, text: str):
        for i in self.llm(
            prompt=f"### Instruction: Summarize the following, return the summarized text only: {text}\n### Response:",
            stream=True,
        ):
            yield i["choices"][0]["text"]

    def streaming_asr(self):
        for i in self.whisper.stream_transcribe(
            5000, sample_rate=16000, step_ms=2500, n_threads=8
        ):
            yield i


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
