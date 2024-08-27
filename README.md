# Battle Ship Challenge


## Requirements

* The user should be able to start a game.
* The user should be able to positionate the ships.
* The action requiered are:
    - Save the gamplay in database.
    - list the board ships position's.
    - Attack enemy's ships.
    - Calculate the win destroying the enemy's ships.

You can find the documentation in the following link: [Api Specifications](api.spec.yaml)

## Workflow

The workflow is the following:

1. Request to create a `Gameplay`.
2. The Gameplay will create a board and the user will positionate the ships and select the enemy.
3. The user can see the board with the ships positionated.
4. Request to positionate the ships and choose for a computer enemy or another real player.
5. After the the set of `Gameplay` the enemy's ships will be automatically positioned if the enemy is an automatic player.
6. The request of attack will include the poisition of the attack.
7. Verify if the attack is a hit or a miss.
8. If the attack is a hit, verify if the ship is destroyed.
9. If the ship is destroyed, verify if the enemy is destroyed.
10. If the enemy is destroyed, the game is over and the winner is the player.
11. Extra: Implement a Turnmanager to manage the turns of the players.