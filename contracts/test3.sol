pragma solidity ^0.5.0;

contract MythrilTest {
    // মিথরিল এটি খুব ভালো ধরে কারণ এটি একটি গাণিতিক ভুল
    function setStorage(uint256 input) public {
        uint256 x = input + 10;
        if (x < input) { // Integer Overflow logic
            // কিছু একটা হবে
        }
    }

    // সরাসরি ইথার পাঠানোর লজিক থাকলে মিথরিল এলার্ট দেয়
    function sendMoney(address payable _to) public payable {
        _to.transfer(msg.value);
    }
}