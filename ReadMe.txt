GOOGLE ADK + VERTEX AI VECTOR SEARCH RAG POC
============================================================
COMPLETE SETUP GUIDE — FROM ZERO
============================================================

This guide assumes a completely fresh machine/environment.

The final architecture is:

User
|
v
Google ADK Agent
|
v
search_knowledge_base()
|
v
Generate Query Embedding
|
v
Vertex AI Vector Search
|
v
Top-K Document IDs
|
v
documents.jsonl
|
v
Retrieved Context
|
v
Gemini 2.5 Flash
|
v
Final Answer


============================================================
1. PREREQUISITES
============================================================

Install:

- Python 3.12
- Google Cloud CLI
- Git
- VS Code (recommended)

Verify:

python --version
gcloud --version
git --version

Python should be:

Python 3.12.x


============================================================
2. CLONE THE PROJECT
============================================================

git clone <REPOSITORY_URL>

cd google-adk-vector-rag


============================================================
3. CREATE PYTHON VIRTUAL ENVIRONMENT
============================================================

python -m venv .venv

Activate:

.\.venv\Scripts\Activate.ps1

Verify:

python --version

The terminal should show:

(.venv)


============================================================
4. INSTALL PYTHON DEPENDENCIES
============================================================

requirements.txt should contain:

google-adk
google-genai
google-cloud-aiplatform
google-cloud-storage
python-dotenv

Install:

pip install -r requirements.txt


============================================================
5. GOOGLE CLOUD LOGIN
============================================================

Login:

gcloud auth login

Check:

gcloud auth list


============================================================
6. SELECT / CREATE GCP PROJECT
============================================================

List projects:

gcloud projects list

Set the project:

gcloud config set project YOUR_PROJECT_ID

Example:

gcloud config set project cp-sandbox-kshitij-kumb179

Verify:

gcloud config get-value project

The output should be your project ID.


============================================================
7. APPLICATION DEFAULT CREDENTIALS (ADC)
============================================================

Python Google Cloud libraries use ADC.

Run:

gcloud auth application-default login

Then:

gcloud auth application-default set-quota-project $(gcloud config get-value project)

Verify:

gcloud auth application-default print-access-token

A token should be returned.


============================================================
8. ENABLE REQUIRED GOOGLE CLOUD APIS
============================================================

Enable Vertex AI:

gcloud services enable aiplatform.googleapis.com

Enable Cloud Storage:

gcloud services enable storage.googleapis.com

If required:

gcloud services enable generativelanguage.googleapis.com

Verify:

gcloud services list --enabled


============================================================
9. CREATE CLOUD STORAGE BUCKET
============================================================

Bucket names must be globally unique.

Create:

gcloud storage buckets create gs://YOUR_PROJECT_ID-vector-poc \
--location=us-central1 \
--project=YOUR_PROJECT_ID

Example:

gcloud storage buckets create gs://cp-sandbox-kshitij-kumb179-vector-poc \
--location=us-central1 \
--project=cp-sandbox-kshitij-kumb179

Verify:

gcloud storage buckets list


============================================================
10. PREPARE DOCUMENTS
============================================================

Create:

data/documents.jsonl

Example contents:

{"id":"doc1","content":"A Kubernetes Pod is the smallest deployable unit in Kubernetes."}
{"id":"doc2","content":"A Kubernetes Service provides a stable network endpoint for Pods."}
{"id":"doc3","content":"A Kubernetes Deployment manages replicated Pods and supports rolling updates."}
{"id":"doc4","content":"Cloud SQL is a fully managed relational database service provided by Google Cloud."}
{"id":"doc5","content":"PostgreSQL is an open-source relational database management system."}


============================================================
11. GENERATE EMBEDDINGS
============================================================

Embedding model:

gemini-embedding-001

Embedding dimensions:

768

Run:

python -m scripts.create_embeddings

Expected:

doc1 -> 768 dimensions
doc2 -> 768 dimensions
doc3 -> 768 dimensions
doc4 -> 768 dimensions
doc5 -> 768 dimensions

This creates:

data/
documents.jsonl
embeddings.jsonl


============================================================
12. UPLOAD EMBEDDINGS TO GCS
============================================================

Run:

python -m scripts.upload_vectors

Expected:

GCS URI:
gs://YOUR_BUCKET/vector-data

Verify:

gcloud storage ls gs://YOUR_BUCKET/vector-data/

The embeddings file should be inside the vector-data directory.


============================================================
13. CREATE VERTEX AI VECTOR SEARCH INDEX
============================================================

Run:

python -m scripts.create_vector_index

Configuration:

Dimensions:
768

Distance:
COSINE_DISTANCE

Update method:
BATCH_UPDATE

After creation, find the Index ID:

gcloud ai indexes list --region=us-central1

The output contains:

