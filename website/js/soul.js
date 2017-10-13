/************ main function *************************************/


console.log('Loading Soul Token script');


/**
 * Rounds values
 *
 * @param value: value to be rounder
 * @param decimals: remaining number of decimals
 * @returns rounded number
 */
function round(value, decimals){
    var rounder = Math.pow(10, decimals);
    return Math.round(value * rounder) / rounder;
}


var Eth = require('ethjs-query');
var EthContract = require('ethjs-contract');
var BigNumber = require('bignumber.js');

// ABI and addresses of both contracts
const contractAddress = '0x65374ed1F16B4c9588c6247e6E4D93CeAf8eeC8A';
const contractAbi = [{"constant":true,"inputs":[{"name":"noSoulMate","type":"address"}],"name":"soulIsOwnedBy","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"noSoulMate","type":"address"}],"name":"soldHisSoulFor","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"soulOwner","type":"address"}],"name":"ownsSouls","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"soulsForSale","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"soulPrices","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"soulsSold","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"soulsOwned","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"charonsBoat","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"fee","type":"uint256"}],"name":"changeBookingFee","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"soulBook","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"noSoulMate","type":"address"}],"name":"transferSoul","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"bookingFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenPrice","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"noSoulMate","type":"address"}],"name":"buySoul","outputs":[{"name":"amount","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"unit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"page","type":"uint256"}],"name":"soulBookPage","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"reason","type":"string"},{"name":"price","type":"uint256"}],"name":"sellSoul","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"noSoulMate","type":"address"}],"name":"soldHisSouldBecause","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"ownedBy","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_obol","type":"uint8"}],"name":"changeObol","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"reasons","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"new_boat_","type":"address"}],"name":"changeBoat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"obol","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"}],"name":"SoulTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]

const nullAddress = "0x0000000000000000000000000000000000000000"

var soulToken;  // global reference to impeachment contract
var bookingFee = 0.013;
var unit = 10000000;

var currentPage = -1;
var totalPages = 1;
var soulsPerPage = 8;
var onSale = false;

function startApp() {
    // Initialize the contracts
    const eth = new Eth(web3.currentProvider);
    const contract = new EthContract(eth);

    const SoulToken = contract(contractAbi);
    soulToken = SoulToken.at(contractAddress);

    // Event Listener for buying Impeachment Tokens
    listenForSoulSellsClicks();
    // check if coinbase is on sale
    checkOnSale();
    // Update the Balances
    updateBalances();
    updateTotalSupply();
    getSoulBook();

    console.log('App started.')
}

function listenForSoulSellsClicks() {
  var button = document.getElementById('sellSoulButton');
  button.addEventListener('click', function() {

      var ether = document.getElementById("soulPrice").value;
      var inWei = web3.toWei(ether, 'ether');
      var bookingFeeInWei = web3.toWei(bookingFee, 'ether');
      var reason = document.getElementById("soulComment").value;

      console.log('Clicked soul selling for ' + inWei + ' wie because: ' + reason);

      var rLength = reason.length;
      if (onSale){
          alert('You did put your soul already on sale! Sneaky, but sorry, you can sell your soul only once!')
      } else if (rLength === 0){
          alert('C`mon you need a reason to sell your soul!');
      } else if(rLength > 666) {
          alert('Your reason is too long with ' + rLength + ' characters, please use 666 or less!')
      } else{
          var gas = 200000 + 1000 * rLength;
          soulToken.sellSoul(reason, inWei, {from: web3.eth.coinbase, value:bookingFeeInWei, gas: gas}).then(function (txHash) {
              console.log('Transaction sent');
              console.dir(txHash)
          })
      }
  })
}


function updateTotalSupply(){

    var napkins;
    soulToken.totalSupply().then(function (results) {
        napkins = results[0];
        console.log('napkins ' + napkins);
        napkins = new BigNumber(napkins).dividedBy(unit);
        var htmlText = "In total Charon has distributed " + napkins + " napkins."

        document.getElementById('totalSupply').innerHTML = htmlText
    });

}


function checkOnSale(){
    var ownReason;
    soulToken.soldHisSouldBecause(web3.eth.coinbase).then(function (results) {
        ownReason = results[0];
        console.log('ownReason ' + ownReason);
        onSale = ownReason.length > 0;
    });
}

function updateBalances(){

    var napkins;
    var souls;
    var htmlText;
    soulToken.balanceOf(web3.eth.coinbase).then(function (results) {
        napkins = results[0];
        console.log('napkins ' + napkins);
        napkins = new BigNumber(napkins).dividedBy(unit);

        soulToken.ownsSouls(web3.eth.coinbase).then(function (results) {
            souls = results[0];
            console.log('souls ' + souls);

            htmlText = "You own "+ souls + " soul(s) and " + napkins + " SOUL tokens, i.e. napkins."
            document.getElementById('balance').innerHTML = htmlText
        });
    }).catch(function (error) {
        console.error(error);
        console.log('ERROR no it balance found');
        htmlText = "Please, unlock your MetaMask wallet to see your soul and napkin balances."
        document.getElementById('balance').innerHTML = htmlText
    });
}


