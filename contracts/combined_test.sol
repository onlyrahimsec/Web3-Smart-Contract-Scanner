// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0; // ওল্ড ভার্সন (Slither ধরবে)

contract JointAuditTest {
    mapping(address => uint256) public balances;

    // ১. Reentrancy: Slither এবং Mythril দুইজনেই এটি ধরবে। 
    // স্লিদার কোড স্ট্রাকচার দেখে ধরবে, মিথরিল লজিক ফ্লো দেখে।
    function withdrawAll() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0);

        (bool success, ) = msg.sender.call{value: amount}(""); // Low-level call
        require(success);

        balances[msg.sender] = 0; // State change after call
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // ২. Integer Overflow: মিথরিল এটি খুব ভালো ডিটেক্ট করে। 
    // কারণ ০.৮ এর আগের ভার্সনে অটো-চেক ছিল না।
    function batchUpdateBalance(uint256 _amount) public {
        balances[msg.sender] += _amount; // Overflow risk
    }

    // ৩. Unprotected Self-Destruct: দুই টুলই এটি ক্রিটিক্যাল হিসেবে ধরবে।
    function killContract() public {
        // কোনো onlyOwner চেক নেই
        selfdestruct(payable(msg.sender));
    }

    // ৪. Unused Return Value & Old Solidity: স্লিদার এগুলোকে ইনফরমেশনাল হিসেবে ধরবে।
    function sendEther(address payable _to) public payable {
        _to.send(msg.value); // Return value ignores (Slither issue)
    }
}