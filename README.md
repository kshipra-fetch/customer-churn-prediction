
markdown
Copy code
# Customer Retention using Fetch.ai Agents and Machine Learning

This repository demonstrates how to integrate a machine learning model with Fetch.ai autonomous agents to make real-time customer-centric decisions. By embedding a customer churn prediction model into these agents, the system can identify potential churners and take proactive measures to retain them. 

## Setup and Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kshipra-fetch/customer-churn-prediction.git
   cd customer-churn-prediction

2. **Install Required Packages**
    ```bash
    pip install -r requirements.txt

3. **Train and Save the Model**\
Open and run Customer_Churn_Prediction.ipynb to train the model, apply pre-processing, and save the model and scaler.

4. **Configure Agents**\
Customer Retention Agent: Customize customer-retention-agent.py with ClickSend credentials.
Churn Prediction Agent: Ensure the paths for saved model and scaler are correct in churn-prediction-agent.py.
6. **Run the Agents**\
- Start the Customer Retention Agent and copy the address and paste in Churn Prediction Agent.
   ```bash
   python3 customer-retention-agent.py

- Start the Churn Prediction Agent in a separate terminal:
   ```bash
   python3 churn-prediction-agent.py
   ```

7. Run the following curl command in a new terminal to test the prediction agent:
   ```bash
   curl -d '{"CreditScore":619,"Geography":"France","Gender":"Female","Age":42,"Tenure":2,"Balance":0,"NumOfProducts":1,"HasCrCard":1,"IsActiveMember":1,"Complain":1,"SatisfactionScore":2}' \
     -H "Content-Type: application/json" \
     -X POST http://localhost:8000/rest/post
   ```
   
8. Check the logs for both agents to confirm that: 
- The prediction agent identifies churn and sends customer details to the retention agent.
- The retention agent generates an offer and logs the SMS response.

## Further Reading

For more details, check out the full article on Medium: [Integrating Machine Learning Models with Fetch.ai Agents for Smarter Decisions](https://medium.com/fetch-ai/integrating-machine-learning-models-with-fetch-ai-agents-for-smarter-decisions-1b1200f8fc51)