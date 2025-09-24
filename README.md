# Azure AI Foundry - Agent Evaluation Pipeline

🚀 **A comprehensive evaluation framework for Azure AI agents using multiple evaluation categories.**

This repository provides a complete evaluation pipeline with **10 specialized evaluators** across 4 categories, designed for thorough assessment of AI agent quality, safety, and performance.

## 📋 Overview

Our evaluation framework covers four main categories with **10 active evaluators**:
- **RAG & Retrieval** (3 evaluators) - For information retrieval accuracy: Groundedness, Relevance, Retrieval
- **Agents** (2 evaluators) - For agent-specific behaviors: Intent Resolution, Task Adherence  
- **General Purpose** (3 evaluators) - For overall response quality: Coherence, Fluency, Friendliness (custom)
- **Safety & Security** (2 evaluators) - Content safety and hate/unfairness detection

## 🤖 How the Evaluations Work

### **🎯 What Gets Evaluated**
This system evaluates **pre-generated AI responses** (not live AI models). You provide a dataset with:
- **Query**: The question asked to the AI
- **Context**: Background information provided to the AI  
- **Response**: The AI's answer (**what gets evaluated**)
- **Ground Truth**: The correct/expected answer (for comparison)

### **☁️ Execution Environment**
- **Location**: Evaluations run in **Azure AI Foundry** (cloud-based)
- **Process**: Your data is uploaded to Azure, evaluated in the cloud, and results returned
- **Scale**: Can handle datasets from 7 samples (testing) to 50,000+ samples (production)

### **📊 Evaluation Process**
1. **Data Upload**: Your JSONL file is sent to Azure AI Foundry
2. **Batch Processing**: All 7 evaluators analyze each response simultaneously  
3. **Scoring**: Each evaluator gives a 1-5 score plus pass/fail result
4. **Aggregation**: Results combined into a single report with metrics and studio URL

### **🔍 What Each Evaluator Does**

#### **Quality Evaluators**
- **Coherence**: Is the response logically organized and sensible?
- **Fluency**: Grammar, clarity, and readability assessment
- **Relevance**: Does the answer directly address the question?

#### **Accuracy Evaluators** 
- **Groundedness**: Is the response based on the provided context?
- **Retrieval**: How well does the response use relevant information?

#### **Agent Evaluators**
- **Intent Resolution**: Does the AI understand what the user really wanted?
- **Task Adherence**: Did the AI follow instructions and meet requirements?

#### **Safety Evaluators**
- **Content Safety**: Detects harmful, inappropriate, or unsafe content
- **Hate/Unfairness**: Identifies biased, discriminatory, or hateful responses

### **📈 Sample Results**
```
Evaluator Results (7 test cases):
✅ fluency: 100% (7/7 passed)
✅ retrieval: 100% (7/7 passed) 
⚠️ coherence: 71% (5/7 passed)
⚠️ relevance: 71% (5/7 passed)
```

### **🏆 Industry Best Practices**
This evaluation approach mirrors what major AI companies use:
- **Multi-dimensional assessment** (no single metric tells the whole story)
- **Automated scale** (evaluate thousands of responses quickly)
- **Human-AI alignment** (ground truth provides human benchmark)
- **Safety-first approach** (detect harmful content before deployment)

### **💡 Use Cases**
- **Model Comparison**: Test different AI models against same questions
- **Quality Assurance**: Validate AI responses before production deployment
- **Performance Monitoring**: Track AI quality over time
- **Safety Validation**: Ensure responses meet safety standards

## 🔧 Dependencies & Requirements

### Azure Services Required

This evaluation framework requires several Azure services to function properly:

#### **Azure OpenAI Service** ⭐ (Required)
- **Purpose**: Powers all LLM-based evaluators (Coherence, Fluency, Relevance, etc.)
- **Required Model**: GPT-4o (recommended) or GPT-4/GPT-4-turbo
- **Configuration**: 
  - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI resource endpoint
  - `AZURE_OPENAI_API_KEY`: Access key for the resource
  - `AZURE_OPENAI_DEPLOYMENT`: Deployment name (e.g., "gpt-4o")
