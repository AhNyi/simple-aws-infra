# AWS CDK Infrastructure as Code (IaC) with Python

This repository provides a step-by-step guide on developing infrastructure using Python-based Infrastructure as Code (IaC) with AWS CDK. You can refer to the [Getting Started with Python-based IaC using AWS CDK](https://dev.to/aws-builders/getting-started-with-python-based-iac-using-aws-cdk-152h) article for additional details.

## Prerequisites

Before you start setting up the project, make sure you have the following prerequisites installed on your system:

1. **AWS CDK:** Ensure that you have AWS CDK installed. You can check the installed version with the following command:

    ```bash
    cdk --version
    ```

    If AWS CDK is not installed, you can follow the official [AWS CDK installation guide](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_install).

2. **Python (>=3.6):** The project requires Python, and it's recommended to have version 3.6 or higher installed. You can check the installed version with the following command:

    ```bash
    python --version
    ```

    If Python is not installed, you can download it from the official [Python website](https://www.python.org/downloads/).

3. **Pipenv:** Pipenv is used for managing Python dependencies and virtual environments. Install Pipenv by running the following command:

    ```bash
    pip install pipenv
    ```

    Verify the installation by checking the Pipenv version:

    ```bash
    pipenv --version
    ```

    If you don't have pip installed, you can follow the [pip installation guide](https://pip.pypa.io/en/stable/installation/).


## Setup Steps

1. Clone the repository and navigate to the project directory:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Initialize the CDK app with Python as the language:

    ```bash
    cdk init app --language python
    ```

3. Set up a virtual environment:

    ```bash
    python -m venv .venv
    ```

4. Install required dependencies:

    ```bash
    pipenv install
    ```

5. List available CDK stacks:

    ```bash
    cdk ls
    ```

    or, with a specific stage:

    ```bash
    cdk -c stage=dev ls
    ```

6. Install additional CDK core package:

    ```bash
    python -m pip install -r requirements.txt
    ```

7. Deploy the CDK stack:

    ```bash
    cdk -c stage=dev deploy simple-aws-dynamodb --profile your-profile-name
    ```

Happy coding!
