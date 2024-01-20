## Deploy your personal assistant
![](demo.gif)

## How to run
```shell
# install necessary packages
pip install torch transformers fastapi streamlit uvicorn

# run the model server
uvicorn model-stream:app

# on a new terminal, run the web server
streamlit run web-app.py
```
