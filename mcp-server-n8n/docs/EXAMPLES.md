# n8n MCP Server - Example Usage Scenarios

This document provides real-world examples of using Claude with the n8n MCP server to create and manage workflows.

## Getting Started Examples

### Example 1: List All Workflows

**Human:** Show me all my n8n workflows

**Claude's Action:**
```
Uses tool: list_workflows
```

**Result:** Gets a list of all workflows with their IDs, names, and active status

### Example 2: Create a Simple Notification Workflow

**Human:** Create a workflow that sends me a Slack message when I manually trigger it

**Claude's Response:**

I'll create a simple manual trigger workflow with a Slack notification.

**Claude's Action:**
```json
Uses tool: create_workflow
{
  "name": "Manual Slack Notification",
  "nodes": [
    {
      "name": "When clicking 'Test workflow'",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {}
    },
    {
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 1,
      "position": [450, 300],
      "parameters": {
        "channel": "#general",
        "text": "Workflow triggered successfully!",
        "otherOptions": {}
      },
      "credentials": {
        "slackApi": {
          "id": "1",
          "name": "Slack account"
        }
      }
    }
  ],
  "connections": {
    "When clicking 'Test workflow'": {
      "main": [
        [
          {
            "node": "Slack",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false
}
```

## Advanced Workflow Creation

### Example 3: Daily Weather Report

**Human:** Create a workflow that:
1. Runs every day at 8 AM
2. Gets the weather for New York City
3. Sends the forecast to Slack

**Claude's Response:**

I'll create an automated daily weather report workflow for you.

**Claude's Action:**
```json
Uses tool: create_workflow
{
  "name": "Daily Weather Report - NYC",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 24,
              "triggerAtHour": 8,
              "triggerAtMinute": 0
            }
          ]
        }
      }
    },
    {
      "name": "OpenWeatherMap",
      "type": "n8n-nodes-base.openWeatherMap",
      "typeVersion": 1,
      "position": [450, 300],
      "parameters": {
        "operation": "currentWeather",
        "cityName": "New York City",
        "format": "json"
      },
      "credentials": {
        "openWeatherMapApi": {
          "id": "2",
          "name": "OpenWeatherMap account"
        }
      }
    },
    {
      "name": "Format Message",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [650, 300],
      "parameters": {
        "values": {
          "string": [
            {
              "name": "message",
              "value": "=Good morning! Today's weather in NYC:\n🌡️ Temp: {{$json.main.temp}}°F\n☁️ Conditions: {{$json.weather[0].description}}\n💨 Wind: {{$json.wind.speed}} mph"
            }
          ]
        }
      }
    },
    {
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 1,
      "position": [850, 300],
      "parameters": {
        "channel": "#weather",
        "text": "={{$json.message}}"
      },
      "credentials": {
        "slackApi": {
          "id": "1",
          "name": "Slack account"
        }
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "OpenWeatherMap", "type": "main", "index": 0}]]
    },
    "OpenWeatherMap": {
      "main": [[{"node": "Format Message", "type": "main", "index": 0}]]
    },
    "Format Message": {
      "main": [[{"node": "Slack", "type": "main", "index": 0}]]
    }
  },
  "active": true
}
```

### Example 4: API Data Aggregator

**Human:** Build a workflow that:
1. Triggers every hour
2. Fetches data from 3 different APIs
3. Combines the results
4. Saves to a Google Sheet

**Claude's Response:**

I'll create a multi-source data aggregation workflow with Google Sheets integration.

*Claude creates a workflow with:*
- Cron Trigger (every hour)
- 3 HTTP Request nodes (parallel)
- Merge node (to combine data)
- Function node (to format data)
- Google Sheets node (to append rows)

## Workflow Modification Examples

### Example 5: Add Error Handling

**Human:** Add error notification to my "Daily Weather Report - NYC" workflow

**Claude's Action:**
1. Uses `get_workflow` to retrieve the current workflow
2. Analyzes the structure
3. Uses `update_workflow` to add:
   - Error trigger node
   - Slack notification for errors
   - Updated connections

### Example 6: Modify Schedule

**Human:** Change the daily report to run at 6 AM instead of 8 AM

**Claude's Action:**
```
Uses tool: get_workflow (to find the workflow)
Uses tool: update_workflow (to modify the schedule trigger)
```

## Execution and Monitoring Examples

### Example 7: Execute and Monitor

**Human:** Run the "API Data Sync" workflow and tell me if it completed successfully

**Claude's Actions:**
1. Uses `execute_workflow` to trigger the workflow
2. Gets the execution ID from the response
3. Uses `get_execution` to check the status
4. Reports back:
   - Execution status (success/error)
   - Duration
   - Any error messages if failed
   - Summary of results

### Example 8: Check Recent Failures

**Human:** Show me all failed workflow executions from the past day

**Claude's Action:**
```
Uses tool: list_executions
{
  "status": "error",
  "limit": 50
}
```

Then analyzes and summarizes the failures.

## Discovery and Learning Examples

### Example 9: Discover Available Nodes

**Human:** What email services can I use in n8n?

