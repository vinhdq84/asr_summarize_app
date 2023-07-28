## This app is for testing the abilities of LLama 2 and Whisper

### How to use

This works as follows:

- Click `Listen` to start real-time speech recognizing. The results will be printed out one after another.
- Afterward, click `Summarize` to stop recogizing and start summarizing the listened content, this may take a while.

Demo video:

https://github.com/vinhdq84/asr_summarize_app/assets/133619903/d18e4caf-07de-4e14-9d8a-20a0db079ef7

### Installation using Conda

Create new conda environment with python version 3.8.10

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

Run the app

```console
python app.py
```