- **Usage**: Core dependency for all evaluation operations

#### **Azure AI Foundry (AI Studio)** ⭐ (Required for Cloud Features)
- **Purpose**: Provides specialized evaluators and cloud deployment capabilities
- **Services Used**:
  - **Content Safety API**: For safety evaluators (Hate/Unfairness, Content Safety)
  - **Agent Evaluators**: Intent Resolution, Task Adherence
  - **Evaluation Pipeline**: Cloud deployment and result tracking
- **Configuration**:
  - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription
  - `AZURE_RESOURCE_GROUP`: Resource group containing AI Foundry project
  - `AZURE_AI_FOUNDRY_PROJECT`: AI Foundry project name
  - `PROJECT_ENDPOINT`: AI Foundry project endpoint URL

#### **Azure Machine Learning** (Required for Cloud Deployment)
- **Purpose**: Backend service for Azure AI Foundry evaluations
- **Usage**: Automatic integration through AI Foundry project
- **Authentication**: Uses same credentials as AI Foundry

### Python Dependencies

#### **Core Evaluation Libraries**
```python
azure-ai-evaluation      # Main evaluation framework
azure-identity           # Azure authentication
azure-ai-projects        # AI Foundry project integration
azure-ai-ml             # Machine Learning client (cloud deployment)
```

#### **Model Integration**
```python
openai                  # OpenAI API client for Azure OpenAI
promptflow-core         # Custom evaluator framework
promptflow-azure        # Azure integration for Promptflow
```

#### **Data Processing & Analysis**
```python
pandas                  # Data manipulation for results analysis
numpy                   # Numerical operations
json                    # JSON data handling
```

#### **Environment & Configuration**
```python
python-dotenv           # Environment variable management
typing-extensions       # Enhanced type hints
```

#### **Jupyter Notebook Support**
```python
notebook                # Jupyter notebook server
ipykernel              # Jupyter kernel
IPython                # Interactive Python
matplotlib             # Plotting and visualization
seaborn                # Statistical data visualization
```

### Authentication Requirements

#### **Azure CLI** (Required for Cloud Deployment)
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login

# Verify authentication
az account show
```

#### **Service Authentication Methods**
1. **Azure CLI Credentials** (Recommended for development)
   - Uses `az login` session
   - Automatic credential discovery
   - Works with both local and cloud scripts

2. **Service Principal** (Recommended for production)
   - Environment variables for automated deployment
   - `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`

3. **Managed Identity** (For Azure-hosted applications)
   - Automatic authentication when running on Azure
   - No credentials needed in code

### System Requirements

#### **Operating System**
- **Windows**: Windows 10/11 (primary support)
- **Linux**: Ubuntu 18.04+ / RHEL 8+ (community support)
- **macOS**: macOS 10.15+ (community support)

#### **Python Version**
- **Python 3.8+** (Required)
- **Python 3.10+** (Recommended for best compatibility)

#### **Hardware Requirements**
- **Memory**: 4GB RAM minimum, 8GB+ recommended
- **Storage**: 2GB free space for dependencies and results
- **Network**: Stable internet connection for Azure API calls

### Cost Considerations

#### **Azure OpenAI**
- **GPT-4o**: ~$0.005-0.015 per 1K tokens (input/output)
- **Evaluation Volume**: ~7 test cases × 10 evaluators = 70 API calls per run
- **Estimated Cost**: $0.10-0.50 per full evaluation run

#### **Azure AI Foundry**
- **Content Safety**: ~$0.001 per text transaction
- **Agent Evaluators**: Included in AI Foundry project quotas
- **Estimated Cost**: $0.01-0.05 per evaluation run

#### **Total Monthly Cost Estimate**
- **Development Usage**: $10-50/month (daily testing)
- **Production Usage**: $100-500/month (continuous monitoring)

> **💡 Cost Optimization Tips**: 
> - Use `run_evaluation_local.py` for development to minimize API calls
> - Reduce sample data size during testing
> - Use GPT-3.5-turbo for cost-sensitive scenarios (lower quality)

### Network & Security Requirements

#### **Outbound Connectivity Required**
```
Azure OpenAI:          *.openai.azure.com:443
Azure AI Foundry:      *.cognitiveservices.azure.com:443
Azure Management:      management.azure.com:443
Azure Storage:         *.blob.core.windows.net:443
```

#### **Data Privacy**
- All evaluation data is processed through your Azure tenant
- No data leaves your Azure subscription boundary
- Evaluation results stored in your AI Foundry project
- Local results saved to `output/` folder

#### **Compliance Features**
- **GDPR Compliant**: Data processing within Azure tenant
- **SOC 2 Type 2**: Azure service compliance
- **HIPAA**: Available with appropriate Azure configuration
- **Data Residency**: Configurable through Azure region selection

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
_env_create.bat

# Activate virtual environment (Windows)
_env_activate.bat
# OR for PowerShell: .venv\Scripts\Activate.ps1

# Install dependencies
_install.bat
```

