purchase_request/ - requires xml file with targets information, returns json in the statement if success otherwise failure reason

login/ - requires username & password and returns Token

logout/ - just logout

contract_list/ - returns list of all contract with the information about all victims

pay_contract/ - requires contract_Id & amount of money, returns success if correct amount of money otherwise failure reason

get_success_payments/ - get all the success payments