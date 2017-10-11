// ERC Token standard #20 Interface
// https://github.com/ethereum/EIPs/issues/20
contract ERC20Interface {

    // Token symbol
    string public constant symbol = "TBA";

    // Name of token
    string public constant name ="TBA";

    // Decimals of token
    uint8 public constant decimals = 18;

    // Get the total token supply
    function totalSupply() public constant returns (uint256 supply);

    // Get the account balance of another account with address _owner
    function balanceOf(address _owner) public constant returns (uint256 balance);

    // Send _value amount of tokens to address _to
    function transfer(address _to, uint256 _value) public returns (bool success);

    // Send _value amount of tokens from address _from to address _to
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);

    // Allow _spender to withdraw from your account, multiple times, up to the _value amount.
    // If this function is called again it overwrites the current allowance with _value.
    // this function is required for some DEX functionality
    function approve(address _spender, uint256 _value) public returns (bool success);

    // Returns the amount which _spender is still allowed to withdraw from _owner
    function allowance(address _owner, address _spender) public constant returns (uint256 remaining);

    // Triggered when tokens are transferred.
    event Transfer(address indexed _from, address indexed _to, uint256 _value);

    // Triggered whenever approve(address _spender, uint256 _value) is called.
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
}


// Implementation of the most intricate parts of the ERC20Interface that
// allows to send tokens around
contract ERC20Token is ERC20Interface{

    // With 7 decimals, a single unit is 10**7
    uint256 public constant unit = 10000000;

    // Balances for each account
    mapping(address => uint256) balances;

    // Owner of account approves the transfer of amount to another account
    mapping(address => mapping (address => uint256)) allowed;

    // What is the balance of a particular account?
    function balanceOf(address _owner) public constant returns (uint256) {
        return balances[_owner];
    }

    // Transfer the balance from owner's account to another account
    function transfer(address _to, uint256 _amount) public returns (bool) {
        if (balances[msg.sender] >= _amount && _amount > 0
                && balances[_to] + _amount > balances[_to]) {
            balances[msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(msg.sender, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    // Send _value amount of tokens from address _from to address _to
    // The transferFrom method is used for a withdraw workflow, allowing contracts to send
    // tokens on your behalf, for example to "deposit" to a contract address and/or to charge
    // fees in sub-currencies; the command should fail unless the _from account has
    // deliberately authorized the sender of the message via some mechanism; we propose
    // these standardized APIs for approval:
    function transferFrom(
        address _from,
        address _to,
        uint256 _amount
    ) public returns (bool) {
        if (balances[_from] >= _amount
            && allowed[_from][msg.sender] >= _amount && _amount > 0
                && balances[_to] + _amount > balances[_to]) {
            balances[_from] -= _amount;
            allowed[_from][msg.sender] -= _amount;
            balances[_to] += _amount;
            Transfer(_from, _to, _amount);
            return true;
        } else {
            return false;
        }
    }

    // Allow _spender to withdraw from your account, multiple times, up to the _value amount.
    // If this function is called again it overwrites the current allowance with _value.
    function approve(address _spender, uint256 _amount) public returns (bool) {
        allowed[msg.sender][_spender] = _amount;
        Approval(msg.sender, _spender, _amount);
        return true;
    }

    // Function to specify how much _spender is allowed to transfer on _owner's behalf
    function allowance(address _owner, address _spender) public constant returns (uint256) {
        return allowed[_owner][_spender];
    }

}


contract SoulToken is ERC20Token{

    // The three letter symbol to define the token, should be overwritten in subclass
    string public constant symbol = "SOUL";

    // Name of token should be overwritten in child
    string public constant name = "Soul Peaces";

    // 7 is a holy number so there are 7 decimals
    uint8 public constant decimals = 7;

    // mapping to keep the reason of the soul sale!
    mapping(address => string) public reasons;

    // prices that people put up for their soul
    mapping(address => uint256) public soulPrices;

    // who owns a particular soul
    mapping(address => address) public ownedBy;

    // number of souls owned by a someone
    mapping(address => uint256) public soulsOwned;

    // book of souls
    mapping(uint256 => address) public soulBook;

    // owner of the contract
    address public owner;

    // Address where sould obol is due to
    address public charonsBoat;

    // fee to pay to transfer soul
    uint8 public obol;

    // small fee to insert soul into soul book
    uint256 public bookingFee;

    // price per token
    uint256 public tokenPrice;

    // this the maximum of Soul
    uint256 totalSupply_;

    //souls for sale
    uint256 public soulsForSale;

    // souls already sold
    uint256 public soulsSold;

    // Logs a soul transfer
    event SoulTransfer(address indexed _from, address indexed _to);

    function SoulToken(){
        owner = msg.sender;
        charonsBoat = msg.sender;
        totalSupply_ = 0;
        obol = 10; // 10%, the ecclesiastical tithe
        // you get also 1000 Soul Peaces per Ether purchased
        tokenPrice = 1 finney / unit;
        // fee for inserting into soulbook, holy 3 finney:
        bookingFee = 3 finney;
        soulsForSale = 0;
        soulsSold = 0;
    }

    // fallback function, taken as donation!
    function () public payable {
        charonsBoat.transfer(msg.value);
    }

    function changeObol(uint8 _obol) public {
        require(msg.sender == owner);
        obol = _obol;
    }

    function changeBookingFee(uint256 fee) public {
        require(msg.sender == owner);
        bookingFee = fee;
    }

    // changes Charons boat, i.e. the address where the obol is payed to
    function changeBoat(address new_boat_) public{
        require(msg.sender == owner);
        charonsBoat = new_boat_;
    }

    function totalSupply() public constant returns (uint256){
        return totalSupply_;
    }

    // returns the reason for the selling
    function soldHisSouldBecause(address noSoulMate) public constant returns(string){
        return reasons[noSoulMate];
    }

    // returns the owner of a soul
    function soulIsOwnedBy(address noSoulMate) public constant returns(address){
        return ownedBy[noSoulMate];
    }

    // returns number of souls owned by someone
    function ownsSouls(address soulOwner) public constant returns(uint256){
        return soulsOwned[soulOwner];
    }

    function soldHisSoulFor(address noSoulMate) public constant returns(uint256){
        return soulPrices[noSoulMate];
    }

    function soulBookPage(uint256 page) public constant returns(address){
        return soulBook[page];
    }

    // sells your soul for a given price and a given reason!
    function sellSoul(string reason, uint256 price) public payable{
        string has_reason;

        // require that user gives a reason
        require(bytes(reason).length > 0);

        // require to pay bookingFee
        require(msg.value >= bookingFee);

        // assert has not sold his soul, yet
        has_reason = reasons[msg.sender];
        require(bytes(has_reason).length == 0);
        require(ownedBy[msg.sender] == address(0));

        // pay book keeping fee
        charonsBoat.transfer(msg.value);

        // store the reason forever on the blockchain
        reasons[msg.sender] = reason;
        // also the price is forever kept on the blockchain, so do not be too cheap
        soulPrices[msg.sender] = price;
        // and keep the soul in the soul book
        soulBook[soulsForSale + soulsSold] = msg.sender;
        soulsForSale += 1;
    }

    // buys msg.sender a soul and rewards him with tokens!
    function buySoul(address noSoulMate) public payable returns(uint amount){
        uint256 charonsObol;
        uint256 price;
        uint256 tokens;

        // you cannot buy an owned soul:
        require(ownedBy[noSoulMate] == address(0));
        // get the price of the soul
        price = soulPrices[noSoulMate];
        // Soul must be for sale
        require(price > 0);
        // Msg sender needs to pay the soul price
        require(msg.value >= price);
        charonsObol = msg.value / obol;
        // you gotta pay Charon
        require(charonsObol > 0);

        // calculate the amount of Tokens
        amount = price / tokenPrice;
        // check for wrap around
        require(totalSupply_ +  amount > totalSupply_);
        require(soulsOwned[msg.sender] + 1 > soulsOwned[msg.sender]);

        // pay Charon
        charonsBoat.transfer(charonsObol);
        // pay the soul owner:
        noSoulMate.transfer(msg.value - charonsObol);

        // Increase total supply by amount
        totalSupply_ += amount;
        // Update the soul stats
        soulsForSale -= 1;
        soulsSold += 1;
        // Increase the sender's balance by the appropriate amount and souls ;-)
        soulsOwned[msg.sender] += 1;
        ownedBy[noSoulMate] = msg.sender;
        balances[msg.sender] += amount;
        // log the transfers
        Transfer(this, msg.sender, amount);
        SoulTransfer(noSoulMate, msg.sender);

        return amount;
    }

    // can transfer a soul to a different account, but beware you have to pay Charon again!
    function transferSoul(address _to, address noSoulMate) payable{
        uint256 charonsObol;

        charonsObol = soulPrices[noSoulMate] / obol;

        require(ownedBy[noSoulMate] == msg.sender);
        require(soulsOwned[_to] + 1 > soulsOwned[_to]);
        require(msg.value >= charonsObol);
        // pay Charon
        charonsBoat.transfer(msg.value);
        // transfer the soul
        soulsOwned[msg.sender] -= 1;
        soulsOwned[_to] += 1;
        ownedBy[noSoulMate] = _to;

        // Log the soul transfer
        SoulTransfer(msg.sender, _to);
    }


}