### 2. Configuration
```bash
# Copy sample configuration
copy sample.env .env

# Edit .env file with your Azure credentials:
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_DEPLOYMENT (recommended: gpt-4o)
# - Azure AI Foundry project details
```

### 3. Run Evaluations
```bash
# Local evaluation (recommended for development)
python run_evaluation_local.py

# Cloud deployment (for production)
python run_evaluation_with_cloud_upload.py

# View results
jupyter notebook foundry_results_viewer.ipynb
```

## � Project Structure

```
ai-evals/
├── run_evaluation_local.py          # Main local evaluation script
├── run_evaluation_with_cloud_upload.py  # Cloud deployment script
├── model_endpoint.py                # Live agent integration endpoint
├── foundry_results_viewer.ipynb     # Results visualization notebook
├── requirements.txt                 # Python dependencies
├── sample.env                       # Environment configuration template
├── .env                            # Your configuration (create from sample.env)
├── _env_create.bat                 # Virtual environment setup
├── _env_activate.bat               # Environment activation
├── _install.bat                    # Dependency installation
├── data/
│   └── sample_data.jsonl          # Input test cases (7 scenarios)
├── output/                         # Output folder (timestamped results)
│   ├── foundry_rag_retrieval_results_*.jsonl
│   ├── foundry_agents_results_*.jsonl
│   ├── foundry_general_purpose_results_*.jsonl
│   ├── foundry_safety_security_results_*.jsonl
│   └── cloud_results_quality_only.json  # Cloud deployment results
├── friendliness/                   # Custom evaluator
│   ├── friendliness.py            # Friendliness evaluator implementation
│   └── friendliness.prompty       # Prompty template
└── images/                        # Documentation screenshots
```

## 💻 Usage Guide

### Input Data Format

The evaluation system reads from `data/sample_data.jsonl`. Each line contains:

```json
{
  "query": "User question or prompt",
  "context": "Reference documentation or background info",
  "response": "AI agent response to evaluate",
  "ground_truth": "Expected correct answer"
}
```

**Current Sample Data (7 test cases):**
- Items 1-5: Normal architecture questions and responses
- Item 6: Moderately problematic content (for safety testing)
- Item 7: Explicitly unsafe content (hate speech detection)

### Output Structure

Results are saved to `output/` with timestamps:

```
foundry_rag_retrieval_results_20250923_143022.jsonl
foundry_agents_results_20250923_143022.jsonl
foundry_general_purpose_results_20250923_143022.jsonl
foundry_safety_security_results_20250923_143022.jsonl
```

