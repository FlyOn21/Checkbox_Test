# Project Setup Instructions

## Configuration

Before starting the project, you need to set up the environment configuration.

### Step 1: Rename the Environment File

Locate the `.env_example` file in the root directory of the project. Rename this file to `.env`. This file will contain your environment-specific settings.

**Important**: Do not share your `.env` file with anyone, as it contains sensitive information that is specific to your environment.

### Step 2: Fill in the Required Values

Open the `.env` file and fill in the necessary values. These values are essential for the correct operation of your application.

## Starting the Application

Once you have configured the environment file, you can start the application using Docker Compose.

### Launching the Application

Open your command line interface and navigate to the root directory of the project. Run the following command:

```bash
docker compose --env-file .env up
```


### For Testing the Application

Open your command line interface and navigate to the root directory of the project. Run the following command:

```bash
pytest
```

### After testing the application, 
Before deploying the application, you need  uncomment str 127 file src/services/checks/check_router.py for enable catch.


