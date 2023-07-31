## This app is for testing the abilities of LLama 2 and Whisper

### Installation using Conda

Create a new conda environment with python version 3.8.10

```console
conda create -n asr_summarize_app python=3.8.10
```

Activate the newly created environment

```console
conda activate asr_summarize_app
```

On Ubuntu, you must have `python3-dev` and `portaudio19-dev` installed first.

```console
sudo apt install python3-dev portaudio19-dev
```

Install the python dependencies

```console
pip install -r requirements.txt
```

Download the `.ggml` models from [here](https://drive.google.com/drive/folders/1K8aeax8GKqfXGQAwJZscDRzUszK0CS15?usp=drive_link) and make sure your directory structure looks like this (use `tree` command):

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

This app works as follows:

- Click `Listen` to start real-time speech recognizing. The results will be printed out one after another.
- Afterward, click `Summarize` to stop recogizing and start summarizing the listened content, this may take a while.

Demo video:

https://github.com/vinhdq84/asr_summarize_app/assets/133619903/d18e4caf-07de-4e14-9d8a-20a0db079ef7
