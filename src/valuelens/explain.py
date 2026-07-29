import shap

def explain_customer(customer_id, model, X, df):
    explainer = shap.TreeExplainer(model)
    row_index = df[df['Customer ID'] == customer_id].index[0]
    shap_values = explainer(X)
    return shap_values[row_index]