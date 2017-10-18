from ethereum.tester import TransactionFailed
from ethereum.exceptions import InvalidTransaction
import pytest
import time

ether = int(1e18)
finney = int(ether/1000)
vig = 10
booking_fee = 13*finney

decimals = 6
unit = int(1e6)

napkin_unit_price = 10 * finney

dev_supply = 1111 * unit

total_supply = 144000 * unit

null_address = '0x0000000000000000000000000000000000000000'

def get_wei(chain, accounts):
    """ Returns the wei for each address in `accounts`

    :param chain: populus chain interface
    :param accounts: List of adresses
    :return: List of weis
    """
    web3 = chain.web3
    weis = []
    for irun, account in enumerate(accounts):
        wei = web3.eth.getBalance(accounts[irun])
        weis.append(wei)
    return weis


def test_init(chain, accounts):

    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    # Check some initial settings:
    assert soul_token.call().owner() == accounts[0]
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply
    assert soul_token.call().balanceOf(soul_token.address) == total_supply - dev_supply
    assert soul_token.call().balanceOf(accounts[1]) == 0
    assert soul_token.call().totalSupply() == total_supply
    assert soul_token.call().name() == 'Soul Napkins'
    assert soul_token.call().symbol() == 'SOUL'
    assert soul_token.call().decimals() == decimals


def test_sell_soul(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored äöÜ'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 100))

    assert soul_token.call().soldSoulBecause(accounts[1]) == reason
    assert soul_token.call().soldSoulBecause(accounts[0]) == ''
    assert soul_token.call().soldSoulFor(accounts[0]) == 0
    assert soul_token.call().soldSoulFor(accounts[1]) == 100
    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulsForSale() == 1
    assert soul_token.call().soulsSold() == 0


def test_sell_soul_fails_low_fee(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored äöÜ'
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee - 1}).sellSoul(reason, 100))



def test_twice_sell_soul_fails(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    # should fail for double sale
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))


def test_buy_soul(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulsForSale() == 1

    weis = get_wei(chain, accounts)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*napkin_unit_price}).buySoul(accounts[1]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 1
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().balanceOf(accounts[2]) == int(1.1*unit) # plus bonus napkin
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply
    assert soul_token.call().balanceOf(soul_token.address) == total_supply - dev_supply - int(1.1*unit)
    assert weis[1] < new_weis[1]
    assert weis[2] > new_weis[2]
    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulBookPage(1) == null_address
    assert soul_token.call().soulsForSale() == 0
    assert soul_token.call().soulsSold() == 1


def test_soul_can_only_be_bouhgt_once(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))


    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*napkin_unit_price}).buySoul(accounts[1]))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*napkin_unit_price}).buySoul(accounts[1]))

    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':1*napkin_unit_price}).buySoul(accounts[1]))


def test_buy_own_soul(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulsForSale() == 1

    weis = get_wei(chain, accounts)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':1*napkin_unit_price}).buySoul(accounts[1]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[1]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 0
    assert soul_token.call().ownsSouls(accounts[1]) == 1
    assert soul_token.call().balanceOf(accounts[2]) == 0
    assert soul_token.call().balanceOf(accounts[1]) == int(1.1*unit) # bonus napkin
    assert weis[1] > new_weis[1]
    assert weis[2] == new_weis[2]
    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulBookPage(1) == null_address
    assert soul_token.call().soulsForSale() == 0
    assert soul_token.call().soulsSold() == 1


def test_buy_multiple_souls(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    rec = chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    assert soul_token.call().totalObol() == booking_fee

    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulsForSale() == 1

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*napkin_unit_price}).buySoul(accounts[1]))

    assert soul_token.call().totalObol() == booking_fee + int(1*finney)

    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulBookPage(1) == null_address
    assert soul_token.call().soulsForSale() == 0
    assert soul_token.call().soulsSold() == 1

    chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason, 2*finney))

    assert soul_token.call().totalObol() == 2*booking_fee + int(1*finney)

    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulBookPage(1) == accounts[3]
    assert soul_token.call().soulBookPage(2) == null_address
    assert soul_token.call().soulsForSale() == 1
    assert soul_token.call().soulsSold() == 1

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':2*napkin_unit_price}).buySoul(accounts[3]))

    assert soul_token.call().totalObol() == 2*booking_fee + int(3*finney)

    assert soul_token.call().soulBookPage(0) == accounts[1]
    assert soul_token.call().soulBookPage(1) == accounts[3]
    assert soul_token.call().soulBookPage(2) == null_address
    assert soul_token.call().soulsForSale() == 0
    assert soul_token.call().soulsSold() == 2

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[3]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 2
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().balanceOf(accounts[2]) == int(2.3*unit) # + 2 bonus napkins
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply




