# Bitcoin Insider Challenge
This is a challenge for the The Bitcoin Insider a company specialized in Bitcoin Trade Market. They Analyze the variations of the bitcoins value in the market and return statistics and important data about the best moment to invest and where.

The clients want to know from when they have to invest in a coin to have the maximum benefit from it.
In order to do that the oscillations in the value of the coin need to be studied and analyzed per day.

## Requirements

* The user should be able to save the coin data in a database.
* The user should be able to see the coin data in a table.
* The action requiered are:
    - Save the coin data in a database.
    - List the Coins prests in the Database.
    - Show the `Close` value for a specific coin.
    - Calculate the maximum profit for a specific coin.

You can find the documentation in the following link: [Api Specifications](api.spec.yaml)

## Workflow

The workflow is the following:

1. The user will send a request to the API to save the data of the coin.
2. Validation of the data will be done. If the data is not valid an error will be returned.
3. The data will be saved in the database.
4. The user will send a request to the API to list the coins.
5. The user will send a request to the API to show the `Close` value for a specific coin. If the coin pass in the parameters does not exist an error will be returned.
6. The user will send a request to the API to calculate the maximum profit for a specific coin. If the coin pass in the parameters does not exist an error will be returned.
7. The Validation of the data will be done. If the data is not valid an error will be returned.
8. The maximum profit will be calculated and returned. The formula to calculate the maximum profit is the following:

    ```
    Maximum Profit = Maximum Value - Minimum Value
    ```

    Where:

    ```
    Maximum Value = Maximum value Close of the coin in the day.
    Minimum Value = Minimum value Close of the coin in the day.
    ```

    $$\[
    \text{{profit}} = \sum_{i=0}^{n-1} (\text{{price[sell[i]]}} - \text{{price[buy[i]]}})
    \]$$


## What are we looking for?

* A **clean**, **readable** and **maintainable** code. A **well designed** and **maintainable** Arquitecture is required.
* **Tests** at least coverage a 90% of the code.
* **Documentation** of the code.
