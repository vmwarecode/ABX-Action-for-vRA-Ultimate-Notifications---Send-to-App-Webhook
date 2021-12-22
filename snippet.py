# ABX Action to send to App Webhooks as part of ABX Flow: Ultimate Notifications
# Created by Guillermo Martinez and Dennis Gerolymatos 
# Version 1.2 - 22.12.2021

import requests # query the API
import json # API query responses to json.
def handler(context, inputs):
    # Variables
    zoom_token=context.getSecret(inputs["zoom_token"])
    
    # Sends Slack Notifications.
    if inputs['depInfoAndRes']['proGrpContent']['slack_notifications']['const']:
        body=   {
                        "username": "VMwareCodeBot",
                        "color": "Blue",
                        "type": "home",
                        "blocks": [
                            {
                                "type": "header",
                                "text": {
                                    "type": "plain_text",
                                    "text": f"{inputs['messageSubject']}"
                                }
                            },
                            {"type": "divider"},
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Deployment Name:*\n{inputs['depInfoAndRes']['name']}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Request Description:*\n{inputs['depInfoAndRes']['description']}."
                                    }
                                ]
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Creation Date: *\n{inputs['depInfoAndRes']['createdAt']}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Created By:*\n{inputs['depInfoAndRes']['createdBy']}"
                                    }
                                ]
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Deployment Owner:*\n{inputs['depInfoAndRes']['ownedBy']}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Deployment Status:*\n{inputs['depInfoAndRes']['status']}"
                                    }
                                ]
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Last Updated By :*\n{inputs['depInfoAndRes']['lastUpdatedBy']}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Last Updated At:*\n{inputs['depInfoAndRes']['lastUpdatedAt']}"
                                    }
                                ]
 
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Project Name :*\n{inputs['depInfoAndRes']['projectName']}"
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Deployment ID:*\n{inputs['depInfoAndRes']['id']}"
                                    }
                                ]
                            },
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f"*Request Details:*\n{inputs['depInfoAndRes']['requestDetails']}."
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": f"<https://{inputs['vra_fqdn']}/automation-ui/#/deployment-ui;ash=%2Fworkload%2Fdeployment%2F{inputs['deploymentId']}|Click here to see your request>"
                                    }
                                ]
                            },
                            {"type": "divider"}
                        ]
                    }
            
        headers={'Content-Type': 'application/json','accept': 'application/json'}
        resSlack=requests.post(inputs['depInfoAndRes']['proGrpContent']['slack_webhook']['const'], headers=headers, data=json.dumps(body), verify=False)
        if resSlack.status_code==200:
            print("Sending Slack Notification...")
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(resSlack.status_code, resSlack.content))
            
    # Sends Teams Notifications.
    if inputs['depInfoAndRes']['proGrpContent']['teams_notifications']['const']:
        body=       {
                        "@type": "MessageCard",
                        "themeColor": "0076D7",
                        "summary": "Create Deployments",
                        "sections": [{
                            "activityTitle": f"Task: {inputs['messageSubject']} ",
                            "activitySubtitle": f"Project: {inputs['depInfoAndRes']['projectName']}",
                            "facts": [
                                    {
                                    "name": "Owner",
                                    "value": f"{inputs['depInfoAndRes']['ownedBy']}"
                                },  {
                                    "name": "Deployment Name",
                                    "value": f"{inputs['depInfoAndRes']['name']}"
                                },  {
                                    "name": "Request Description",
                                    "value": f" {inputs['depInfoAndRes']['description']}"
                                },  {
                                    "name": "Request Details",
                                    "value": f" {inputs['depInfoAndRes']['requestDetails']}"
                                }, {
                                    "name": "Creation Date",
                                    "value": f"{inputs['depInfoAndRes']['createdAt']}"
                                }, {
                                    "name": "Last Updated at",
                                    "value": f"{inputs['depInfoAndRes']['lastUpdatedAt']}"
                                }, {
                                    "name": "Last Updated By",
                                    "value": f"{inputs['depInfoAndRes']['lastUpdatedBy']}"
                                }, {
                                    "name": "Created By",
                                    "value": f"{inputs['depInfoAndRes']['createdBy']}"
                                }, {
                                    "name": "Deployment ID",
                                    "value": f"{inputs['depInfoAndRes']['id']}"
                                },
                                {
                                    "name": "Status",
                                    "value": f"{inputs['depInfoAndRes']['status']}"
                                },
                                                                {
                                    "name": "Deployment URL",
                                    "value": f"https://{inputs['vra_fqdn']}/automation-ui/#/deployment-ui;ash=%2Fworkload%2Fdeployment%2F{inputs['deploymentId']}"
                                },
                                ],
                            "markdown": "true"
                        }]
                    }    
        
        headers={'Content-Type': 'application/json','accept': 'application/json'}
        resTeams=requests.post(inputs['depInfoAndRes']['proGrpContent']['teams_webhook']['const'], headers=headers, data=json.dumps(body), verify=False)
        if resTeams.status_code==200:
            print("Sending Teams Notification...")
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(resTeams.status_code, resTeams.content))
   
    # Sends Teams Notifications.
    if inputs['depInfoAndRes']['proGrpContent']['zoom_notifications']['const']:
        body={
				  "head": {
					"text": f"{inputs['messageSubject']}",
					"style":{
							"bold": "true"
							}
				  },
				  "body": [
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Deployment Name:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['name']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Request Description:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['description']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Request Details:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['requestDetails']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Creation Date:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['createdAt']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Creation By:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['createdBy']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Deployment Owner:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['ownedBy']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Deployment Status:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['status']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Last Updated By:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['lastUpdatedBy']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Last Updated At:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['lastUpdatedAt']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Project Name:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['projectName']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Deployment ID:",
						  "style":{
								"bold": "true"
								  }
						},
						{
						  "type": "message",
						  "text": f"{inputs['depInfoAndRes']['id']}"
						}
					  ]

					},
					{
					  "type": "section",
					  "sections": [
						{
						  "type": "message",
						  "text": "Click here to see your request:",
						  "link": f"https://{inputs['vra_fqdn']}/automation-ui/#/deployment-ui;ash=%2Fworkload%2Fdeployment%2F{inputs['deploymentId']}"
						}
					  ]

					}
				  ]
				}
        
        headers={'Content-Type': 'application/json','accept': '*/*','Authorization': "Bearer "+zoom_token}
        resZoom=requests.post(inputs['depInfoAndRes']['proGrpContent']['zoom_webhook']['const']+"?format=full", headers=headers, data=json.dumps(body), verify=False)
        if resZoom.status_code==200:
            print("Sending Zoom Notification...")
        else:
            print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(resZoom.status_code, resZoom.content))
        


