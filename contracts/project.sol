// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.17;

contract ProjectContract {
    struct Task {
        string taskAssignedTo;
        string task;
            }
    string projectName;
    string peopleAssigned;
    uint companyGSTNumber;
    string Description;
    Task[] public tasks;


    function createProject(string memory _projectName, string memory _peopleAssigned, uint _companyGSTNumber, string memory _Description) public  returns(string memory)
    {
        projectName=_projectName;
        peopleAssigned=_peopleAssigned;
        companyGSTNumber=_companyGSTNumber;
        Description = _Description;
        return projectName;
    }


    function addTask(string memory _taskAssignedTo, string memory _task) public  returns(uint){
        tasks.push(Task(_taskAssignedTo, _task));
        uint newIndex = tasks.length - 1;
        return newIndex;
    }

    function getTaskByIndex(uint index) public view returns ( string memory, string memory) {
        require(index < tasks.length, "Invalid index");

        Task storage task = tasks[index];
        return (task.taskAssignedTo, task.task);
    }

}