projects/PROJECT_NUMBER/locations/us-central1/indexes/INDEX_ID

Save the numeric INDEX_ID.


============================================================
14. CREATE VECTOR SEARCH INDEX ENDPOINT
============================================================

Run:

gcloud ai index-endpoints create \
--display-name=adk-vector-poc-endpoint \
--public-endpoint-enabled \
--region=us-central1 \
--project=YOUR_PROJECT_ID

Find the endpoint:

gcloud ai index-endpoints list \
--region=us-central1

The output contains:

projects/PROJECT_NUMBER/locations/us-central1/indexEndpoints/ENDPOINT_ID

Save the numeric ENDPOINT_ID.


============================================================
15. DEPLOY INDEX TO ENDPOINT
============================================================

Use the Index ID and Endpoint ID obtained above.

Run:

gcloud ai index-endpoints deploy-index ENDPOINT_ID \
--index=INDEX_ID \
--deployed-index-id=adk_vector_poc \
--region=us-central1

Verify:

gcloud ai index-endpoints describe ENDPOINT_ID \
--region=us-central1

Look for:

deployedIndexes:
id: adk_vector_poc


============================================================
16. UNDERSTAND THE THREE IMPORTANT IDs
============================================================

These are DIFFERENT values:

INDEX ID:

3959409541342298112

ENDPOINT ID:

2253200591499034624

DEPLOYED INDEX ID:

adk_vector_poc

Your actual Index ID and Endpoint ID will be different in a new project.

Get them using the commands above.


============================================================
17. CREATE .env
============================================================

Create:

.env

Use:

GCP_PROJECT_ID=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1

EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSIONS=768

VECTOR_SEARCH_INDEX_ID=YOUR_INDEX_ID
VECTOR_SEARCH_INDEX_ENDPOINT_ID=YOUR_ENDPOINT_ID
DEPLOYED_INDEX_ID=adk_vector_poc

VECTOR_SEARCH_BUCKET=YOUR_BUCKET_NAME
VECTOR_SEARCH_GCS_PATH=vector-data

TOP_K=3
GEMINI_MODEL=gemini-2.5-flash


============================================================
18. HOW TO GET EACH .env VALUE
============================================================

GCP_PROJECT_ID:

gcloud config get-value project


GOOGLE_CLOUD_LOCATION:

us-central1


EMBEDDING_MODEL:

gemini-embedding-001


EMBEDDING_DIMENSIONS:

768


VECTOR_SEARCH_INDEX_ID:

gcloud ai indexes list --region=us-central1


VECTOR_SEARCH_INDEX_ENDPOINT_ID:

gcloud ai index-endpoints list --region=us-central1


DEPLOYED_INDEX_ID:

gcloud ai index-endpoints describe ENDPOINT_ID \
--region=us-central1

Look for:

deployedIndexes:
id: adk_vector_poc


VECTOR_SEARCH_BUCKET:

gcloud storage buckets list


VECTOR_SEARCH_GCS_PATH:

gcloud storage ls gs://YOUR_BUCKET/

Use:

vector-data


TOP_K:

3


GEMINI_MODEL:

gemini-2.5-flash


============================================================
19. VERIFY GCP RESOURCES
============================================================

Verify project:

gcloud config get-value project


Verify bucket:

gcloud storage buckets list


Verify vector data:

gcloud storage ls gs://YOUR_BUCKET/vector-data/


Verify Vector Search index:

gcloud ai indexes list --region=us-central1


Verify Vector Search endpoint:

gcloud ai index-endpoints list --region=us-central1


Verify deployment:

gcloud ai index-endpoints describe ENDPOINT_ID \
--region=us-central1


============================================================
20. TEST EMBEDDING GENERATION
============================================================

Run:

python -m scripts.create_embeddings

Expected:

doc1 -> 768 dimensions
doc2 -> 768 dimensions
doc3 -> 768 dimensions
doc4 -> 768 dimensions
doc5 -> 768 dimensions

Confirm:

data/embeddings.jsonl

exists.


============================================================
21. TEST GCS UPLOAD
============================================================

Run:

python -m scripts.upload_vectors

Verify:

gcloud storage ls gs://YOUR_BUCKET/vector-data/


============================================================
22. TEST VECTOR SEARCH DIRECTLY
============================================================

Run:

python -m scripts.test_vector_search

Test query:

What is a Kubernetes Pod?

Expected top result:

ID: doc1

This confirms:

Query
|
v
Gemini Embedding
|
v
768-dimensional vector
|
v
Vertex AI Vector Search
|
v
Nearest documents


============================================================
23. TEST FULL RETRIEVAL
============================================================

Run:

python -m tests.test_retrieval

Expected:

Result 1
ID: doc1

Content:
A Kubernetes Pod is the smallest deployable unit in Kubernetes.

This confirms:

