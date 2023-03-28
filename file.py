# using flask_restful
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
  
# creating the flask app
app = Flask(__name__)

# creating an API object
api = Api(app)


# Creating runningBalance-schema :- (with attributes as given in problem-statement)

class runningBalance:
    def __init__(self, wallet, gold, goldPrice):
        self.wallet = wallet
        self.gold = gold
        self.goldPrice = goldPrice

# Creating walletTransaction-schema :-

class walletTransaction:
    def __init__(self, userId, amount, type, status, runningBalance, transaction, createdAt, updatedAt):
        self.userId = userId
        self.amount = amount
        self.type = type
        self.status = status
        self.runningBalance = runningBalance
        self.transaction = transaction
        self.createdAt = createdAt
        self.updatedAt = updatedAt

# Creating user-schema :-

class user:
    def __init__(self, userId, firstName, lastName, password, mobileNumber, country, email, runningBalance):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.mobileNumber = mobileNumber
        self.country = country
        self.email = email
        self.runningBalance = runningBalance

# Creating goldTransaction-schema :-

class goldTransaction:
    def __init__(self, userId, entityUser, quantity, amount, type, status, runningBalance, createdAt, updatedAt):
        self.userId = userId
        self.entityUser = entityUser
        self.quantity = quantity
        self.amount = amount
        self.type = type
        self.status = status
        self.runningBalance = runningBalance
        self.createdAt = createdAt
        self.updatedAt = updatedAt

# Making lists of some dummy-user(s) and dummy-transaction(s), can add multiple if required.

allUsers = []
allGoldTransactions = []
u1 = user('5', 'per', 'son1', 'pswd', '1234', 'India', 'p1@abc.com', runningBalance(1000, 5, 100))
allUsers.append(u1)
gt1 = goldTransaction(5, '5', 5, 100, 'DEBIT', 'SUCCESS', 1000, 'today', 'today')
allGoldTransactions.append(gt1)


# Function executing a gold-transaction, involving user-schema & goldTransaction-schema

def doGoldTransaction(temp):
    # Update (user-id)'s data
    print('Transaction happening')
    if(temp.status == 'SUCCESS'):
        for u in allUsers:
            if(u.userId == temp.userId):
                print('user found', u.userId)
                # update runningBalance of user
                if(temp.type == "CREDIT"):
                    print(u.runningBalance)
                    u.runningBalance.gold = (u.runningBalance.gold + temp.quantity)
                    print(u.runningBalance)
                else:
                    if(temp.quantity > u.runningBalance.gold):
                        u.runningBalance.gold = 0
                    else:
                        u.runningBalance.gold -= temp.quantity
    else:
        # FAILED or WAITING  ==>  FAILING transaction
        return



def doWalletTransaction(temp):
    print('Wallet Transaction happening')
    if(temp.status == 'SUCCESS'):
        for u in allUsers:
            if(u.userId == temp.userId):
                print('user found here too ', u.userId)
                # update runningBalance of user
                if(temp.type == "CREDIT"):
                    print(u.runningBalance)
                    u.runningBalance.wallet = (u.runningBalance.wallet + temp.amount)
                    print(u.runningBalance)
                else:
                    if(temp.amount > u.runningBalance.wallet):
                        u.runningBalance.wallet = 0
                    else:
                        u.runningBalance.wallet -= temp.amount
    else:
        # FAILED or WAITING  ==>  FAILING transaction
        return



class nauggets(Resource):
    
    def get(self, num):
        # Calculate previous-fund of all users combined (i.e. before current-transactions take place)
        prev=0
        curr=0
        for u in allUsers:
            prev += u.runningBalance.wallet
            prev += (u.runningBalance.gold * u.runningBalance.goldPrice)

        temp = goldTransaction('5', '5', 1, 500, 'DEBIT', 'SUCCESS', allUsers[0].runningBalance, 'today', 'today')
        temp2 = walletTransaction('5', 400, 'CREDIT', 'SUCCESS', 1000, '5', 'today', 'today')
        doGoldTransaction(temp)
        doWalletTransaction(temp2)

        # Calculate current-fund of all users combined (after all transactions has taken place)
        for u in allUsers:
            curr += u.runningBalance.wallet
            curr += (u.runningBalance.gold * u.runningBalance.goldPrice)

        # Now, calculating the metrics needed, as asked in the problem statement.
        netFundAdded = 0
        if(curr > prev):
            netFundAdded = (curr - prev)
        netChange = (curr - prev)
        gainOrLossPercentage = (((curr-prev) / prev) * 100)
        changePercentage = str(gainOrLossPercentage) + "%"

        # Returning the metrics-result as JSON object.
        return jsonify({'netFundAdded': netFundAdded}, {'currentFund': curr}, {'netGrowthOrLoss': netChange}, {'gainOrLossPercentage': changePercentage})
  


# In future, we can add user-id to execute an API-request.
api.add_resource(nauggets, '/nauggets/<int:num>')
# Currently, I've just created a dummy link, to execute the API-request.
# You can try out the (link in terminal + "/nauggets/x") , where x is any integer


# driver function
if __name__ == '__main__':
  
    app.run(debug = True)

