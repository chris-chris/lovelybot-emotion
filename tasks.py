from microsoftbotframework import ReplyToActivity
import requests
import json

# https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment
"""
POST
https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment

Ocp-Apim-Subscription-Key:4cfe6f744f1b486db3fa83d874bafdd9
Content-Type:application/json
Accept:application/json
"""

# https://api.korbit.co.kr/v1/ticker

def echo_response(message):
  if message["type"] == "message":
    if "bitcoin" in message["text"]:
      r = requests.get("https://api.korbit.co.kr/v1/ticker")
      bitcoin_price = r.json()["last"]
      msg = "bitcoin price is %s" % bitcoin_price
      print msg
      ReplyToActivity(fill=msg,
                    text=msg).send()
    else:
      data =  {
        "documents": [
          {
            "language": "en",
            "id": "1",
            "text": message["text"]
          }
        ]
      }
      headers = {'Ocp-Apim-Subscription-Key': '4cfe6f744f1b486db3fa83d874bafdd9',
                 'Content-Type': 'application/json',
                 'Accept': 'application/json',
                 }

      r = requests.post("https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment",
                        data=json.dumps(data),
                        headers=headers)
      emo_score = r.json()["documents"][0]["score"]
      msg = "emotion score is %s\n" % emo_score

      if emo_score > 0.5:
        msg = msg + "You look happy!"
      else:
        msg = msg + "You look unhappy.."

      print msg
      ReplyToActivity(fill=msg,
                      text=msg).send()
