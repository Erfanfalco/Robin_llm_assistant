import openai
import os

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Schema for the database
schema = '''
    Column_Name,Data_Type,Allow_Nulls
    Id,uniqueidentifier,Unchecked
    BackOfficeId,nvarchar(MAX),Checked
    State,int,Unchecked
    RequestNumber,int,Unchecked
    DbsAccountNumber,nvarchar(MAX),Checked
    PaymentDescription,nvarchar(MAX),Checked
    Amount,decimal(18, 2),Unchecked
    ShebaNumber,nvarchar(MAX),Checked
    IsIssued,bit,Unchecked
    CreateDate,datetime2(7),Unchecked
    RequestDate,datetime2(7),Unchecked
    PaymentRetryCount,int,Unchecked
    StarvationCount,int,Unchecked
    Created,datetime2(7),Unchecked
    CreatedBy,uniqueidentifier,Checked
    LastModified,datetime2(7),Checked
    LastModifiedBy,uniqueidentifier,Checked
    ConfirmState,int,Unchecked
    PersonalInfoId,uniqueidentifier,Checked
    PrxCustomer,bit,Unchecked
    '''


def chat_with_openai(question):
    """Send a question or command to the OpenAI API related to the schema."""
    query = f"""
    my table name is paymentRequests and the database's name is HamtaDb and in dbo,you must write only query without any redundant description,query should be efficient,
    Use the below SCHEMA for the financial manager's question or command,result of query should be TOP (100)  
    If the answer cannot be found, write "I don't know."

    SCHEMA:
    \"\"\"
    {schema}
    \"\"\"

    Question: {question}
    """

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": query}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"


# def convert_to_sql(natural_language_query):
#     """Convert natural language to SQL using OpenAI."""
#     try:
#         question = f"This is a command, convert the following to an SQL query: '{natural_language_query}'"
#         sql_query = chat_with_openai(question)
#         return sql_query
#     except Exception as e:
#         return f"Error: {str(e)}"


def main():
    """Main loop for interacting with the chat assistant."""
    print("Welcome to the financial assistant! Type 'exit' to quit.")

    while True:
        user_input = input("What's up?: ").strip()

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Check if the user wants to convert a natural language query to SQL
        # if user_input.lower().startswith("sql:"):
        #     natural_language_query = user_input[4:].strip()
        #     if not natural_language_query:
        #         print("Please provide a query after 'sql:'.")
        #         continue
        #
        #     sql_query = convert_to_sql(natural_language_query)
        #     print(f"SQL Query: {sql_query}")
        else:
            answer = chat_with_openai(user_input)
            print(f"Assistant: {answer}")


if __name__ == "__main__":
    main()
