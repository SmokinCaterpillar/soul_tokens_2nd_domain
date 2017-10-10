from ethereum.tester import TransactionFailed
import pytest
import time

ether = int(1e18)

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
    assert soul_token.call().balanceOf(accounts[0]) == 0
    assert soul_token.call().balanceOf(accounts[1]) == 0
    assert soul_token.call().totalSupply() == 0

def test_sell_soul(chain, accounts):
    provider = chain.provider
    soul_token, deploy_txn_hash = provider.get_or_deploy_contract(
        'SoulToken'
    )

    reason = 'I`m bored'
    chain.wait.for_receipt(soul_token.transact({'from':accounts[1]}).sellSoul(reason, 100))

    assert soul_token.call().soldHisSouldBecause(accounts[1]) == reason
    assert soul_token.call().soldHisSouldBecause(accounts[0]) == ''
    assert soul_token.call().soldHisSoulFor(accounts[0]) == 0
    assert soul_token.call().soldHisSoulFor(accounts[1]) == 100