function getWrittenNapkingSold(index, soul, reason, owner){
    var half = soul.length / 2;
    var soul1Half = soul.substr(0, half);
    var soul2Half = soul.substr(half + 1);
    var owner1Half = owner.substr(0, half);
    var owener2Half = owner.substr(half + 1);
    var htmlText="<div class='col-lg-3 col-sm-3'>" +
                    "<a class='portfolio-box text-faded text-center' id=" + soul + ">" +
                      "<h2>SOUL #" + index + "</h2><br>" +
                      "<p> <i>" + reason + "</i></p>" +
                      "<p><b>Owned by " + owner.substr(0, 7) + "...</b></p>" +
                      "<div class='portfolio-box-caption'>" +
                        "<div class='portfolio-box-caption-content'>" +
                          "<div class='project-category text-faded'>" +
                            "Soul of <br>&quot" + soul1Half + "<br>" + soul2Half + "&quot" +
                          "</div>" +
                          "<div class='project-name'>" +
                            "Already Sold to <br><small>&quot" + owner1Half + "<br>" + owener2Half + "&quot</small>" +
                          "</div>" +
                        "</div>" +
                      "</div>" +
                    "</a>" +
                "</div>";
    return htmlText
}

function getWrittenNapkingForSale(index, soul, reason, priceInEth){
    var half = soul.length / 2;
    var soul1Half = soul.substr(0, half);
    var soul2Half = soul.substr(half + 1);
    var htmlText="<div class='col-lg-3 col-sm-3'>" +
                    "<a class='portfolio-box text-faded text-center' id=" + soul + ">" +
                      "<h2>SOUL #" + index + "</h2><br>" +
                      "<p> <i>" + reason + "</i></p>" +
                      "<p><b>Avialbale for " + priceInEth + " ETH</b></p>" +
                      "<div class='portfolio-box-caption'>" +
                        "<div class='portfolio-box-caption-content'>" +
                          "<div class='project-category text-faded'>" +
                            "Soul of <br>&quot" + soul1Half + "<br>" + soul2Half + "&quot" +
                          "</div>" +
                          "<div class='project-name'>" +
                            "For Sale: Only " + priceInEth + " ETH!" +
                          "</div>" +
                        "</div>" +
                      "</div>" +
                    "</a>" +
                "</div>";
    return htmlText
}


function getSoulBook(){
    var soulsForSale;
    var soulsSold;
    var totalSouls;
    var htmlText;

    soulToken.soulsForSale().then(function (results) {
        soulsForSale = results[0];
        console.log('soulsForSale ' + soulsForSale);

        soulToken.soulsSold().then(function (results) {
            soulsSold = results[0];
            console.log('soulsSold ' + soulsSold);

            htmlText = "<mark>" + soulsForSale + " Soul(s) for Sale and " + soulsSold + " soul(s) sold! " +
                "Just click on one of the souls to purchase it!</mark>";
            document.getElementById('status').innerHTML = htmlText

            totalSouls  = Number(soulsSold) + Number(soulsForSale);
            totalPages = Math.ceil(totalSouls / soulsPerPage);
            console.log('Soul book has pages ' + totalPages + ' and souls ' + totalSouls);
            if ((currentPage <= 0) || (currentPage > totalPages)) {
                currentPage = totalPages
            }
            document.getElementById('pageNumber').innerHTML = "Page " + currentPage;
            document.getElementById('soulBook').innerHTML = "";
            lookUpSouls(totalSouls);

        });
    });
};


function lookUpSouls(totalSouls) {
    var end = Math.min(totalSouls, currentPage * soulsPerPage);
    var start = Math.max(0, end - soulsPerPage);
    console.log('Looking up souls from idx ' + start + ' to idx ' + end);
    for (var idx = start; idx < end; idx++) {
        console.log('Looking up soul idx ' + idx)
        loadIndividualSoul(idx)
    }
}

function loadIndividualSoul(soulIndex){
    var soul;
    var reason;
    var owner;
    var price;
    var priceInEth;
    var htmlText;

    soulToken.soulBookPage(soulIndex).then(function (results) {
        soul = results[0];
        console.log('Found soul ' + soul);

        soulToken.soldHisSouldBecause(soul).then(function (results) {
            reason = results[0];
            console.log('Found reason ' + reason);

            soulToken.soldHisSoulFor(soul).then(function (results) {
                price = results[0];
                console.log('Found price ' + price);

                soulToken.ownedBy(soul).then(function (results) {
                    owner = results[0];
                    console.log('Found owner ' + owner);

                    if (owner === nullAddress){
                        priceInEth = web3.fromWei(price, 'ether');
                        priceInEth = round(priceInEth, 4);
                        htmlText = getWrittenNapkingForSale(soulIndex + 1, soul, reason, priceInEth);
                    } else {
                        htmlText = getWrittenNapkingSold(soulIndex + 1, soul, reason, owner);
                    }
                    document.getElementById('soulBook').innerHTML += htmlText;
                });
            });
        });

    });
}




window.addEventListener('load', function() {

  // Check if Web3 has been injected by MetaMask:
  if (typeof web3 !== 'undefined') {
    // You have a web3 plugin, Start the DApp
      web3 = new Web3(web3.currentProvider);
      startApp();
  } else {
      console.log('You need a Web3 plugin like MetaMask for your browser to trade souls on this website.\n' +
          'Visit https://metamask.io/ to install the plugin.')
      startAppNoWeb3();
  }
});

console.log('Soul Script loaded.');