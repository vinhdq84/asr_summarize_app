import os
import sys

import numpy as np
import pyaudio
from llama_cpp import Llama
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from whispercpp import Whisper

basedir = os.path.dirname(__file__)


class OpsWorker(QObject):
    finished = pyqtSignal()
    streaming = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._stop_requested = False

    def run_loading(self):
        self.llama = Llama(
            model_path=os.path.join(
                basedir, "models/llama2/llama-2-13b-chat.ggmlv3.q4_K_M.bin"
            )
        )
        self.whisper = Whisper.from_pretrained(
            os.path.join(basedir, "models/whisper/ggml-tiny.en.bin")
        )
        self.text = "He was far from being her friends let alone her lover. She told him to focus on his career, love would chase him. Then the day he succeeded came, but she had already been with another man."
        self.finished.emit()

    def run_recognizing(self):
        self.text = ""
        self._stop_requested = False
        audio = pyaudio.PyAudio()

        self.streaming.emit("=== Listening ===\n")

        sr = 16000
        sample_format = pyaudio.paFloat32
        chunk = 1024
        time_to_record = 3

        stream = audio.open(
            format=sample_format,
            channels=1,
            rate=sr,
            input=True,
            output=False,
            frames_per_buffer=chunk,
        )

        data = []
        while not self._stop_requested:
            data = data[-int(sr * 0.25) // (chunk) :]
            for _ in range(sr // chunk * time_to_record):
                data.append(stream.read(chunk))
            res = self.whisper.transcribe(
                np.frombuffer(b"".join(data), dtype=np.float32)
            )
            self.text += res
            self.streaming.emit(res)

        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.finished.emit()

    def run_summarizing(self):
        titled = False
        for i in self.llama(
            prompt=f"### Instruction: Summarize the following, no longer than the original, return the result only: {self.text}\n### Response:",
            stream=True,
        ):
            if not titled:
                self.streaming.emit("=== Summary ===\n")
                titled = True

            self.streaming.emit(i["choices"][0]["text"])
        self.finished.emit()

    def stop_recognizing(self):
        self._stop_requested = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Listen and Summarize")
        self.resize(800, 600)

        global_layout = QVBoxLayout()

        self.asr_content = QLabel("Asr content dummy")
        self.asr_content.setWordWrap(True)
        self.asr_content.setMaximumWidth(self.width())
        self.asr_content.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.asr_content.setMargin(5)

        self.sum_content = QLabel("Sum content dummy", self)
        self.sum_content.setWordWrap(True)
        self.sum_content.setMaximumWidth(self.width())
        self.sum_content.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.sum_content.setMargin(5)

        self.spinner = QMovie(os.path.join(basedir, "icons/spinner2.gif"))
        
        global_layout.addWidget(self.asr_content)
        global_layout.addWidget(self.sum_content)

        button_panel = QHBoxLayout()
        self.listen_button = QPushButton("Listen")
        self.listen_button.setIcon(QIcon(os.path.join(basedir, "icons/start.png")))
        self.listen_button.clicked.connect(self.recognize)
        button_panel.addWidget(self.listen_button)

        self.summarize_button = QPushButton("Summarize")
        self.summarize_button.setIcon(
            QIcon(os.path.join(basedir, "icons/complete.png"))
        )
        self.summarize_button.clicked.connect(self.stop_recognizing)
        button_panel.addWidget(self.summarize_button)

        global_layout.addLayout(button_panel)
        container = QWidget()
        container.setLayout(global_layout)

        self.setCentralWidget(container)
        self.show()

        self.worker_thread = QThread()
        self.ops_worker = OpsWorker()
        self.ops_worker.moveToThread(self.worker_thread)
        self.load()

    def load(self):
        self._loading_status(True)
        self.worker_thread.started.connect(self.ops_worker.run_loading)
        self.ops_worker.finished.connect(lambda: self._loading_status(False))
        self.ops_worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.start()

    def disconnect(self):
        connections = [
            self.worker_thread.started,
            self.worker_thread.finished,
            self.ops_worker.finished,
            self.ops_worker.streaming,
        ]

        for connection in connections:
            try:
                connection.disconnect()
            except TypeError:
                ...

    def _loading_status(self, toggle=True):
        if toggle:
            self.asr_content.setText("Loading Whisper...")
            self.sum_content.setText("Loading Llama 2...")
            self.listen_button.setEnabled(False)
            self.summarize_button.setEnabled(False)
        else:
            self.asr_content.setText("")
            self.sum_content.setText("")
            self.listen_button.setEnabled(True)
            self.summarize_button.setEnabled(True)

    def recognize(self):
        self.asr_content.setText("")
        self.sum_content.setText("")
        self.disconnect()
        self.listen_button.setEnabled(False)
        self.worker_thread.started.connect(self.ops_worker.run_recognizing)
        self.worker_thread.finished.connect(lambda: self.listen_button.setEnabled(True))
        self.ops_worker.finished.connect(self.worker_thread.quit)
        self.ops_worker.finished.connect(self.summarize)
        self.ops_worker.streaming.connect(self.show_reg_res)
        self.worker_thread.start()

    def stop_recognizing(self):
        if self.worker_thread.isRunning():
            self.summarize_button.setEnabled(False)
            self.sum_content.setMovie(self.spinner)
            self.spinner.start()
            self.ops_worker.stop_recognizing()
  
    def summarize(self):
        self.disconnect()
        self.summarize_button.setEnabled(False)
        self.listen_button.setEnabled(False)
        self.worker_thread.started.connect(self.ops_worker.run_summarizing)
        self.worker_thread.finished.connect(
            lambda: self.summarize_button.setEnabled(True)
        )
        self.worker_thread.finished.connect(lambda: self.listen_button.setEnabled(True))
        self.ops_worker.finished.connect(self.worker_thread.quit)
        self.ops_worker.streaming.connect(self.show_sum_res)
        self.worker_thread.start()

    def show_reg_res(self, res: str):
        self.asr_content.setText(self.asr_content.text() + res)

    def show_sum_res(self, res: str):
        self.sum_content.setText(self.sum_content.text() + res)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()
