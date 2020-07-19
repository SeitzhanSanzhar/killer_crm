Solution: basically I just keep PriorityQueue to every time extract most prior target, after I see is there any new targets can be added to PQ and then I repeat this steps while I have something in my PQ
 
Dockerfiles can be found in this repo


purchase_request/ - requires xml file with targets information, returns json in the statement if success otherwise failure reason

login/ - requires username & password and returns Token

logout/ - just logout

contract_list/ - returns list of all contract with the information about all victims

pay_contract/ - requires contract_Id & amount of money, returns success if correct amount of money otherwise failure reason

get_success_payments/ - get all the success payments