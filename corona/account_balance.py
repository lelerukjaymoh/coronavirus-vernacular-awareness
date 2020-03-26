import africastalking

class APPLICATION_DATA:
    def __init__(self):
		# Set your app credentials
        self.username = "coronavirus"
        self.api_key = "d9db994263bb40651311842a76b9935709989ddeceab55c0798de7809291d864"

		# Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the application service
        self.application = africastalking.Application

    def fetchdata(self):
        try:
			# Fetch the application data
            res = self.application.fetch_application_data()
            print (res)
            return res['UserData']['balance']
        except Exception as e:
            print ("Received error response:%s" %str(e))