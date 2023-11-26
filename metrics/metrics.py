class Comprison:
    def __init__(self, q_response, cq_response):
        self.response_int = 
        self.response_int_ext = 

    def forget_pct(self):
        element_forget = [element_int for element_int in self.response_int if element_int not in self.response_int_ext]
        return len(element_forget) / len(self.response_int)