# How to use Generative Models to Improve Focused Crawling?

**Abstract**  
Focused crawling aims to enhance the efficiency of web crawlers by directing them to gather content specifically related to a particular topic, rather than exhaustively indexing the entire web. In this context, focused crawling can significantly support researchers and students looking to find relevant papers within their field of study. The goal of this paper is to evaluate several techniques that could improve the ability of a focused crawler to retrieve relevant research papers, namely through query expansion using Large Language Models (LLMs) and by employing the HYDE method for similarity calculation.

In order to test these techniques, we designed three distinct use cases, simulating the information-seeking behavior of a researcher using focused crawling systems.
In summary, our findings suggest that query expansion via an LLM has the potential to uncover relevant papers that would otherwise be missed, though further refinements in prompt design are necessary to maximize its effectiveness. The classifiers, while useful in some contexts, do not consistently improve results and, in some cases, may perform worse than the default search engines. The HYDE method shows promise and could play a key role in improving focused crawling techniques.

The report described the methodology, results and limitations as well as a litterature review are available in folder /docs.

## Paper

## Domain review

## Code Architecture
![Code architecture](./images/class_diagram.png)

## How to Use the Code
Before running the code, make sure to choose the correct saving directory, use case, and searcher in file run_crawler.py.

### Step-by-Step Instructions:

#### 1. Install Ollama
Open the first terminal and run the following commands to install and start Ollama:
```bash
curl https://ollama.ai/install.sh | sh
ollama serve
```
#### 2. Set Up the Python Environment
In a second terminal, navigate to the project directory and create a virtual environment:
```bash
cd demokritos_internship/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2
```
#### 3. Run Focused Crawlers
```bash
run_crawler.py
```