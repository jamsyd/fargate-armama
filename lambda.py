
def lambda_handler(event, context):

    import json
    import boto3
      
    # Opening JSON file
    f = open('settings.json')
    
    # Load in the data
    input_data = json.load(f)


    # Send messages
    for ticker in input_data:
        sqs = boto3.client('sqs')      
        sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/732559080652/jamsyd-arma-ma.fifo",
            MessageAttributes={
                        'ticker': {
                            'DataType': 'String',
                            'StringValue': ticker
                        },
                        'order': {
                            'DataType': 'String',
                            'StringValue': input_data[ticker]['order']
                        },
                        'trainDFLength': {
                            'DataType': 'Number',
                            'StringValue': '252'
                        },
                        'column': {
                            'DataType': 'String',
                            'StringValue': 'Close'
                        },
                        'forecastHorizon': {
                            'DataType': 'Number',
                            'StringValue': '5'
                        },

                    },
            MessageBody=('Test run for arma-ma'),
            MessageGroupId="jamsyd-arma-ma-fargate",
        )
    print(ticker)

    # Closing file
    f.close()
    
    return {
        'statusCode': 200,
        'body': "Success"
    }