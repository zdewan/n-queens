#include <iostream>
#include <cmath>
#include <array>
#include <vector>
#include <random>
#include <cstdio>
#include <numeric>
#include <ctime>
#include <chrono>
using namespace std;
using namespace chrono;

vector<int> conflicts(int queens[], int n, int col)
{
    vector<int> confs(n, -1);
    for (int i = 0; i < n; i++)
    {
        if ((i == col) || (queens[i] == -1))
        {
            continue;
        }
        confs[queens[i]]++;

        // diagonal upwards
        if (0 <= queens[i] - abs(i - col) < n)
        {
            confs[queens[i] - abs(i - col)]++;
        }

        // diagonal downwards
        if (0 <= queens[i] + abs(i - col) < n)
        {
            confs[queens[i] + abs(i - col)]++;
        }
    }
    return confs;
}

int move(int queens[], int n, int col)
{
    vector<int> confs;

    confs = conflicts(queens, n, col);

    int min_conf = confs[0];
    for (int i = 0; i < n; i++)
    {
        if (min_conf > confs[i])
            min_conf = confs[i];
    }

    vector<int> smallest_indexes;

    for (int i = 0; i < n; i++)
    {
        if (confs[i] == min_conf)
        {
            smallest_indexes.push_back(i);
        }
    }
    srand(time(NULL));

    int rand_conf = rand() % smallest_indexes.size();

    return smallest_indexes[rand_conf];
}
int main()
{

    const int n = 10;
    auto start = high_resolution_clock::now();

    int queens[n];
    for (int i = 0; i < n; i++)
    {
        queens[i] = -1;
    }

    // initialize queens in all rows
    for (int i = 0; i < n; i++)
    {
        // puts queens in col i
        queens[i] = move(queens, n, i);
        cout << "Initialize queen " << i << endl;
    }
    // conflict initialization

    // build row and diagonal conflicts arrays
    int row_confs[n];
    int pos_diag_confs[2 * n - 1];
    int neg_diag_confs[2 * n - 1];

    for (int i = 0; i < n; i++)
    {
        row_confs[queens[i]]++;
        pos_diag_confs[queens[i] - i + n - 1]++;
        neg_diag_confs[queens[i] + i]++;
    }

    // build total conflicts array
    int total_confs[n];
    for (int i = 0; i < n; i++)
    {
        total_confs[i] = (row_confs[queens[i]] + pos_diag_confs[queens[i] - i + n - 1] + neg_diag_confs[queens[i] + i]);
    }

    int count = 0;
    while (accumulate(total_confs, total_confs + n, 0) > 0)
    {
        count++;

        // choose which random conflicting queen to move
        vector<int> found_confs;
        int move_col;

        for (int i = 0; i < n; i++)
        {
            if (total_confs[i] > 0)
            {
                found_confs.push_back(i);
            }
        }
        srand(time(NULL));
        int rand_conf = rand() % found_confs.size();
        move_col = found_confs[rand_conf];

        // move queen in chosen column
        int old_row = queens[move_col];
        int new_row;
        new_row = move(queens, n, move_col);
        queens[move_col] = new_row;

        // update total conflicts

        // recalculate conglict for the moved column
        total_confs[move_col] = 0;

        for (int i = 0; i < n; i++)
        {
            if (i == move_col)
            {
                continue;
            }

            // subtract conflict if it was conflicting with the old queen
            if ((queens[i] == old_row) || (abs((queens[i] - old_row)) == abs((i - move_col))))
            {
                total_confs[i]--;
            }
            // add conflict if it is now conflicting with the new queen
            if ((queens[i] == new_row) || (abs((queens[i] - new_row)) == abs((i - move_col))))
            {
                total_confs[i]++;
                total_confs[move_col]++;
            }
        }
        cout << "Iterate Minimum Conflict " << count << endl;
    }

    auto algorithm_duration = high_resolution_clock::now();
    duration<double> total_time_seconds = algorithm_duration - start;
    cout << "\n"
         << total_time_seconds.count() << " seconds" << endl;
    return 0;
}