Each JSONL file contains:
```json
{
  "inputs": {...},
  "outputs": {
    "evaluator_name": {"score": 4.0, "reason": "..."},
    "another_evaluator": {"score": 3.5, "reason": "..."}
  }
}
```

### Running Different Evaluation Modes

#### 1. Local Development (Recommended)
```bash
python run_evaluation_local.py
```
**Features:**
- ✅ Runs all 10 evaluators locally
- ✅ Fast iteration for development
- ✅ Detailed console output with progress
- ✅ Saves results to timestamped JSONL files
- ✅ No cloud dependencies beyond Azure OpenAI

**Use Cases:**
- Development and testing
- Quick evaluation iterations
- Debugging evaluator behavior
- Offline evaluation

#### 2. Cloud Deployment (Production)
```bash
python run_evaluation_with_cloud_upload.py
```
**Features:**
- ✅ Deploys evaluators to Azure AI Foundry
- ✅ Uploads results to cloud project
- ✅ Enterprise-grade logging and tracking
- ✅ Supports distributed evaluation
- ✅ Integrates with Azure ML workflows

**Use Cases:**
- Production environments
- Team collaboration
- Compliance and audit trails
- Integration with Azure ML pipelines

**Prerequisites:**
- Azure CLI logged in (`az login`)
- Proper Azure permissions for AI Foundry
- All environment variables configured

### Viewing Results

#### 1. Jupyter Notebook Viewer
```bash
jupyter notebook foundry_results_viewer.ipynb
```
**Features:**
- ✅ Automatically finds latest results
- ✅ Loads all 4 categories into pandas DataFrames
- ✅ Clean visualization of scores and reasons
- ✅ Easy data exploration and analysis

#### 2. Direct File Analysis
Results are in standard JSONL format - read with any JSON tool:
```python
import json
import pandas as pd

# Load results
with open('output/foundry_rag_retrieval_results_latest.jsonl', 'r') as f:
    results = [json.loads(line) for line in f]

# Convert to DataFrame
df = pd.json_normalize(results)
```

### Customizing Evaluations

#### 1. Adding Your Own Test Data
Replace or extend `data/sample_data.jsonl`:
```json
{"query": "Your question", "context": "Your context", "response": "Your response", "ground_truth": "Expected answer"}
{"query": "Another question", "context": "More context", "response": "Another response", "ground_truth": "Another answer"}
```

#### 2. Connecting Live Agents
Modify `model_endpoint.py` to connect to your live agent:
```python
def __call__(self, query: str) -> Response:
    # Replace with your agent endpoint
    response = your_agent.generate(query)
    return {"query": query, "response": response}
```

#### 3. Custom Evaluators
Follow the pattern in `friendliness/`:
1. Create evaluator class with `__call__` method
2. Add prompty template if needed
3. Import and add to evaluation scripts

### Environment Configuration

#### Required Environment Variables
```bash
# Azure OpenAI (required for all evaluators)
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Azure AI Foundry (required for cloud deployment)
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_AI_FOUNDRY_PROJECT=your-project-name
PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
```

#### Optional Configuration
```bash
# Custom model settings
AZURE_OPENAI_DEPLOYMENT=gpt-4o  # Recommended model
# Alternative models: gpt-4, gpt-4-turbo, gpt-35-turbo
```

### Troubleshooting

#### Common Issues

**1. Authentication Errors**
```bash
# Ensure Azure CLI is logged in
az login
az account show

# Verify environment variables
echo $AZURE_OPENAI_ENDPOINT  # (PowerShell: $env:AZURE_OPENAI_ENDPOINT)
```

**2. Missing Dependencies**
```bash
# Reinstall requirements
pip install -r requirements.txt

# Check for conflicts
pip list | findstr azure
```

**3. Evaluation Failures**
- Check console output for specific evaluator errors
- Verify input data format in `sample_data.jsonl`
- Ensure all required fields (query, context, response, ground_truth) are present

