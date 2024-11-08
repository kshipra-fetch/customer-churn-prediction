from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
import time

class CustomerDetails(Model):
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

class Response(Model):
    timestamp: int
    text: str
    agent_address: str

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
    name="Churn Prediction Agent",
    seed="churn-prediction-seed",    #Replace with your own seed phrase
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"]
)

fund_agent_if_low(agent.wallet.address())

customer_retention_agent_address="agent1qt5r492qwtpqa0v6nfugdw2lmpc8up02kyjw8y3wlshqqefzggsas85njw6"

@agent.on_rest_post("/rest/post", CustomerDetails, Response)
async def churn_prediction(ctx: Context, req: CustomerDetails) -> Response:
    ctx.logger.info("Received POST request")
    customer_data = pd.DataFrame([{
        'CreditScore': req.CreditScore,
        'Geography': req.Geography,
        'Gender': req.Gender,
        'Age': req.Age,
        'Tenure': req.Tenure,
        'Balance': req.Balance,
        'NumOfProducts': req.NumOfProducts,
        'HasCrCard': req.HasCrCard,
        'IsActiveMember': req.IsActiveMember,
        'Complain': req.Complain,
        'Satisfaction Score': req.SatisfactionScore
    }])

    # Map Gender column
    customer_data['Gender'] = customer_data['Gender'].map({'Female': 1, 'Male': 0})

    # One-hot encode Geography column to match specific format
    customer_data = pd.get_dummies(customer_data, columns=['Geography'], drop_first=True)

    # Ensure the columns are present, adding missing ones as needed
    for col in ['Geography_Germany', 'Geography_Spain']:
        if col not in customer_data.columns:
            customer_data[col] = 0

    # Final column order for consistency
    column_order = [
        'CreditScore', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
        'HasCrCard', 'IsActiveMember', 'Complain', 'Satisfaction Score',
        'Geography_Germany', 'Geography_Spain'
    ]
    customer_data = customer_data[column_order]
    ctx.logger.info(customer_data)

    loaded_scaler = joblib.load('scaler.save')

    # Use transform() instead of fit_transform() to scale customer_data based on training data ranges
    scaled_customer_data = pd.DataFrame(loaded_scaler.transform(customer_data), columns=customer_data.columns)

    # Load the SMOTE model
    loaded_model_smot = load_model("model_smot.h5")

    # Prediction with the SMOTE model
    smot_prediction = loaded_model_smot.predict(scaled_customer_data)
    prediction = smot_prediction.flatten() >= 0.5

    ctx.logger.info(f"SMOTE Model Prediction (Churn=1, No Churn=0):{prediction[0]}")

    customer_details = Notify(
        churn=True,
        CreditScore=req.CreditScore,
        Geography=req.Geography,
        Gender=req.Gender,
        Age=req.Age,
        Tenure=req.Tenure,
        Balance=req.Balance,
        NumOfProducts=req.NumOfProducts,
        HasCrCard=req.HasCrCard,
        IsActiveMember=req.IsActiveMember,
        Complain=req.Complain,
        SatisfactionScore=req.SatisfactionScore
    )

    if prediction == True:
        await ctx.send(customer_retention_agent_address, customer_details)

    return Response(
        text=f"Request has been processed",
        agent_address=ctx.agent.address,
        timestamp=int(time.time()),
    )

if __name__ == "__main__":
    agent.run()

