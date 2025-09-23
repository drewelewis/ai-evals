#!/usr/bin/env python3
"""
Local-Only Evaluation - All Evaluators Without Cloud Upload

This script runs all evaluations locally without uploading to Azure AI Foundry.
Results are saved locally and can be analyzed without cloud dependencies.
"""

import os
import json
from dotenv import load_dotenv
from azure.ai.evaluation import evaluate
from azure.ai.evaluation import (
    RelevanceEvaluator,
    CoherenceEvaluator,
    GroundednessEvaluator,
    FluencyEvaluator,
    RetrievalEvaluator,
    IntentResolutionEvaluator,
    TaskAdherenceEvaluator
)
from azure.ai.evaluation import AzureOpenAIModelConfiguration

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def get_model_config():
    """Get Azure OpenAI model configuration."""
    return AzureOpenAIModelConfiguration(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        api_version="2024-02-01"
    )

def create_evaluators(model_config):
    """Create all available evaluators."""
    evaluators = {}
    
    try:
        # Quality evaluators
        evaluators["coherence"] = CoherenceEvaluator(model_config=model_config)
        evaluators["fluency"] = FluencyEvaluator(model_config=model_config)
        evaluators["groundedness"] = GroundednessEvaluator(model_config=model_config)
        evaluators["relevance"] = RelevanceEvaluator(model_config=model_config)
        
        # RAG evaluators
        evaluators["retrieval"] = RetrievalEvaluator(model_config=model_config)
        
        # Agent evaluators
        evaluators["intent_resolution"] = IntentResolutionEvaluator(model_config=model_config)
        evaluators["task_adherence"] = TaskAdherenceEvaluator(model_config=model_config)
        
        print(f"✅ Created {len(evaluators)} evaluators")
        return evaluators
        
    except Exception as e:
        print(f"❌ Error creating evaluators: {e}")
        return {}

def target_fn(query, context=None):
    """Target function that evaluators will test."""
    return {
        "response": f"This is a response to: {query}",
        "context": context or "Default context"
    }

def run_evaluations():
    """Run all evaluations locally without cloud upload."""
    print("🚀 Starting Local AI Evaluation Pipeline")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
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
    print(f"💡 Running evaluations locally (no cloud upload)")
    
    # Run evaluations
    results = {}
    successful_evals = 0
    
    for name, evaluator in evaluators.items():
        try:
            print(f"\n🔄 Running {name} evaluation...")
            
            result = evaluate(
                evaluation_name=f"local_{name}",
                data=data_file,
                evaluators={name: evaluator},
                target=target_fn
                # NOTE: No azure_ai_project parameter = local execution only
            )
            
            results[name] = result
            successful_evals += 1
            print(f"✅ {name} evaluation completed successfully")
            
        except Exception as e:
            print(f"❌ {name} evaluation failed: {e}")
            results[name] = {"error": str(e)}
            continue
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Evaluation Summary: {successful_evals}/{len(evaluators)} successful")
    
    if successful_evals > 0:
        print("✅ Evaluations completed successfully!")
        
        # Save results locally
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        local_file = f"output/local_results_{timestamp}.json"
        
        os.makedirs("output", exist_ok=True)
        with open(local_file, 'w') as f:
            json.dump({k: str(v) for k, v in results.items()}, f, indent=2)
        
        print(f"💾 Results saved locally: {local_file}")
        
        # Also save a summary
        summary_file = f"output/local_summary_{timestamp}.json"
        summary = {}
        for name, result in results.items():
            if isinstance(result, dict) and "error" not in result:
                try:
                    # Try to extract key metrics if available
                    if hasattr(result, 'metrics'):
                        summary[name] = {"metrics": result.metrics}
                    else:
                        summary[name] = {"status": "completed", "type": str(type(result))}
                except:
                    summary[name] = {"status": "completed"}
            else:
                summary[name] = result
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Summary saved: {summary_file}")
        
        return True
    else:
        print("❌ No evaluations completed successfully")
        return False

if __name__ == "__main__":
    success = run_evaluations()
    if success:
        print("\n🎉 Local evaluation pipeline completed successfully!")
        print("💡 To enable cloud upload, fix Azure storage permissions and use run_evaluation_with_cloud_upload.py")
    else:
        print("\n💥 Local evaluation pipeline failed")
        exit(1)