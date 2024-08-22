# webUI-for-LLM

The purpose here is to build a simple web UI for conversing with LLM of your choice. This
is the first step to build a more sophisticated chatbot, and the aim here it to explore
and understand the capabilities of models that have their APIs available for free.

To run this, update the [authorisation_file](https://github.com/mriya98/webUI-for-LLM/blob/main/authorisation_file.py) with your access token and the API URL from
Hugging Face.

Install the requirements by running the following on your terminal:

```bash
pip install -r requirements.txt
```

Run the main.py script to launch the web UI locally:
```bash
python main.py
```

The quality of conversation depends on the model being used for inference. Smaller models
can be loaded quickly but the responses tend to be incoherent. Large models like flan-t5-xxl
are too large to load.