**4. No Results Files**
- Check `output/` folder exists
- Verify write permissions
- Look for error messages in console output

#### Performance Tips

**1. Faster Development Iterations**
- Use `run_evaluation_local.py` for development
- Reduce sample data size for quick testing
- Focus on specific evaluator categories

**2. Production Optimization**
- Use `run_evaluation_with_cloud_upload.py` for scale
- Batch process large datasets
- Monitor Azure quota usage

**3. Cost Management**
- Use gpt-4o for best results, gpt-35-turbo for cost savings
- Monitor API usage in Azure portal
- Optimize input data length

## 🚀 Main Evaluation Scripts

### `run_evaluation_local.py` - Local Development Script

The **Local Evaluation Script** is the primary tool for development and testing:
**Features:**
- ✅ **Runs 10 active evaluators locally** across 4 categories
- ✅ **Reads from `data/sample_data.jsonl`** automatically
- ✅ **Generates 4 separate JSONL files** for each category
- ✅ **Provides detailed console output** with scores and results
- ✅ **Handles errors gracefully** with proper exception handling
- ✅ **Fast iteration** for development and testing

**Usage:**
```bash
python run_evaluation_local.py
```

**Output Files:**
Results are saved to `output/` with timestamp:
- `foundry_rag_retrieval_results_[timestamp].jsonl`
- `foundry_agents_results_[timestamp].jsonl`
- `foundry_general_purpose_results_[timestamp].jsonl`
- `foundry_safety_security_results_[timestamp].jsonl`

### `run_evaluation_with_cloud_upload.py` - Cloud Deployment Script

The **Cloud Evaluation Script** deploys evaluators to Azure AI Foundry for enterprise-grade evaluation:

**Key Features:**
- ✅ **9 core evaluators** with explicit Azure ML hub connection
- ✅ **Identity-based authentication** using Azure CLI credentials
- ✅ **Detailed status reporting** shows which evaluators succeed/fail
- ✅ **Cloud deployment** uploads results to Azure AI Foundry project
- ✅ **Enterprise integration** with Azure ML workflows
- ✅ **Production-ready** with enhanced error handling

**Evaluator Groups:**
1. **Core Evaluators** (most reliable): Groundedness, Relevance, Coherence, Fluency
2. **Advanced Evaluators**: Retrieval, Intent Resolution, Task Adherence  
3. **Safety Evaluators**: Hate/Unfairness, Content Safety

**Usage:**
```bash
python run_evaluation_with_cloud_upload.py
```

**Output:**
- **Cloud**: Results uploaded to your Azure AI Foundry project
- **Local**: Results saved to `output/` folder
- **Console**: Detailed status of which evaluators loaded successfully
- **Integration**: Available in Azure ML studio for further analysis

**Prerequisites:**
- Azure CLI logged in (`az login`)
- Azure AI Foundry project configured
- Proper Azure permissions for cloud deployment

## 🔍 RAG & Retrieval Evaluators (3)

These evaluators assess how well the system retrieves and uses information from knowledge bases.

### Retrieval ✅
- **Purpose**: Measures textual quality and relevance of retrieved context chunks for addressing the query (LLM-based, no ground truth required)
- **Implementation**: `RetrievalEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale with threshold=3
- **Key Features**: 
  - Evaluates how relevant context chunks are to the query
  - Assesses if most relevant chunks are surfaced at the top
  - No ground truth required (unlike DocumentRetrievalEvaluator)
  - Uses LLM for quality assessment vs. classical IR metrics
- **Use Case**: Evaluating RAG retrieval component effectiveness

### Groundedness ✅
- **Purpose**: Measures how consistent the response is with respect to the retrieved context
- **Implementation**: `GroundednessEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale (higher = better grounded in context)
- **Example**: Ensures architecture recommendations are based on provided reference material

