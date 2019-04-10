
#include <vector>
#include <map>
#include <string>
#include <iostream>
#include <sstream>

#include <benchmark/benchmark.h>

using namespace std;

class Solution
{
  public:
/**
给定 nums = [2, 7, 11, 15], target = 9
因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
**/
    vector<int> twoSum(vector<int> &nums, int target)
    {
        map<int, int> m;
        for (int i = 0; i < nums.size(); ++i)
        {
            int cur_num = nums[i];
            int t = target - cur_num;
            if (m.count(t))
            {
                return {m[t], i};
            }
            m[cur_num] = i;
        }
        return {};
    }
};

void trimLeftTrailingSpaces(string &input)
{
    input.erase(input.begin(), find_if(input.begin(), input.end(), [](int ch) {
                    return !isspace(ch);
                }));
}

void trimRightTrailingSpaces(string &input)
{
    input.erase(find_if(input.rbegin(), input.rend(), [](int ch) {
                    return !isspace(ch);
                })
                    .base(),
                input.end());
}

vector<int> stringToIntegerVector(string input)
{
    vector<int> output;
    trimLeftTrailingSpaces(input);
    trimRightTrailingSpaces(input);
    input = input.substr(1, input.length() - 2);
    stringstream ss;
    ss.str(input);
    string item;
    char delim = ',';
    while (getline(ss, item, delim))
    {
        output.push_back(stoi(item));
    }
    return output;
}

int stringToInteger(string input)
{
    return stoi(input);
}

string integerVectorToString(vector<int> list, int length = -1)
{
    if (length == -1)
    {
        length = list.size();
    }

    if (length == 0)
    {
        return "[]";
    }

    string result;
    for (int index = 0; index < length; index++)
    {
        int number = list[index];
        result += to_string(number) + ", ";
    }
    return "[" + result.substr(0, result.length() - 2) + "]";
}


void common_use_input() {
    string line;
    while (getline(cin, line))
    {
        vector<int> nums = stringToIntegerVector(line);
        getline(cin, line);
        int target = stringToInteger(line);

        vector<int> ret = Solution().twoSum(nums, target);

        string out = integerVectorToString(ret);
        cout << out << endl;
    }
}

void common_use_prepare_case() {
    vector<int> nums = {2, 7, 13, 15};
    int target = 9;
    vector<int> ret = Solution().twoSum(nums, target);
    string out = integerVectorToString(ret);

    cout << out << endl;
}

int main()
{
    false ? common_use_input() : common_use_prepare_case();
    return 0;
}