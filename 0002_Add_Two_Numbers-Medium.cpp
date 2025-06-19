// Importing Neccessary Packages //
#include <iostream>
#include <string>

// Standard Namespace //
using namespace std;

// Definition for singly-linked list. //
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
    bool isEqual(ListNode* other) const {
        const ListNode* a = this;
        const ListNode* b = other;
        while (a && b) {
            if (a->val != b->val) return false;
            a = a->next;
            b = b->next;
        }
        return a == nullptr && b == nullptr;
    }
};

// Class Solution to Submit in LeetCode //
class Solution {
    // Public Class twoSum for solution//
    public:
        ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
            // Create a dummy head to simplify handling the result list //
            ListNode* dummyHead = new ListNode();
            // Pointer to build the result list //
            ListNode* current = dummyHead;
            // To keep track of carry from each digit addition //
            int carry = 0;

            // Loop while either list has nodes or there's a remaining carry //
            while (l1 || l2 || carry) {
                // Get values from current nodes, or 0 if one list is shorter //
                int val1 = (l1 ? l1->val : 0);
                int val2 = (l2 ? l2->val : 0);

                // Calculate sum of values and carry //
                int sum = val1 + val2 + carry;

                // Update carry for next iteration  //
                carry = sum / 10;

                // Create a new node with the digit value (sum % 10) //
                current->next = new ListNode(sum % 10);
                // Move to the next node in result list //
                current = current->next;

                // Move to the next nodes in l1 and l2 if available //
                if (l1) l1 = l1->next;
                if (l2) l2 = l2->next;

            }

            // Return the next of dummy head, which is the actual result head //
            return dummyHead->next;
        }
};

// Main function to pass test case //
int main() {
    // Creating and Running Test Cases //
    Solution *solution = new Solution();
    ListNode* result_1 = solution->addTwoNumbers(new ListNode(2, new ListNode(4, new ListNode(3))), new ListNode(5, new ListNode(6, new ListNode(4))));
    ListNode* result_2 = solution->addTwoNumbers(new ListNode(0), new ListNode(0));
    ListNode *result_3 = solution->addTwoNumbers(new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9))))))), new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9)))));
    delete solution;

    // Test Case 1 //
    if (result_1->isEqual(new ListNode(7, new ListNode(0, new ListNode(8))))) {
        cout << "\033[32mTest Case 1 Passed.\033[0m" << endl;
    } else {
        cout << "\033[31mTest Case 1 Failed.\033[0m" << endl;
    }

    // Test Case 2 //
    if (result_2->isEqual(new ListNode(0))) {
        cout << "\033[32mTest Case 2 Passed.\033[0m" << endl;
    } else {
        cout << "\033[31mTest Case 2 Failed.\033[0m" << endl;
    }

    // Test Case 3 //
    if (result_3->isEqual(new ListNode(8, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(0, new ListNode(0, new ListNode(0, new ListNode(1)))))))))) {
        cout << "\033[32mTest Case 3 Passed.\033[0m" << endl;
    } else {
        cout << "\033[31mTest Case 3 Failed.\033[0m" << endl;
    }

    return 0;
}