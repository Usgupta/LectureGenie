import requests, json

token = "<NOTION-API-KEY>"

databaseId = '<NOTION-DATABASE-KEY>'

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def createPage(page_title, content, databaseId=databaseId, headers=headers):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId },
        "properties": {
           "Name": {
            "title": [
                {   "text": {
                        "content": page_title
                    }
                }
            ]
            }
        },

        "Content": {
            "rich_text": [
                {
                    "text": {
                        "content": "content"
                    }
                }
            ]
        }

    }
    
    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    text_block = {
    "type": "paragraph",
    "paragraph": {
      "text": [{
        "type": "text",
        "text": {
          "content": content,
        }
      }]
    }
  }

    

    # print(res.status_code)
    # print(res.text)
    result = json.loads(res.text)
    append_child_blocks(result['id'], [text_block],headers)
   
    return result["url"]

def append_child_blocks(parent_id: str, children,headers):
    url = "https://api.notion.com/v1"+ f"/blocks/{parent_id}/children"
    response = requests.request("PATCH",url,headers=headers,json={"children": children})
    return response.text



