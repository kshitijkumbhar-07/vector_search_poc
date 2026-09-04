from google.cloud import aiplatform

from app.config import (
    GCP_PROJECT_ID,
    GOOGLE_CLOUD_LOCATION,
)



ENDPOINT_DISPLAY_NAME = "adk-vector-poc-endpoint"

PUBLIC_ENDPOINT = True


def main() -> None:


    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GOOGLE_CLOUD_LOCATION,
    )

    print("=" * 70)
    print("CREATING VERTEX AI VECTOR SEARCH INDEX ENDPOINT")
    print("=" * 70)

    print(f"Project        : {GCP_PROJECT_ID}")
    print(f"Region         : {GOOGLE_CLOUD_LOCATION}")
    print(f"Display name   : {ENDPOINT_DISPLAY_NAME}")
    print(f"Public endpoint: {PUBLIC_ENDPOINT}")

    print("=" * 70)



    index_endpoint = (
        aiplatform.MatchingEngineIndexEndpoint.create(
            display_name=ENDPOINT_DISPLAY_NAME,
            public_endpoint_enabled=PUBLIC_ENDPOINT,
        )
    )

    print()
    print("=" * 70)
    print("VECTOR SEARCH INDEX ENDPOINT CREATED")
    print("=" * 70)

    print(f"Display name       : {index_endpoint.display_name}")
    print(f"Resource name      : {index_endpoint.resource_name}")
    print(f"Endpoint ID        : {index_endpoint.name.split('/')[-1]}")
    print(
        f"Public endpoint    : "
        f"{index_endpoint.public_endpoint_domain_name}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()