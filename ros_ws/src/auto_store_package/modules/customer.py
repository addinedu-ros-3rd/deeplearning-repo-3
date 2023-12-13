class Customer:
    def __init__(self, customer_id, pay_id, in_time):
        self.id = customer_id
        self.pay_id = pay_id
        
        self.checkIn_state = False
        self.shopping_state = False
        self.action_state = None
        
        self.in_time = in_time
        self.out_time = None

        self.shopping_list = {}
        self.total_price = 0
    
    def start_shopping(self):
        self.shopping_state = True

    def stop_shopping(self):
        self.shopping_state = False

    def update_action_state(self, action_type):
        self.action_state = action_type

    def update_out_time(self, out_time):
        self.out_time = out_time

    def update_shopping_list(self, fruit_type, number):
        self.shopping_list[fruit_type] = number
    
    def calc_total_price(self, price_list):
        self.total_price = 0