Query
|
v
Embedding
|
v
Vector Search
|
v
Document ID
|
v
documents.jsonl
|
v
Actual document content


============================================================
24. TEST ADK AGENT IMPORT
============================================================

Run:

python -c "from app.agent import root_agent; print(root_agent.name)"

Expected:

rag_agent


============================================================
25. START GOOGLE ADK
============================================================

Run:

adk web

Open the URL shown by ADK.

Select:

rag_agent


============================================================
26. TEST RAG QUESTIONS
============================================================

TEST 1:

What is a Kubernetes Pod?

Expected relevant document:

doc1


TEST 2:

What provides a stable network endpoint for Pods?

Expected relevant document:

doc2


TEST 3:

What manages replicated Pods and rolling updates?

Expected relevant document:

doc3


TEST 4:

What is Cloud SQL?

Expected relevant document:

doc4


TEST 5:

What is PostgreSQL?

Expected relevant document:

doc5


============================================================
27. NEGATIVE / GROUNDEDNESS TEST
============================================================

Ask:

What is Amazon DynamoDB?

DynamoDB is not present in the sample knowledge base.

The agent should NOT invent an answer.

It should explain that the knowledge base does not contain enough information.


============================================================
28. COMPLETE RAG FLOW
============================================================

USER QUERY
|
v
Google ADK Agent
|
v
search_knowledge_base()
|
v
Generate Embedding
|
v
768-D Vector
|
v
Vertex AI Vector Search
|
v
Top-K IDs
|
v
documents.jsonl
|
v
Retrieved Context
|
v
Gemini 2.5 Flash
|
v
Final Answer


============================================================
29. NORMAL DAY-TO-DAY TESTING
============================================================

Once the infrastructure already exists, DO NOT recreate:

- Vector Search Index
- Vector Search Endpoint
- Index Deployment

Normally use:

.\.venv\Scripts\Activate.ps1

Then:

python scripts/run_poc.py

If validation passes:

adk web


============================================================
30. WHEN DOCUMENTS CHANGE
============================================================

If documents are added or modified:

1. Update:

data/documents.jsonl

2. Generate embeddings:

python -m scripts.create_embeddings

3. Upload:

python -m scripts.upload_vectors

4. Update the existing Vector Search index using the project's
update/index synchronization process.

Do NOT create a new Vector Search index every time.


============================================================
31. IMPORTANT RULES
============================================================

DO NOT run this every time:

python -m scripts.create_vector_index

It creates a new Vector Search index.

DO NOT create a new endpoint every time:

gcloud ai index-endpoints create ...

The endpoint is a persistent Google Cloud resource.

Keep embedding dimensions consistent:

Embedding Model
|
v
768 dimensions
|
v
Vector Search Index
|
v
768 dimensions


============================================================
32. COMPLETE FIRST-TIME SETUP COMMANDS
============================================================

For a completely fresh machine:

1.

git clone <REPOSITORY_URL>

2.

cd google-adk-vector-rag

3.

python -m venv .venv

4.

.\.venv\Scripts\Activate.ps1

5.

pip install -r requirements.txt

6.

gcloud auth login

7.

gcloud projects list

8.

gcloud config set project YOUR_PROJECT_ID

9.

gcloud auth application-default login

10.

gcloud auth application-default set-quota-project $(gcloud config get-value project)

11.

gcloud services enable aiplatform.googleapis.com

12.

gcloud services enable storage.googleapis.com

13.

Create the GCS bucket

14.

Create data/documents.jsonl

15.

python -m scripts.create_embeddings

16.

python -m scripts.upload_vectors

17.

python -m scripts.create_vector_index

18.

Get the Index ID

19.

Create the Vector Search Endpoint

20.

Get the Endpoint ID

21.

Deploy the Index

22.

Get the Deployed Index ID

23.

Create .env

24.

python -m scripts.test_vector_search

25.

python -m tests.test_retrieval

26.

python -c "from app.agent import root_agent; print(root_agent.name)"

27.

adk web


============================================================
33. QUICK CHECKLIST
============================================================

[ ] Python 3.12 installed
[ ] Google Cloud CLI installed
[ ] Git installed
[ ] Repository cloned
[ ] Virtual environment created
[ ] Virtual environment activated
[ ] requirements.txt installed
[ ] gcloud authenticated
[ ] ADC configured
[ ] GCP project selected
[ ] Vertex AI API enabled
[ ] Cloud Storage API enabled
[ ] GCS bucket created
[ ] documents.jsonl created
[ ] Embeddings generated
[ ] Embeddings uploaded to GCS
[ ] Vector Search index created
[ ] Vector Search endpoint created
[ ] Index deployed
[ ] .env configured
[ ] Vector Search test passed
[ ] Retrieval test passed
[ ] ADK agent loaded
[ ] ADK web started
[ ] RAG queries tested

