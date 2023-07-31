## This app is for testing the abilities of LLama 2 and Whisper

### Installation

#### Install Conda

Conda is some kind of python package manager. It helps you set up an isolated python environment (so that you don't mess other apps' environment up). You may want to use Miniconda for simpler installation.

Download the Minconda installer from [this link](https://repo.anaconda.com/miniconda/Miniconda3-py38_23.5.2-0-MacOSX-arm64.sh). In terminal, change directory to where the installer located, run the command below:

```console
bash Miniconda3-py38_23.5.2-0-MacOSX-arm64.sh
```

Follow the instructions to finish installation. Then close and re-open the terminal, type `conda --version`, the result should be `conda 23.5.2`.

#### Environment setup

Create new conda environment with Python version `3.8.10`

```console
conda create -n asr_summarize_app python=3.8.10
```

Activate the newly created environment

```console
conda activate asr_summarize_app
```

Clone this repository using

```console
git clone https://github.com/vinhdq84/asr_summarize_app.git
```

In your terminal, type

```console
cd asr_summarize_app/
```

Install `portaudio` through `brew`

```console
brew install portaudio
```

Install the python dependencies

```console
pip install -r requirements.txt
```

Download the `.ggml` models from [here](https://drive.google.com/drive/folders/1K8aeax8GKqfXGQAwJZscDRzUszK0CS15?usp=drive_link) and extract them to the project directory. Make sure your project directory looks like this (use `tree -la`):

```console
.
├── app.py
├── draft.ipynb
├── .gitignore
├── icons
│   ├── complete.png
│   ├── icon.png
│   ├── spinner2.gif
│   ├── spinner.gif
│   └── start.png
├── Listen and Summarize.spec
├── models
│   ├── llama2
│   │   └── llama-2-13b-chat.ggmlv3.q4_K_M.bin
│   └── whisper
│       └── ggml-tiny.en.bin
├── README-macos.md
├── README.md
└── requirements.txt
```

Run the app

```console
python app.py
```

### How to use

This works as follows:

- Click `Listen` to start real-time speech recognizing. The results will be printed out one after another.
- Afterward, click `Summarize` to stop recogizing and start summarizing the listened content, this may take a while.

Demo video:

https://github.com/vinhdq84/asr_summarize_app/assets/133619903/d18e4caf-07de-4e14-9d8a-20a0db079ef7
