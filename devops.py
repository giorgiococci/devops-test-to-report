from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from config import get_config_value

# Fill in with your personal access token and org URL


def get_devops_connection():
    """
    Get a DevOps connection object
    """
    personal_access_token = get_config_value("PAT")
    credentials = BasicAuthentication("", personal_access_token)
    organization_url = get_config_value("ORGANIZATION_URL")

    return Connection(
        creds=credentials,
        base_url=organization_url)

def get_test_client():
    """
    Get a test client
    """
    # Create a connection to the organization
    connection = get_devops_connection()
    return connection.clients.get_test_client()

def get_test_runs(test_client):
    """
    Get a list of test runs
    """
    # Get a list of test runs
    test_runs = test_client.get_test_runs(project=get_config_value("PROJECT"))
    return test_runs

def parse_args():
    """
    Parse command line arguments
    """
    import argparse
    parser = argparse.ArgumentParser(description="Get test runs")
    parser.add_argument("--runId", "-p", help="Test run id")
    return parser.parse_args()


if __name__ == "__main__":

    # Get args
    args = parse_args()

    # Get a client
    test_client = get_test_client()

    # Get a list of test runs
    test_runs = get_test_runs(test_client)

    # If runId is specified, get the test run
    if args.runId:
        test_results = test_client.get_test_results(project=get_config_value("PROJECT"), run_id=args.runId)
        for test_result in test_results:
            test_result_attachments = test_client.get_test_result_attachments(project=get_config_value("PROJECT"), run_id=args.runId, test_case_result_id=test_result.id)
            print(test_result_attachments)

    print("Test Runs:")
    print(test_runs)