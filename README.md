# chatbot-group7

## Getting started
Tutorial to start developing on the project.

### Get files from gitlab

```
cd existing_repo
git remote add <preferred remote name> https://git.informatik.uni-leipzig.de/SWS/lehre/ss-2023/se4ai/project/chatbot-group7.git
git pull <preferred remote name> main
```

### Set up local python environment

Add python virtualenv inside the project folder (name = env)
```
python -m venv env
```

Activate virtualenv
```
source env/bin/activate
```

Install depenendencies from requirements.txt inside virtualenv
```
pip install -r requirements.txt
```

### Set up environment variable file for credentials

Create .env-file inside project folder
```
nano .env
vi .env
```

Inside the file fill in the following environment variables
```
PINECONE_INDEX_NAME=""
PINECONE_API_KEY=""
PINECONE_API_ENV=""
```

### Development workflow for virtualenv & dependency installation

Before developing start the virtualenv if not already active
```
source env/bin/activate
```

If you want to add new dependencies/requirements assure yourself that
* you got the latest requirements.txt file within the branch
* your virtualenv is active
* your virtualenv has all the newest dependencies installed

If this is true install the dependency regularly
```
pip install <dependency name>
```

After the installation is finished write a new requirements.txt file
```
pip freeze > requirements.txt
```

The requirements.txt file can then be shared regularly via git and installed by all the others. This is also why it is important to check for new dependencies in the file, when pulling code.

For Conda users getting odd path references in requirements.txt, use:

```
pip list --format=freeze > requirements.txt
```