def test_buy_soulmore(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    weis = get_wei(chain, accounts)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':2*napkin_unit_price}).buySoul(accounts[1]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 1
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().balanceOf(accounts[2]) == int(1.2*unit) # plus bonus napkin
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply
    assert weis[1] < new_weis[1]
    assert weis[2] > new_weis[2]


def test_superlong_reason(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'a' * 99999
    # should fail because of gas limit
    with pytest.raises(InvalidTransaction):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    reason = 'a' * 999
    receipt = chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))
    assert receipt.gasUsed > 500000
    assert receipt.gasUsed < 200000 + 1000*999

    reason = 'a' * 666
    receipt = chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason, 1*finney))
    assert receipt.gasUsed < 200000+1000*666

    reason = 'a'
    receipt = chain.wait.for_receipt(soul_token.transact({'from':accounts[4], 'value':booking_fee}).sellSoul(reason, 1*finney))
    assert receipt.gasUsed < 200000


def test_fail_on_empty_reason(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = ''
    # should fail because of gas limit
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[1]}).sellSoul(reason, 1*finney))


def test_vig(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).changeBoat(accounts[3]))

    weis = get_wei(chain, accounts)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))
    new_weis = get_wei(chain, accounts)

    assert weis[3] + booking_fee == new_weis[3]

    weis = get_wei(chain, accounts)
    val = 2*napkin_unit_price
    obol = val // 10
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':val}).buySoul(accounts[1]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 1
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().balanceOf(accounts[2]) == int(1.2*unit)  # bonus napkin
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply
    assert weis[1] + 2*napkin_unit_price - obol == new_weis[1]
    assert weis[2] > new_weis[2]
    assert weis[3] + obol == new_weis[3]


def test_only_allowed_by_owenr(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[1]}).changeBoat(accounts[3]))


def test_buy_soul_errors(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    # fails because price cannot be 0
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason, 0))

    # fails because charon wants some share
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason, 9))

    # fails because there must be a reason
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul('', 22))

    # fails because your offer is not high enough
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':int(0.9*finney)}).buySoul(accounts[1]))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*finney}).buySoul(accounts[1]))

    # fails because you cannot buy a bought soul
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[0], 'value':1*finney}).buySoul(accounts[1]))

    # fails because soul is not for sale
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[4], 'value':1*finney}).buySoul(accounts[0]))

    # # fails because obol can only be changed by author
    # with pytest.raises(TransactionFailed):
    #     chain.wait.for_receipt(soul_token.transact({'from':accounts[1]}).changeObol(22))

    # fails because bookingFee can onyl be changed by author
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[1]}).changeBookingFee(22))

    # fails because internal function
    with pytest.raises(ValueError):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).payCharon(22))

    # fails because internal function
    with pytest.raises(ValueError):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).payOutNapkins(22))


