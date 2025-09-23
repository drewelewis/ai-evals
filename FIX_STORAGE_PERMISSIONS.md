# Fix Azure AI Foundry Storage Upload Issue

## Problem
Your evaluations run successfully but fail to upload to Azure AI Foundry with this error:
```
❌ Cloud deployment failed: (UserError) Failed to upload evaluation run to the cloud due to insufficient permission to access the storage.
```

## Root Cause
Azure AI Foundry projects need:
1. A connected storage account for evaluation data
2. Proper permissions for the project to write to that storage

## Step-by-Step Fix

### Step 1: Check Your Project Type
First, verify you have an **Azure AI Foundry project** (not a hub-based project):

1. Go to [ai.azure.com](https://ai.azure.com)
2. Navigate to your project: `ai-evals-project`
3. Look for "Management Center" in the bottom left corner
   - ✅ If you see "Management Center" → You have a Foundry project (correct)
   - ❌ If you don't see it → You have a hub-based project (needs migration)

### Step 2: Connect Storage Account to Your Project

1. **Navigate to your project** at [ai.azure.com](https://ai.azure.com)
2. **Go to Management Center** (bottom left corner)
3. **Select "Connected Resources"** under your Resource (NOT Project)
4. **Click "New connection"**
5. **Select "Storage account"**
6. **Search for and select your storage account** (or create new one)
7. **Authentication method**: Select "Microsoft Entra ID" (recommended)
8. **Click "Add Connection"**

### Step 3: Grant Storage Permissions

1. **Go to Azure Portal** → Navigate to your storage account
2. **Select "Access Control (IAM)"** on the left side
3. **Click "+ Add" → "Add role assignment"**
4. **Role Tab**: Search for and select **"Storage Blob Data Contributor"**
5. **Members Tab**: 
   - Assign access to: **"Managed identity"**
   - Click **"+ Select members"**
   - Subscription: Your subscription
   - Managed identity: **"All system-assigned managed identities"**
   - Search for your project name: `ai-evals-project`
   - **Important**: Select the one formatted as `[ResourceName]/[ProjectName]` 
   - **Don't select** the resource name without the `/[ProjectName]`
6. **Click "Select"** → **"Review + assign"** → **"Review + assign"** again

### Step 4: Wait and Test
- Wait 5-10 minutes for permissions to propagate
- Run your evaluation script again

## Alternative: Use Local-Only Evaluation

If you want to skip cloud upload for now:

```bash
python run_evaluation_local.py
```

This saves results to the `output/` folder without requiring cloud storage permissions.

## Verification Commands

After setting up permissions, you can verify:

```bash
# Check your Azure login
az account show

# Check storage permissions (if you have Azure CLI storage extension)
az storage account show --name [your-storage-account] --resource-group ai-evals-rg
```

## Additional Permissions Needed

Your user account might also need:
- `Microsoft.Storage/storageAccounts/listAccountSas/action` permission
- **Storage Blob Data Owner** role (if using Microsoft Entra ID authentication)

## Common Issues

1. **Selected wrong managed identity**: Make sure you select `[ResourceName]/[ProjectName]`, not just the resource name
2. **Permissions not propagated**: Wait 5-10 minutes after adding permissions
3. **Wrong authentication method**: Use Microsoft Entra ID, not access keys
4. **Storage account not connected to resource**: Must be connected at the **Resource** level, not Project level

## Resources
- [Azure AI Foundry Storage Account Setup](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/evaluations-storage-account)
- [Cloud Evaluation Prerequisites](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/cloud-evaluation#prerequisites)