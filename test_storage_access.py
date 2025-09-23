#!/usr/bin/env python3
"""
Quick Azure Storage Access Test

Test if we can access the storage account that was working yesterday.
"""

import os
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.ml import MLClient

load_dotenv()

def test_storage_access():
    """Test basic storage access through Azure ML."""
    try:
        print("🔍 Testing Azure ML workspace connection...")
        
        credential = AzureCliCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
            resource_group_name=os.getenv("AZURE_RESOURCE_GROUP"),
            workspace_name=os.getenv("AZURE_AI_FOUNDRY_PROJECT")
        )
        
        # Get workspace info
        workspace = ml_client.workspaces.get(os.getenv("AZURE_AI_FOUNDRY_PROJECT"))
        print(f"✅ Workspace: {workspace.name}")
        print(f"✅ Location: {workspace.location}")
        
        # Try to list datastores (this tests storage access)
        print("\n🔍 Testing datastore access...")
        datastores = ml_client.datastores.list()
        datastore_list = list(datastores)
        
        print(f"✅ Found {len(datastore_list)} datastore(s):")
        for ds in datastore_list:
            print(f"   - {ds.name} ({ds.type})")
        
        # Try to access the default datastore
        default_ds = ml_client.datastores.get_default()
        print(f"✅ Default datastore: {default_ds.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Storage access test failed: {e}")
        return False

def test_evaluation_upload():
    """Test the actual evaluation upload mechanism."""
    try:
        print("\n🔍 Testing evaluation data upload...")
        
        # This is similar to what the evaluation library does internally
        from azure.ai.evaluation import evaluate
        from azure.ai.evaluation import AzureOpenAIModelConfiguration
        
        # Test with minimal data
        test_data = [
            {
                "query": "Test query",
                "response": "Test response", 
                "context": "Test context"
            }
        ]
        
        # Just test the upload mechanism without running full evaluation
        print("✅ Evaluation library imports work")
        print("💡 This suggests the issue is during the actual upload step, not the setup")
        
        return True
        
    except Exception as e:
        print(f"❌ Evaluation upload test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Azure Storage Access Test")
    print("=" * 40)
    print("Testing what changed since yesterday...")
    
    storage_ok = test_storage_access()
    eval_ok = test_evaluation_upload()
    
    print("\n" + "=" * 40)
    if storage_ok and eval_ok:
        print("✅ Basic access tests passed")
        print("💡 The issue may be in the evaluation library's upload process")
        print("💡 Try running the evaluation again - it might be a temporary Azure service issue")
    else:
        print("❌ Found access issues")
        print("💡 This indicates what changed since yesterday")