### Relevance ✅
- **Purpose**: Measures how relevant the response is with respect to the query
- **Implementation**: `RelevanceEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale (higher = more relevant)
- **Example**: Ensures responses directly address the architecture questions asked

## 🤖 Agents Evaluators (2)

These evaluators assess agent-specific capabilities and behaviors.

### Intent Resolution ✅
- **Purpose**: Measures how accurately the agent identifies and addresses user intentions
- **Implementation**: `IntentResolutionEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale (higher = better intent understanding)
- **Example**: Evaluates if the agent correctly understands what the user wants to achieve
- **Note**: Experimental Azure AI evaluator

### Task Adherence ✅
- **Purpose**: Measures how well the agent follows through on identified tasks
- **Implementation**: `TaskAdherenceEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale (higher = better task completion)
- **Example**: Checks if the agent provides actionable solutions for architecture problems
- **Note**: Experimental Azure AI evaluator

## 🎯 General Purpose and Custom Evaluators (3)

These evaluators assess overall response quality and language characteristics.

### Coherence ✅
- **Purpose**: Measures logical consistency and flow of responses
- **Implementation**: `CoherenceEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale (higher = more coherent)
- **Example**: Ensures architecture recommendations follow logical reasoning

### Fluency ✅
- **Purpose**: Measures natural language quality and readability
- **Implementation**: `FluencyEvaluator` in `run_evaluation_local.py`
- **Scoring**: 1-5 scale (higher = more fluent)
- **Example**: Ensures architecture advice is clearly written and grammatically correct

### Friendliness ✅ (Custom Evaluator)
- **Purpose**: Measures conversational tone and helpfulness
- **Implementation**: `FriendlinessEvaluator` (custom evaluator) in `friendliness/friendliness.py`
- **Scoring**: 1-5 scale (higher = more friendly and helpful)
- **Example**: Ensures responses maintain a professional and helpful tone
- **Template**: Uses `friendliness.prompty` for structured evaluation

## 🛡️ Safety & Security Evaluators (2)

These evaluators detect potentially harmful or unsafe content using Azure's content safety services.

### Hate/Unfairness ✅
- **Purpose**: Identifies biased, discriminatory, or hateful content
- **Implementation**: `HateUnfairnessEvaluator` in `run_evaluation_local.py`
- **Scoring**: 0-7 scale (0-2 = safe, 3+ = unsafe)
- **Threshold**: 3 (scores ≥3 are flagged as "fail")
- **Output**: Provides detailed reasoning for scores

### Content Safety (Composite) ✅
- **Purpose**: Comprehensive assessment of various safety concerns in a single evaluator
- **Implementation**: `ContentSafetyEvaluator` in `run_evaluation_local.py`
- **Categories Covered**:
  - **Hate**: Discriminatory or biased content
  - **Sexual**: Inappropriate sexual content
  - **Violence**: Violent content or incitement
  - **Self-Harm**: Content promoting or describing self-harm
- **Scoring**: 0-7 scale per category (0-2 = safe, 3+ = unsafe)
- **Threshold**: 3 for all categories
- **Output**: Detailed breakdown of all safety categories with individual scores and reasons

## 📊 Evaluation Data

### Sample Data (`data/sample_data.jsonl`)
Contains **7 architecture-related scenarios** including:
- ✅ **Normal Cases**: Proper architecture questions and responses (Items 1-5)
- ✅ **Moderately Problematic**: Offensive but not explicitly hateful content (Item 6)
- ✅ **Explicitly Unsafe**: Hateful, discriminatory content for safety testing (Item 7)

### Data Structure
Each item contains:
```json
{
  "query": "User question",
  "context": "Reference documentation",
  "response": "Agent response", 
  "ground_truth": "Expected answer"
}
```

### 🔌 Live Agent Integration: `model_endpoint.py`

The **Model Endpoint** is a placeholder endpoint designed for integration with live agentic applications.

