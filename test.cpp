#include <bits/stdc++.h>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }
        int x = a[0];
        vector<int> b(a.begin() + 1, a.end());
        sort(b.begin(), b.end());
        for (int y : b) {
            if (y > x) {
                x += (y - x + 1) / 2;
            }
        }
        cout << x << endl;
    }
    return 0;
}