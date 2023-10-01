
I have implemented this project using vectorDB(FAISS), model(TheBloke/Llama-2-7B-Chat-GGML),Bhagavad_Gita_As_It_Is(pdf)
Following model can be extracted from the HuggingFace. The problem with actual one is it is taking too much RAM while training
which is crashing the terminal. Hence I have taken GGML file of the same.I have preprocessed the input file by removing unneccessary pages.
There are other input files which are only english versions but they are concise so I have taken the following pdf which has resulted
in better results comparatively.

Installation instructions:
Execute the following commands while running the model.
pip install -r requirements.txt --default-timeout=100 future
and then run python upload.python this will create a vectorstore folder(cross verify) in the directory
and then run python model.py this will open chatbot using chainlit

Usage instructions:
It will display an introductory statement of:
"# Welcome to Gita App!
We have tried best to provide the valid answer for the queries.
Kindly check the source documents provided in answer as well for detailed explaination.

When we enter an query in the bot we will get the response of output and also the source document(with page specified) will be given."
Sample output:
Query: what to do in depression?
Result:  1. You should not be overly attached to any material possessions, but instead be detached from them mentally. 2. You should try to understand that everything is temporary, and so we shouldn't get too attached to anything. 3. We must learn to tolerate all of life's challenges with patience and inner strength.
Source Documents:
act giving up all results of your work and try to be self-situated. PURPORT
Source: /home/Bhagavad_Gita_As_It_Is.pdf, Page: 741
coming and going of happiness and distre ss, so one should be detached from the materialistic way of life and be automatically equipoised in both cases. Generally, when we get something desirable we are very happy, and when we get something undesirable we are distressed. But if we are actually in the spiritual position these things will not agitate us. To reac h that stage, we have to practice unbreakable devotional se rvice. Devotional service to Kåñëa
Source: /home/Bhagavad_Gita_As_It_Is.pdf, Page: 771

File structure:
data folder contains the pdf(initial upload command work for any pdfs added into data folder so that we can add accordingly)
Rest of the files like model.py,upload.py,requirements.txt will be in the main folder directory itself.


