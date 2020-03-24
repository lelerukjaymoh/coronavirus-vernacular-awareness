import africastalking

class SMS:
	def __init__(self):
		# Set your app credentials
		self.username = "coronavirus"
		self.api_key = "d9db994263bb40651311842a76b9935709989ddeceab55c0798de7809291d864"
		# Initialize the SDK
		africastalking.initialize(self.username, self.api_key)
		# Get the SMS service
		self.sms = africastalking.SMS

	def send(self, phone, message):
		# Set the numbers you want to send to in international format
		recipients = phone

		# Set your message
		print(message)
		message = message;

		# Set your shortCode or senderId
		# sender = "K"
		try:
			# Thats it, hit send and we'll take care of the rest.
			response = self.sms.send(message, recipients)
			print(response)
			return response
		except Exception as e:
			print ('Encountered an error while sending: %s' % str(e))
