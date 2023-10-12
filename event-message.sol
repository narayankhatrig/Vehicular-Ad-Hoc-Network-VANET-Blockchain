// SPDX-License-Identifier: NARAYAN KHATRI
pragma solidity >=0.7.0 <0.9.0;
contract MESSAGE {
    uint256 initial_balance = 10;
    struct EventList{ // structure for maintaining event information
        bytes32 id;
        address addr;
        bytes32 balance;
        bytes32 trust_value;
        //address initiator;
    }

    mapping(address => EventList) eventlist;
    event registerevent(bytes32 id, address addr, bytes32 balance, bytes32 trust_value);

    function Initiator(bytes32 id, address initiator, bytes32 balance, bytes32 trust_value) public payable{
        eventlist[initiator].id = id;
        eventlist[initiator].addr = initiator;
        eventlist[initiator].balance = balance;
        eventlist[initiator].trust_value = trust_value;
        emit registerevent(eventlist[initiator].id, eventlist[initiator].addr, eventlist[initiator].balance, eventlist[initiator].trust_value);
    }
    
    function viewevent(address initiator) public view returns(bytes32, address, bytes32, bytes32){
        return(eventlist[initiator].id, eventlist[initiator].addr, eventlist[initiator].balance, eventlist[initiator].trust_value);
    }
    
}