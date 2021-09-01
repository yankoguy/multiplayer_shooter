file = open("D:\\Maor\\הורדותD\\גיא\\New folder\\TheMessage.txt", "rb").read()
result = ""
for char in file:
	if char == 32:
		result += "0"
	else:
		result += "1"
print(result)