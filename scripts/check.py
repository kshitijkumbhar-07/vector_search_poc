from google.cloud import aiplatform

aiplatform.init(project="cp-sandbox-gaurav-math300", location="us-east4")

index = aiplatform.MatchingEngineIndex(
    index_name="projects/181154304722/locations/us-east4/indexes/9200594553973768192"
)

# Print basic index details
print("Index Display Name:", index.display_name)
print("Last Updated Time :", index.update_time)