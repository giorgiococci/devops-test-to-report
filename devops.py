from vsts.vss_connection import VssConnection
from msrest.authentication import BasicAuthentication
from config import get_config_value

# Fill in with your personal access token and org URL


def get_vsts_connection():
    """
    Get a VSTS connection object
    """
    personal_access_token = get_config_value("PAT")
    credentials = BasicAuthentication("", personal_access_token)
    organization_url = get_config_value("ORGANIZATION_URL")

    return VssConnection(
        creds=credentials,
        base_url=organization_url)

def get_test_client():
    """
    Get a test client
    """
    # Create a connection to the organization
    connection = get_vsts_connection()
    TEST_CLIENT = "vsts.test.v4_1.test_client.TestClient"
    return connection.get_client(TEST_CLIENT)

def get_test_runs(test_client):
    """
    Get a list of test runs
    """
    # Get a list of test runs
    test_runs = test_client.get_test_runs()
    return test_runs


if __name__ == "__main__":

    # Get a client
    test_client = get_test_client()

    # Get a list of test runs
    test_runs = get_test_runs(test_client)

    print("Test Runs:")
    print(test_runs)