def test_change_boking_fee(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).changeBookingFee(22))
    chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).changeBoat(accounts[3]))

    weis = get_wei(chain, accounts)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':22}).sellSoul(reason, 1*finney))
    new_weis = get_wei(chain, accounts)

    assert weis[3] + 22 == new_weis[3]

    weis = get_wei(chain, accounts)
    val = 2*napkin_unit_price
    obol = val // 10
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':val}).buySoul(accounts[1]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 1
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().balanceOf(accounts[2]) == int(1.2*unit)  # bonus napkin
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply
    assert weis[1] + 2*napkin_unit_price - obol == new_weis[1]
    assert weis[2] > new_weis[2]
    assert weis[3] + obol == new_weis[3]


def test_transferSoul(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    rec = chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*napkin_unit_price))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*napkin_unit_price}).buySoul(accounts[1]))
    chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason, 2*napkin_unit_price))
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':2*napkin_unit_price}).buySoul(accounts[3]))


    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[3]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 2
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().balanceOf(accounts[2]) == int(2.3*unit) # with bonus napkins
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply

    chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).changeBoat(accounts[5]))

    weis = get_wei(chain, accounts)
    obol = int(1*finney)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':obol}).transferSoul(accounts[0], accounts[1]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[0]
    assert soul_token.call().soulIsOwnedBy(accounts[3]) == accounts[2]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 1
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().ownsSouls(accounts[0]) == 1

    assert soul_token.call().balanceOf(accounts[2]) == int(2.3*unit) # with bonus napkins
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply

    assert weis[5] + obol == new_weis[5]

    weis = get_wei(chain, accounts)
    obol = int(5*finney)
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':obol}).transferSoul(accounts[3], accounts[3]))
    new_weis = get_wei(chain, accounts)

    assert soul_token.call().soulIsOwnedBy(accounts[1]) == accounts[0]
    assert soul_token.call().soulIsOwnedBy(accounts[3]) == accounts[3]
    assert soul_token.call().soulIsOwnedBy(accounts[2]) == null_address
    assert soul_token.call().ownsSouls(accounts[2]) == 0
    assert soul_token.call().ownsSouls(accounts[1]) == 0
    assert soul_token.call().ownsSouls(accounts[0]) == 1
    assert soul_token.call().ownsSouls(accounts[3]) == 1

    assert soul_token.call().balanceOf(accounts[2]) == int(2.3*unit) # bonus napkin
    assert soul_token.call().balanceOf(accounts[0]) == dev_supply

    assert weis[5] + obol == new_weis[5]


def test_transferSoul_fails(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    rec = chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 1*finney))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1*finney}).buySoul(accounts[1]))
    chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason, 2*finney))
    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':2*finney}).buySoul(accounts[3]))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).changeBoat(accounts[5]))

    obol = int(0.09*finney)
    # should fail because of to few money
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':obol}).transferSoul(accounts[0], accounts[1]))

    # should fail because not owner of soul
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(soul_token.transact({'from':accounts[0], 'value':100*finney}).transferSoul(accounts[3], accounts[3]))


def test_fallback(chain, accounts, web3):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    weis = get_wei(chain, accounts)

    chain.wait.for_receipt(soul_token.transact({'from':accounts[0]}).changeBoat(accounts[5]))

    chain.wait.for_receipt(web3.eth.sendTransaction({'value':10*napkin_unit_price, 'from':accounts[1], 'to': soul_token.address,
                                                     'gas':200000}))
    chain.wait.for_receipt(web3.eth.sendTransaction({'value':20*napkin_unit_price, 'from':accounts[0], 'to': soul_token.address,
                                                     'gas':200000}))
    new_weis = get_wei(chain, accounts)

    assert weis[5] + 300*finney == new_weis[5]
    assert soul_token.call().balanceOf(accounts[0]) == 20*unit + dev_supply
    assert soul_token.call().balanceOf(accounts[1]) == 10*unit



