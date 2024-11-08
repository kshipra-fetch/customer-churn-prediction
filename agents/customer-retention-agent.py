from uagents import Model, Context, Agent
from uagents.setup import fund_agent_if_low
import requests
import json
from requests.auth import HTTPBasicAuth
from openai import OpenAI

class Notify(Model):
    churn: bool
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: int
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    Complain: int
    SatisfactionScore: int



agent = Agent(
    name="customer-retention-agent",
    seed="customer-retention-agent-seed",
    port=8001,
    endpoint=f"http://localhost:8001/submit"
)

fund_agent_if_low(agent.wallet.address())


async def generate_an_offer(credit_score, geography, gender, age, tenure, balance, num_of_products, has_cr_card,
                            is_active_member, complain, satisfaction_score):
    # Construct the prompt with customer information
    prompt = f"""
    A bank customer is at risk of leaving the bank. Here are their details:
    - Credit Score: {credit_score}
    - Geography: {geography}
    - Gender: {gender}
    - Age: {age}
    - Tenure with bank: {tenure} years
    - Account Balance: ${balance}
    - Number of Products: {num_of_products}
    - Has Credit Card: {"Yes" if has_cr_card else "No"}
    - Is Active Member: {"Yes" if is_active_member else "No"}
    - Has a Complaint: {"Yes" if complain else "No"}
    - Satisfaction Score: {satisfaction_score} (out of 5)

    Based on this information, create a polite, engaging, and personalized message that the bank can send directly to this customer. The message should offer specific benefits or incentives that would be most appealing based on their profile, such as fee waivers, extra reward points, or special loyalty programs. The goal is to encourage the customer to stay with the bank. Please make the message very concise and start the message with Dear Sir/Ma'am and End it with Warm Regards ABC Bank
    """

    # Make the GPT API call
    client = OpenAI()  # Ensure you have instantiated the OpenAI client correctly
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract and return the generated offer message
    offer_text = response.choices[0].message.content.strip()
    return offer_text

async def notify_family(message):
    username = "xxxxxxxxxxxx"
    api_key = "xxxxxxxxxxxxxx"

    # The ClickSend SMS API URL
    url = 'https://rest.clicksend.com/v3/sms/send'

    # The payload containing the message details
    payload = {
        "messages": [
            {
                "source": "python",
                "body": message,
                "to": "+4499999999",
                "from": "PythonApp"
            }
        ]
    }

    # Send the POST request to the ClickSend API
    response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'},
                             auth=HTTPBasicAuth(username, api_key))

    # Check if the request was successful
    if response.status_code == 200:
        print('Message sent successfully!')
        print(response.json())
    else:
        print(f'Failed to send message. Status code: {response.status_code}')
        print(response.json())


@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)

@agent.on_message(model=Notify)
async def send_message(ctx: Context, sender: str, msg: Notify):
    ctx.logger.info(msg.churn)
    ctx.logger.info(msg.CreditScore)

    offer=await generate_an_offer(msg.CreditScore,msg.Geography,msg.Gender,msg.Age,msg.Tenure,msg.Balance,msg.NumOfProducts,msg.HasCrCard,msg.IsActiveMember,msg.Complain,msg.SatisfactionScore)
    print(offer)
    await notify_family(offer)



if __name__ == "__main__":
    agent.run()
