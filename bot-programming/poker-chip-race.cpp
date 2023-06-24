#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

/**
 * It's the survival of the biggest!
 * Propel your chips across a frictionless table top to avoid getting eaten by bigger foes.
 * Aim for smaller oil droplets for an easy size boost.
 * Tip: merging your chips will give you a sizeable advantage.
 **/
int main()
{
    int playerId; // your id (0 to 4)
    cin >> playerId; cin.ignore();

    // game loop
    while (1) {
        int playerChipCount; // The number of chips under your control
        cin >> playerChipCount; cin.ignore();
        int entityCount; // The total number of entities on the table, including your chips
        cin >> entityCount; cin.ignore();
        for (int i = 0; i < entityCount; i++) {
            int id; // Unique identifier for this entity
            int player; // The owner of this entity (-1 for neutral droplets)
            float radius; // the radius of this entity
            float x; // the X coordinate (0 to 799)
            float y; // the Y coordinate (0 to 514)
            float vx; // the speed of this entity along the X axis
            float vy; // the speed of this entity along the Y axis
            cin >> id >> player >> radius >> x >> y >> vx >> vy; cin.ignore();
        }
        for (int i = 0; i < playerChipCount; i++) {

            // Write an action using cout. DON'T FORGET THE "<< endl"
            // To debug: cerr << "Debug messages..." << endl;

            cout << "WAIT" << endl; // One instruction per chip: 2 real numbers (x y) for a propulsion, or 'WAIT'.
        }
    }
}