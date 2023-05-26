# Wood 2 League

## Goal

End the game with more crystal than your opponent.

The game takes place in a lab, in which two scientists in charge of robot ants are competing to find the most efficient way of gathering crystals.

However, the ants **cannot be controlled directly**. The ants will respond to the presence of beacons.

## Rules

The game is played in turns. On each turn, both players perform any number of actions simultaneously.

### The Map
On each run, the map is **generated randomly** and is made up of **hexagonal cells**.

Each cell has an **index** and up to six neighbors. Each direction is labelled `0` to `5`.

Each cell has a **type**, which indicates what the cell contains:
- `0` if it does not contain a resource.
- *`1` will appear in later leagues and can be ignored for now.*
- `2` if it contains the crystal resource.
The amount of `resources` contained in each cell is also given, and is subject to change during the game as the ants **harvest** cells.

A cell may also have a **base** on it. The players’ ants will start the game on these bases.

### Ants & Beacons

Both players start with several ants placed on their **base**. The players cannot move the ants directly but can place **beacons** to affect their movement.

Players can place **any number** of beacons per turn but can only place **one each per cell**.

When placing a beacon, players must give that beacon a `strength`. These beacon strengths act as **weights**, determining the **proportion of ants** that will be dispatched to each one.

In other words, the **higher** the beacon `strength`, the greater the **percentage** of your ants that will be sent to that beacon.

*Example: There are three beacons of `strength` `2`, `1`, and `2`. `10` ants in total will be dispatched to the beacons. The `10` ants will move to the three beacons, keeping the same proportions as the beacon strengths: `4`, `2`, and `4`.*

The ants will do their best to take the **shortest paths** to their designated beacons, moving at a speed of** one cell per turn**.

In between turns, the **existing beacons** are powered down and **removed from play**.

Use beacons to place your ants in such a way to create **harvesting chains** between your **base** and a **resource**.

### Harvesting Chains

In order to harvest **crystal** and score points, there must be an **uninterrupted chain** of **cells containing your ants** between the resource and your **base**.

The amount of crystal harvested per turn is equal to the **weakest link** in the chain. In other words, it is the smallest amount of ants from the cells that make up the chain.

**Harvesting** is calculated separately for **each resource**, and for each one the game will automatically choose the **best chain** from its cell to your base.

### Actions

On each turn players can do any amount of valid actions, which include:

- `BEACON` `index` `strength`: place a beacon of strength `strength` on cell `index`.
- `LINE` `index1` `index2` `strength`: place beacons all along a path from `index1` to `index2`, all of strength `strength`. A shortest path is chosen automatically.
- `WAIT`: do nothing.
- `MESSAGE` `text`. Displays text on your side of the HUD.

### Action order for one turn

1. `LINE` actions are computed.
2. `BEACON` actions are computed.
3. Ants move.
4. Crystal is harvested and points are scored.

### Victory Conditions

- You have over half of the total **crystal** on the map.
- You have more **crystal** than your opponent after `100` turns.

### Defeat Conditions

- Your program does not provide a command in the allotted time or it provides an unrecognized command.

### 🐞 Debugging tips
- Hover over a tile to see extra information about it, including beacon `strength`.
- Use the `MESSAGE` command to display some text on your side of the HUD.
- Press the gear icon on the viewer to access extra display options.
- Use the keyboard to control the action: space to play/pause, arrows to step 1 frame at a time.

## Game Protocol

### Initialization Input

**First line:** `numberOfCells` an integer for the amount of cells in the map.
**Next `numberOfCells` lines:** the cells, ordered by `index`. Each cell is represented by `8` space-separated integers:
- `type`: `1` for egg, `2` for crystal, `0` otherwise.
- `initialResources` for the amount of crystal/egg here.
- `6` `neigh` variables: Ignore for this league.
**Next line:** one integer `numberOfBases` which equals `1` for this league.
**Next line:** `numberOfBases` integers for the cell indices where a **friendly base** is present.
**Next line:** `numberOfBases` integers for the cell indices where an **opponent base** is present.

### Input for One Game Turn

**Next `numberOfCells` lines:** one line per cell, ordered by `index`. `3` integers per cell:
- `resources`: the amount of crystal/eggs on the cell.
- `myAnts`: the amount of ants you have on the cell.
- `oppAnts`: the amount of ants your opponent has on the cell.

### Output

All your actions on one line, separated by a `;`
- `BEACON` `index` `strength`. Places a beacon that lasts one turn.
- `LINE` `index1` `index2` `strength`. Places beacons along a path between the two provided cells.
- `WAIT`. Does nothing.
- `MESSAGE` `text`. Displays text on your side of the HUD.

### Constraints

`numberOfBases` = `1`
Response time per turn ≤ `100`ms
Response time for the first turn ≤ `1000`ms.

## What is in store for me in the higher leagues?

- The egg resource will be available.
- Larger maps will be available.
- Ants of opposing teams will interact.