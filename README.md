
# Custom Chatbot Generator 👽

This Flask application will generate a chatbot for the user depending on the specifications and data that they put in. The project leverages popular AI tools such as Langchain, Chroma vector database, and the OpenAI API. The custom chatbot utilizes RAG (retrieval augmented generation) to use the users uploaded files as knowedge for the chtatbot. 

Use cases of this would include recreational, internal knowledge bots, and legal analysis. 


## Deployment 🚀 

To deploy this project, create a .env file with the following variables:

* OPENAI_API_KEY : This is your API key retrieved from OpenAI 
* UPLOAD_FOLDER : This is a local directory path where the users uploaded files will be temporarily stored

Then, run the following commands:

```bash
  python3 -m venv venv
```
```bash
  source venv/bin/activate
```
```bash
  pip install -r requirements.txt
```
```bash
  python3 app.py
```
## Tech Stack 💻

**Framework** - Flask

**Libraries** - Langchain, OpenAI, Chroma

## Authors 👩

- [@garnere1](https://www.github.com/garnere1)