def test_token_transfer(chain, accounts):
    provider = chain.provider

    soul_token, deploy_txn_hash2 = provider.get_or_deploy_contract(
        'SoulToken'
    )

    # buy some tokens
    reason='äää'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason, 100*napkin_unit_price))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[0], 'value':100*napkin_unit_price}).buySoul(accounts[1]))

    assert soul_token.call().balanceOf(accounts[0]) == int(11*unit) + dev_supply

    # does nothing because of insufficient funds
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(19925*unit)))
    assert soul_token.call().balanceOf(accounts[0]) == int(11*unit) + dev_supply

    # transfer the tokens
    chain.wait.for_receipt(soul_token.transact().transfer(accounts[1], int(25*unit)))

    # check that transfer worled
    assert soul_token.call().balanceOf(accounts[0]) == int(11*unit) + dev_supply - int(25*unit)
    assert soul_token.call().balanceOf(accounts[1]) == int(25*unit)

    # approve some future transfers
    chain.wait.for_receipt(soul_token.transact().approve(accounts[2], int(50*unit)))

    # check for to large sending
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(51*unit)))

    # there should be no transfer because the amount was too large
    assert soul_token.call().balanceOf(accounts[0]) == int(11*unit) + dev_supply - int(25*unit)
    assert soul_token.call().balanceOf(accounts[1]) == int(25*unit)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25*unit)))

    assert soul_token.call().balanceOf(accounts[0]) == int(11*unit) + dev_supply - int(50*unit)
    assert soul_token.call().balanceOf(accounts[1]) == int(50*unit)
    assert soul_token.call().allowance(accounts[0], accounts[2]) == int(25*unit)

    # this should be allowed
    chain.wait.for_receipt(soul_token.transact({'from': accounts[2]}).transferFrom(accounts[0],
                                                                                 accounts[1],
                                                                                 int(25*unit)))

    assert soul_token.call().balanceOf(accounts[0]) == int(11*unit) + dev_supply - int(75*unit)
    assert soul_token.call().balanceOf(accounts[1]) == int(75*unit)
    assert soul_token.call().allowance(accounts[0], accounts[2]) == 0


def test_maximum_supply(chain, accounts, web3):
    provider = chain.provider

    soul_token, deploy_txn_hash2 = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'mooooney'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1], 'value':booking_fee}).sellSoul(reason,
                                                                                                   1000*napkin_unit_price))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1000*napkin_unit_price}).buySoul(accounts[1]))

    assert soul_token.call().balanceOf(accounts[2]) == int(101*unit)

    chain.wait.for_receipt(web3.eth.sendTransaction({'value':(143898 - int(dev_supply/unit))*napkin_unit_price,
                                                     'from':accounts[1], 'to': soul_token.address,
                                                     'gas':200000}))

    assert soul_token.call().balanceOf(accounts[1]) == int(143898*unit) - dev_supply

    # fails cause not enough supply
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(web3.eth.sendTransaction({'value':2*napkin_unit_price, 'from':accounts[1], 'to': soul_token.address,
                                                     'gas':200000}))


    chain.wait.for_receipt(soul_token.transact({'from':accounts[3], 'value':booking_fee}).sellSoul(reason,
                                                                                                   100*napkin_unit_price))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':100*napkin_unit_price}).buySoul(accounts[3]))

    assert soul_token.call().balanceOf(accounts[2]) == int(102*unit)


    # fails cause not enough supply
    with pytest.raises(TransactionFailed):
        chain.wait.for_receipt(web3.eth.sendTransaction({'value':1, 'from':accounts[1], 'to': soul_token.address,
                                                     'gas':200000}))


    chain.wait.for_receipt(soul_token.transact({'from':accounts[4],
                                                'value':booking_fee}).sellSoul(reason, 1000*napkin_unit_price))

    chain.wait.for_receipt(soul_token.transact({'from':accounts[2], 'value':1000*napkin_unit_price}).buySoul(accounts[4]))

    assert soul_token.call().balanceOf(accounts[2]) == int(102*unit)
    assert soul_token.call().balanceOf(soul_token.address) == 0