#### Current Usage (Static Data)
- ✅ Evaluation uses pre-generated responses from `sample_data.jsonl`
- ✅ Responses are stored as static text in the `"response"` field
- ✅ Good for testing and development with known data

#### Future Usage (Live Agent Integration)
- 🔄 **Connect to running agent**: Replace static responses with live agent calls
- 🔄 **Dynamic evaluation**: Pass `query` and `context` to live agent endpoint
- 🔄 **Real-time responses**: Get fresh responses for each evaluation run
- 🔄 **Production testing**: Evaluate actual agent performance in real scenarios


#### Benefits of Live Integration
- **🎯 Real Performance**: Evaluate actual agent behavior, not pre-written responses
- **🔄 Dynamic Testing**: Each run tests current agent state and capabilities  
- **📈 Continuous Monitoring**: Regular evaluation of deployed agents
- **🚀 Production Ready**: Bridge between development testing and production monitoring

#### Migration Path
1. **Phase 1**: Use static data for pipeline development ✅ (Current)
2. **Phase 2**: Integrate `model_endpoint.py` with your agentic application 🔄 (Future)
3. **Phase 3**: Switch evaluation pipeline to use live responses 🔄 (Future)
4. **Phase 4**: Set up continuous evaluation monitoring 🔄 (Future)

## 📈 Results Viewer: `foundry_results_viewer.ipynb`

Simple Jupyter notebook with **7 cells** that:
- ✅ **Automatically finds latest results** based on timestamp
- ✅ **Loads all 4 categories** into pandas DataFrames
- ✅ **Displays results** with shape information and full data
- ✅ **Minimal and clean** interface for quick result inspection

### Usage
1. Open `foundry_results_viewer.ipynb`
2. Run all cells
3. View DataFrames for each evaluation category

## 🎯 Key Insights from Our Testing

### Content Safety Effectiveness
Based on testing with problematic content (Items 6-7):

- ✅ **Intent/Task Evaluators**: Successfully identify problematic content (scores 1.0/5.0)
- ✅ **Hate/Unfairness Evaluator**: Correctly flags explicit hate speech (score 6, result: "fail")
- ✅ **Content Safety Composite**: Provides detailed breakdown:
  - Item 6 (moderate): Violence=3, others=0
  - Item 7 (explicit): Hate=6, Violence=4, others=0
- ✅ **Threshold System**: Scores ≥3 properly trigger "fail" results

### Quality Measurement
- ✅ **Multi-Dimensional**: Different evaluators catch different issues
- ✅ **Complementary**: Combining approaches provides comprehensive coverage
- ✅ **Actionable**: Results clearly indicate specific areas for improvement
- ✅ **Scalable**: Single script handles all evaluation categories efficiently

### Agent Behavior Detection
- ✅ **Intent Resolution**: Ranges from 1.0 (problematic content) to 5.0 (clear technical questions)
- ✅ **Task Adherence**: Shows degradation from 5.0 (complete answers) to 1.0 (inappropriate responses)
- ✅ **Correlation**: Agent evaluators correlate well with content safety findings

## 🔧 Getting Started

### Prerequisites
- Python 3.8+ installed
- Azure subscription with OpenAI and AI Foundry access
- Git (for cloning the repository)

### Step-by-Step Setup

#### 1. Clone and Setup Environment
```bash
# Clone the repository
git clone <repository-url>
cd ai-evals

# Create virtual environment
_env_create.bat

# Activate environment (Windows Command Prompt)
_env_activate.bat

# For PowerShell users:
.venv\Scripts\Activate.ps1

# Install dependencies
_install.bat
```

#### 2. Configure Azure Services
```bash
# Copy environment template
copy sample.env .env

# Edit .env file with your Azure credentials
notepad .env
```

**Required Configuration:**
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_AI_FOUNDRY_PROJECT=your-project-name
```

#### 3. Verify Setup
```bash
# Test Azure CLI authentication (for cloud deployment)
az login
az account show