**Claude's Actions:**
1. Uses `list_node_types`
2. Filters for email-related nodes
3. Lists: Gmail, Outlook, SendGrid, Mailgun, SMTP, etc.
4. Explains capabilities of each

### Example 10: Understand Existing Workflow

**Human:** Explain what my "Customer Onboarding" workflow does

**Claude's Actions:**
1. Uses `get_workflow` with the workflow ID
2. Analyzes the nodes and connections
3. Provides a human-readable explanation:
   - Trigger conditions
   - Data transformations
   - External services used
   - Final outcomes

## Complex Multi-Step Examples

### Example 11: Complete Automation Setup

**Human:** I want to automate my customer onboarding. When someone fills out our TypeForm:
1. Create a record in Airtable
2. Send them a welcome email
3. Add them to our Mailchimp list
4. Create a Slack message for our team
5. Create a Trello card for follow-up

**Claude's Response:**

I'll create a comprehensive customer onboarding automation workflow.

*Claude creates a workflow with:*
- Typeform Trigger (webhook)
- Airtable node (create record)
- Gmail/SendGrid node (welcome email)
- Mailchimp node (add subscriber)
- Slack node (team notification)
- Trello node (create card)
- Error handling with notifications
- All properly connected and configured

### Example 12: Data Pipeline

**Human:** Create a data pipeline that:
1. Monitors a Google Sheet for new rows
2. Validates the data
3. Enriches it with data from an external API
4. Transforms it to match our database schema
5. Inserts it into PostgreSQL
6. Logs everything to a monitoring dashboard

**Claude's Response:**

I'll build a complete data pipeline with validation, enrichment, and logging.

*Claude creates a sophisticated workflow with:*
- Google Sheets Trigger (polling)
- Function node (validation logic)
- HTTP Request node (API enrichment)
- Multiple Function nodes (transformations)
- PostgreSQL node (insertion)
- HTTP Request node (logging to dashboard)
- Error handling and retry logic

## Debugging Examples

### Example 13: Troubleshoot Failed Workflow

**Human:** My "Daily Backup" workflow is failing. Can you help debug it?

**Claude's Actions:**
1. Uses `list_executions` to find recent failures
2. Uses `get_execution` to analyze the error
3. Uses `get_workflow` to review the configuration
4. Identifies the issue (e.g., invalid credentials, wrong API endpoint)
5. Suggests fixes
6. Can use `update_workflow` to apply fixes if requested

### Example 14: Performance Optimization

**Human:** My workflow is taking too long. Can you optimize it?

**Claude's Actions:**
1. Uses `get_workflow` to analyze the structure
2. Identifies bottlenecks:
   - Sequential operations that could be parallel
   - Unnecessary data transformations
   - Inefficient API calls
3. Suggests optimizations
4. Can implement changes with `update_workflow`

## Bulk Operations Examples

### Example 15: Activate Multiple Workflows

**Human:** Activate all my workflows that have "Production" in the name

**Claude's Actions:**
1. Uses `list_workflows` to get all workflows
2. Filters for workflows with "Production" in name
3. Uses `activate_workflow` for each match
4. Reports results

### Example 16: Clean Up Old Executions

**Human:** Delete all failed executions older than 7 days

**Claude's Actions:**
1. Uses `list_executions` with status filter
2. Filters by date
3. Uses `delete_execution` for each match
4. Reports number of deletions

## Integration Examples

### Example 17: Migrate Workflow

**Human:** Copy my "Email Digest" workflow from the development instance to production

**Claude's Response:**

I'll help you migrate the workflow. First, I need access to both instances. Let me:
1. Export from dev (uses `get_workflow`)
2. Import to prod (uses `create_workflow` on prod instance)
3. Verify and report

### Example 18: Backup All Workflows

**Human:** Export all my workflows as JSON for backup

**Claude's Actions:**
1. Uses `list_workflows` to get all workflows
2. Uses `get_workflow` for each to get full details
3. Combines into a backup file
4. Provides the backup data

## Best Practices from Examples

1. **Always activate explicitly**: Workflows are created inactive by default
2. **Include error handling**: Add error triggers and notifications
3. **Use descriptive names**: Both for workflows and nodes
4. **Test before activating**: Use `execute_workflow` to test
5. **Monitor executions**: Regularly check `list_executions` for issues
6. **Document complex logic**: Use note nodes or workflow descriptions
7. **Version control**: Keep backups of important workflows

## Tips for Effective Prompts

### Good Prompts

- "Create a workflow that does X when Y happens"
- "Add error handling to my workflow named Z"
- "Show me all workflows that are currently active"
- "Execute workflow X and tell me the result"

### Less Effective Prompts

- "Make a workflow" (too vague)
- "Fix my workflow" (need to specify which one)
- "Set up automation" (need more details)

### Pro Tips

1. **Be specific about triggers**: "daily at 8 AM" vs "regularly"
2. **Mention services by name**: "Slack" vs "messaging"
3. **Specify data flow**: "fetch → transform → send"
4. **Include error handling needs**: "notify me if it fails"
5. **State activation preference**: "activate immediately" or "leave inactive"

---

These examples demonstrate the power of combining Claude's AI capabilities with n8n's workflow automation through the MCP server. The possibilities are endless!
