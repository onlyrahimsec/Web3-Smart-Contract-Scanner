// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint256) public balances;

    // ১. Reentrancy Vulnerability (🔴 HIGH)
    // এই ফাংশনটি দিয়ে হ্যাকাররা বারবার ফান্ড তুলে নিতে পারবে।
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Insufficient balance");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        balances[msg.sender] = 0; // এটি টাকা পাঠানোর আগে হওয়া উচিত ছিল
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // ২. Integer Overflow/Underflow (🟠 MEDIUM - যদিও ০.৮ এর পরে সলিডিটি এটি চেক করে)
    // কিন্তু স্লিদার এটি ওল্ড কম্পাইলার ভার্সন হলে ফ্ল্যাগ করবে।
    function decreaseBalance(uint256 amount) public {
        balances[msg.sender] -= amount; // আন্ডারফ্লোর ঝুঁকি
    }

    // ৩. Unprotected Self-Destruct (🔴 HIGH)
    // যে কেউ এই কন্ট্রাক্টটি ডিলিট করে দিতে পারবে! 
    function kill() public {
        selfdestruct(payable(msg.sender));
    }
}