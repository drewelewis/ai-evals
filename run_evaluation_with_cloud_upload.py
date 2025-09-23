#!/usr/bin/env python3
"""
Fixed Cloud Deployment - All Evaluators with Enhanced Error Handling

Addresses authentication, connection, and permission issues identified in the logs.
Uses explicit Azure ML hub connection instead of CONNECTION_STRING.
"""

import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.ai.ml import MLClient
from azure.ai.evaluation import evaluate
from azure.ai.evaluation import (
    ContentSafetyEvaluator,
    HateUnfairnessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    GroundednessEvaluator,
    FluencyEvaluator,
    RetrievalEvaluator,
    IntentResolutionEvaluator,
    TaskAdherenceEvaluator,
    AzureOpenAIModelConfiguration
)

# Load environment variables
load_dotenv(override=True)

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY", 
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_SUBSCRIPTION_ID",
        "AZURE_RESOURCE_GROUP",
        "AZURE_AI_FOUNDRY_PROJECT"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("💡 Please copy sample.env to .env and fill in the missing values")
        return False
    
    print("✅ All required environment variables are set")
    return True

def get_az_command():
    """Get the Azure CLI command with Windows-specific path handling."""
    import os
    import subprocess
    
    # Try common Azure CLI installation paths on Windows
    az_paths = [
        'az',  # If it's in PATH
        r'C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd',
        r'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd',
        r'C:\Users\{}\AppData\Local\Programs\Python\Python*\Scripts\az.exe'.format(os.getenv('USERNAME', '')),
    ]
    
    for az_path in az_paths:
        try:
            result = subprocess.run([az_path, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return az_path
        except Exception:
            continue
    
    return 'az'  # Fallback to default

def check_azure_cli_installed():
    """Check if Azure CLI is installed."""
    import subprocess
    try:
        
        az_cmd = get_az_command()
        result = subprocess.run([az_cmd, '--version'], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
        
    except Exception as e:
        print(f"Debug: Azure CLI check failed with: {e}")
        return False

def test_authentication():
    """Use DefaultAzureCredential instead of forcing Azure CLI login."""
    print("� Using DefaultAzureCredential for authentication...")
    print("🔄 This will try multiple authentication methods automatically.")
    
    try:
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        
        # Test the credential
        token = credential.get_token("https://management.azure.com/.default")
        print("✅ Authentication successful with DefaultAzureCredential!")
        
        return credential
        
    except Exception as e:
        print(f"❌ DefaultAzureCredential failed: {e}")
        print("💡 Falling back to AzureCliCredential...")
        
        try:
            credential = AzureCliCredential()
            token = credential.get_token("https://management.azure.com/.default")
            print("✅ Authentication successful with AzureCliCredential!")
            return credential
        except Exception as e2:
            print(f"❌ AzureCliCredential also failed: {e2}")
            print("💡 Please run 'az login' manually in a terminal")
            return None

def get_model_config():
    """Get Azure OpenAI model configuration."""
    return AzureOpenAIModelConfiguration(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_version="2024-02-01"
    )

def create_ml_client():
    """Create Azure ML client with enhanced error handling."""
    try:
        # Force authentication
        credential = test_authentication()
        if not credential:
            print("❌ Authentication failed")
            return None
        
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        resource_group = os.getenv("AZURE_RESOURCE_GROUP") 
        project_name = os.getenv("AZURE_AI_FOUNDRY_PROJECT")
        
        print(f"🔗 Connecting to Azure AI Foundry...")
        print(f"   Subscription: {subscription_id[:8]}...")
        print(f"   Resource Group: {resource_group}")
        print(f"   Project: {project_name}")
        
        client = MLClient(
            credential=credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=project_name
        )
        
        # Test the connection
        try:
            client.workspaces.get(project_name)
            print("✅ Azure AI Foundry connection successful")
            return client
        except Exception as e:
            print(f"❌ Failed to connect to Azure AI Foundry: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating ML client: {e}")
        return None

def create_evaluators(model_config):
    """Create evaluation instances with error handling."""
    evaluators = {}
    
    try:
        # Basic evaluators (usually most reliable)
        evaluators['coherence'] = CoherenceEvaluator(model_config=model_config)
        evaluators['fluency'] = FluencyEvaluator(model_config=model_config)
        evaluators['groundedness'] = GroundednessEvaluator(model_config=model_config)
        evaluators['relevance'] = RelevanceEvaluator(model_config=model_config)
        
        # RAG evaluators
        evaluators['retrieval'] = RetrievalEvaluator(model_config=model_config)
        
        # Intent and task evaluators  
        evaluators['intent_resolution'] = IntentResolutionEvaluator(model_config=model_config)
        evaluators['task_adherence'] = TaskAdherenceEvaluator(model_config=model_config)
        
        # Safety evaluators (may require special permissions)
        try:
            evaluators['content_safety'] = ContentSafetyEvaluator()
            evaluators['hate_unfairness'] = HateUnfairnessEvaluator(model_config=model_config)
        except Exception as e:
            print(f"⚠️  Note: Some safety evaluators may need additional permissions: {e}")
        
        print(f"✅ Created {len(evaluators)} evaluators")
        return evaluators
        
    except Exception as e:
        print(f"❌ Error creating evaluators: {e}")
        return {}

def target_fn(query: str, context: str = None, **kwargs):
    """Target function for evaluation - returns a simple response."""
    return {
        "response": f"This is a response to: {query}",
        "context": context or "Default context"
    }

def run_evaluations():
    """Run all evaluations with cloud upload."""
    print("🚀 Starting Azure AI Foundry Evaluation Pipeline")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        return False
    
    # Get authentication credentials first
    credential = test_authentication()
    if not credential:
        return False
    
    # Create ML client (includes authentication)
    client = create_ml_client()
    if not client:
        return False
    
    # Get model configuration
    model_config = get_model_config()
    
    # Create evaluators
    evaluators = create_evaluators(model_config)
    if not evaluators:
        print("❌ No evaluators created")
        return False
    
    # Use data file path for evaluations
    data_file = "data/sample_data.jsonl"
    
    # Verify data file exists
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return False
    
    print(f"📁 Using data file: {data_file}")
    
    # Add debugging information about the Azure project configuration
    print(f"\n🔍 Azure AI Project Configuration:")
    print(f"   - Subscription ID: {os.getenv('AZURE_SUBSCRIPTION_ID')[:8]}...{os.getenv('AZURE_SUBSCRIPTION_ID')[-4:]}")
    print(f"   - Resource Group: {os.getenv('AZURE_RESOURCE_GROUP')}")
    print(f"   - Project Name: {os.getenv('AZURE_AI_FOUNDRY_PROJECT')}")
    
    # Test if we can read the data file
    try:
        with open(data_file, 'r') as f:
            sample_line = f.readline()
            print(f"   - Data file first line preview: {sample_line[:100]}...")
    except Exception as e:
        print(f"   - Could not preview data file: {e}")
    
    # Run evaluation with ALL evaluators in single batch call
    # This creates grouped reporting like the previous working format  
    # Following the exact pattern from deploy_to_cloud2.py
    print(f"\n🔄 Running batch evaluation with all {len(evaluators)} evaluators...")
    print(f"🔍 Batch evaluation details:")
    print(f"   - Data file: {data_file}")
    print(f"   - Total evaluators: {len(evaluators)}")
    print(f"   - Evaluator names: {list(evaluators.keys())}")
    print(f"   - Azure project config:")
    print(f"     * Subscription: {os.getenv('AZURE_SUBSCRIPTION_ID')[:8]}...")
    print(f"     * Resource Group: {os.getenv('AZURE_RESOURCE_GROUP')}")
    print(f"     * Project: {os.getenv('AZURE_AI_FOUNDRY_PROJECT')}")

    # Create evaluator configs for column mapping (following deploy_to_cloud2.py pattern)
    evaluator_configs = {}
    for name, evaluator in evaluators.items():
        # Use appropriate column mapping based on evaluator type
        if name in ["retrieval"]:
            evaluator_configs[name] = {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}"
                }
            }
        elif name in ["friendliness"]:
            evaluator_configs[name] = {
                "column_mapping": {
                    "response": "${data.response}"
                }
            }
        elif name in ["groundedness", "relevance", "fluency"]:
            evaluator_configs[name] = {
                "column_mapping": {
                    "query": "${data.query}",
                    "context": "${data.context}",
                    "response": "${data.response}"
                }
            }
        else:  # coherence, intent_resolution, task_adherence, hate_unfairness, content_safety
            evaluator_configs[name] = {
                "column_mapping": {
                    "query": "${data.query}",
                    "response": "${data.response}"
                }
            }

    try:
        # Use exact pattern from working deploy_to_cloud2.py
        result = evaluate(
            data=data_file,
            evaluators=evaluators,  # ALL evaluators in single call
            evaluator_config=evaluator_configs,  # Column mappings
            azure_ai_project={
                "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
                "resource_group_name": os.getenv("AZURE_RESOURCE_GROUP"),
                "project_name": os.getenv("AZURE_AI_FOUNDRY_PROJECT"),
            },
            output_path="./output/foundry_batch_results.json"
        )
        
        # Log detailed information about the batch result
        print(f"📊 Batch evaluation result analysis:")
        print(f"   - Result type: {type(result)}")
        if hasattr(result, 'keys'):
            print(f"   - Result keys: {list(result.keys())}")
        
        # Check for specific upload-related attributes
        if hasattr(result, 'studio_url'):
            print(f"   - Studio URL: {result.studio_url}")
        if hasattr(result, 'metrics'):
            print(f"   - Metrics available: {bool(result.metrics)}")
            
        results = {"batch_evaluation": result}
        successful_evals = 1
        print(f"✅ Batch evaluation completed successfully")
        
    except Exception as e:
        print(f"❌ Batch evaluation failed: {e}")
        print(f"🔍 Error details:")
        print(f"   - Error type: {type(e).__name__}")
        print(f"   - Error message: {str(e)}")
        
        # Check if it's specifically a storage/upload error
        error_str = str(e).lower()
        if 'storage' in error_str:
            print(f"   - This is a STORAGE-related error")
        if 'upload' in error_str:
            print(f"   - This is an UPLOAD-related error")
        if 'permission' in error_str:
            print(f"   - This is a PERMISSION-related error")
            
        # Try to get more detailed error information
        if hasattr(e, '__cause__') and e.__cause__:
            print(f"   - Root cause: {e.__cause__}")
        if hasattr(e, 'args') and e.args:
            print(f"   - Error args: {e.args}")
            
        results = {"batch_evaluation": {"error": str(e)}}
        successful_evals = 0
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Evaluation Summary: {successful_evals}/1 batch evaluation successful")
    
    if successful_evals > 0:
        print("✅ Batch evaluation completed successfully!")
        print(f"📊 Evaluated {len(evaluators)} evaluators in single batch:")
        for evaluator_name in evaluators.keys():
            print(f"   - {evaluator_name}")
        
        # Save results locally as backup
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        local_file = f"output/foundry_all_results_{timestamp}.json"
        
        os.makedirs("output", exist_ok=True)
        with open(local_file, 'w') as f:
            json.dump({k: str(v) for k, v in results.items()}, f, indent=2)
        
        print(f"💾 Results also saved locally: {local_file}")
        
        return True
    else:
        print("❌ Batch evaluation failed")
        return False

if __name__ == "__main__":
    success = run_evaluations()
    if success:
        print("\n🎉 Evaluation pipeline completed successfully!")
    else:
        print("\n💥 Evaluation pipeline failed")
        exit(1)