#Insert Card => PIN number => Select Account => See Balance/Deposit/Withdraw

import time

class ATM():
    def __init__(self):
        self.use_bank_api = False
        self.PIN = 123
        self.accounts = {0: 5, 1: 2}
        self.sel = -1
        self.state = "STANDBY"
        self.StateMachine()
        
    def StateMachine(self):
        while True:
            if self.state == "STANDBY":
                res = self.WaitForCard()
                if res:
                    self.state = "CARD_READY"
                else:
                    break
            elif self.state == "CARD_READY":
                res = self.GetPIN()
                if res:
                    self.state = "PIN_OK"
                else:
                    print("Wrong PIN!")
                    self.state = "STANDBY"
            elif self.state == "PIN_OK":
                res = self.SelectAccount()
                if res:
                    self.state = "ACCOUNT_CHOSEN"
                else:
                    self.state = "STANDBY"
            elif self.state == "ACCOUNT_CHOSEN":
                res = self.SelectAction()
                if res == 0:
                    self.state = "SHOW_BALANCE"
                elif res == 1:
                    self.state = "DEPOSIT"
                elif res == 2:
                    self.state = "WITHDRAW"
                else:
                    self.state = "STANDBY"
            elif self.state == "SHOW_BALANCE":
                print("Your balance is {:d}".format(self.accounts[self.sel]))
                self.sel = -1
                self.state = "STANDBY"
            elif self.state == "DEPOSIT":
                money = self.DepositMoney()
                if money>0:
                    self.accounts[self.sel] += money
                else:
                    print("Please enter a number > 0. Exiting.")
                self.sel = -1
                self.state = "STANDBY"
            elif self.state == "WITHDRAW":
                money = self.WithdrawMoney()
                if 0<money<=self.accounts[self.sel]:
                    self.accounts[self.sel] -= money
                elif money<=0:
                    print("Please enter a number > 0. Exiting.")
                else:
                    print("You don't have enough money in your account. Exiting.")
                self.sel = -1
                self.state = "STANDBY"
            else:
                print("Not valid")
                self.sel = -1
                self.state = "STANDBY"
            
            time.sleep(0.3)
        
        
    def WaitForCard(self):
        # UI function
        val = input("Insert your card (Y/N)? ")
        return val=='Y' or val=='y'
    
    def GetUserPINInput(self):
        # UI function
        val = input("Enter your PIN: ")
        return int(val)
        
    def BankAPI_CheckPIN(self, user_pin):
        # Bank API
        return False
            
    def CheckPIN(self, user_pin):
        if self.use_bank_api:
            return self.BankAPI_CheckPIN(user_pin)
        else:
            return user_pin == self.PIN
        
    def GetUserSelection(self):
        # UI function
        L = len(self.accounts)
        val = input("Choose account [{} ~ {}]: ".format(0, L-1))
        return int(val)
    
    def GetUserAction(self):
        # UI function
        # 0: SHOW_BALANCE, 1: DEPOSIT, 2: WITHDRAW, other: not valid
        val = input("Choose action (0: BALANCE, 1: DEPOSIT, 2: WITHDRAW): ")
        return int(val)
    
    def DepositMoney(self):
        # UI function
        val = input("How much to deposit: ")
        return int(val)
        
    def WithdrawMoney(self):
        # UI function
        val = input("How much to withdraw: ")
        return int(val)
        
    
    def GetPIN(self):
        user_pin = self.GetUserPINInput()
        return self.CheckPIN(user_pin)
            
    def SelectAccount(self):
        L = len(self.accounts)
        if L==0:
            print("You have no accounts. Now exiting.")
            return False
        else:
            sel = self.GetUserSelection()
            if sel>L-1: # n should be [0, L-1]
                print("Bad selection. Now exiting.")
                return False
            else:
                self.sel = sel
                return True

    
    def SelectAction(self):
        return self.GetUserAction()
            
        
def main():
    atm = ATM()
    
    
if __name__=="__main__":
    main()