# Verify environment variables
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('OpenAI Endpoint:', os.getenv('AZURE_OPENAI_ENDPOINT'))"
```

#### 4. Run Your First Evaluation
```bash
# Start with local evaluation
python run_evaluation_local.py

# Check results
dir output\

# View results in Jupyter
jupyter notebook foundry_results_viewer.ipynb
```

### Next Steps
1. **Customize Input Data**: Modify `data/sample_data.jsonl` with your test cases
2. **Connect Live Agent**: Update `model_endpoint.py` for dynamic evaluation
3. **Deploy to Cloud**: Use `run_evaluation_with_cloud_upload.py` for production
4. **Automate Workflows**: Set up CI/CD pipelines for continuous evaluation

## 📝 Configuration

### Azure Services Required
- **Azure OpenAI**: For LLM-based evaluators (GPT-4o recommended)
- **Azure AI Foundry**: For content safety and agent evaluators
- **Default Azure Credential**: For authentication

### Evaluation Thresholds
- **Safety Evaluators**: threshold=3 (scores ≥3 flagged as unsafe)
- **Quality Evaluators**: 1-5 scale (higher = better quality)
- **Agent Evaluators**: 1-5 scale (higher = better performance)

## 🏗️ Architecture

```
Azure AI Foundry Evaluation Pipeline
├── Input Layer
│   ├── data/sample_data.jsonl (test cases)
│   └── model_endpoint.py (live agent integration)
├── Evaluation Engine
│   ├── run_evaluation_local.py (development)
│   └── run_evaluation_with_cloud_upload.py (production)
├── Evaluator Categories
│   ├── RAG & Retrieval (3): Groundedness, Relevance, Retrieval
│   ├── Agents (2): Intent Resolution, Task Adherence
│   ├── General Purpose (3): Coherence, Fluency, Friendliness
│   └── Safety & Security (2): Hate/Unfairness, Content Safety
├── Output Layer
│   ├── output/ (timestamped JSONL files)
│   ├── Azure AI Foundry (cloud storage)
│   └── foundry_results_viewer.ipynb (visualization)
└── Configuration
    ├── .env (Azure credentials)
    ├── requirements.txt (dependencies)
    └── setup scripts (_env_*.bat, _install.bat)
```

This evaluation framework provides comprehensive coverage across all major aspects of AI agent quality, safety, and performance in a streamlined, easy-to-use pipeline. 

## 📁 Sample Results Files (Removed)

**Note:** The sample result files (`cloud_results_full_with_safety.json` and `cloud_results_quality_only.json`) have been removed to keep the project focused on actual evaluation workflows.

**Why removed?**
- ✅ **Cleaner organization**: Clear distinction between input data and output results
- ✅ **Reduced confusion**: No mixing of sample files with actual evaluation outputs
- ✅ **Better workflow**: Users focus on running evaluations rather than studying static examples

**Understanding Output Format:**
- Run `python run_evaluation_local.py` to see actual output format
- Check `output/` folder for timestamped results
- Use `foundry_results_viewer.ipynb` to explore result structure

**Previous Sample Files:**
- `cloud_results_full_with_safety.json` → Example with all 11 evaluators (including safety)
- `cloud_results_quality_only.json` → Example with 9 quality evaluators only

**Current Workflow:**
1. **Input**: `data/sample_data.jsonl` (your test cases)
2. **Processing**: Run evaluation scripts
3. **Output**: Timestamped JSONL files in `output/`
4. **Analysis**: Use Jupyter notebook for visualization

### Example Outputs on Azure AI Foundry

Below are sample evaluation outputs from running the run_evaluation_with_cloud_upload.py script as seen on Azure AI Foundry:
These screenshots demonstrate the comprehensive evaluation results across all categories, including safety scores, quality metrics, and agent performance measurements.

![Detailed Evaluation Metrics](/images/foundry-outputs-2.jpg)
![Foundry Evaluation Results](/images/foundry-outputs.jpg)

