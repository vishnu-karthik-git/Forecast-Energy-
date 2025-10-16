#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 09:10:41 2023

@author: nick

Instructions:
-------------
To run this code, you need to install pyomo for optimization and highs as the solver.
Install with:
    conda install conda-forge::pyomo
    conda install conda-forge::highs

Usage:
------
python opt_func.py

Make sure you have a CSV file with a column 'price' and a datetime or integer index.
"""

import pyomo.environ as pyo
import pandas as pd


def optimize_storage_dispatch(
    price_df,
    storage_params=None,
):
    """
    Optimizes battery storage dispatch to maximize profit given external price time series.

    Returns
    -------
    model : pyomo.ConcreteModel
        Solved Pyomo model.
    """
    # Sensible defaults
    if storage_params is None:
        storage_params = {
            "capacity": 100,
            "p_max": 50,
            "eff_ch": 0.95,
            "eff_dis": 0.95,
            "soc_init": 0,
        }
    # Ensure price_df is a Series
    if isinstance(price_df, pd.DataFrame):
        price_series = price_df.iloc[:, 0]
    else:
        price_series = price_df

    n_steps = len(price_series)
    model = pyo.ConcreteModel()
    model.T = pyo.RangeSet(0, n_steps - 1)

    # Variables
    model.P_ch = pyo.Var(
        model.T, within=pyo.NonNegativeReals, bounds=(0, storage_params["p_max"])
    )
    model.P_dis = pyo.Var(
        model.T, within=pyo.NonNegativeReals, bounds=(0, storage_params["p_max"])
    )
    model.E = pyo.Var(
        model.T, within=pyo.NonNegativeReals, bounds=(0, storage_params["capacity"])
    )

    # Storage state of charge constraints
    def soc_rule(model, t):
        if t == 0:
            return (
                model.E[t]
                == storage_params["soc_init"]
                + model.P_ch[t] * storage_params["eff_ch"]
                - model.P_dis[t] / storage_params["eff_dis"]
            )
        else:
            return (
                model.E[t]
                == model.E[t - 1]
                + model.P_ch[t] * storage_params["eff_ch"]
                - model.P_dis[t] / storage_params["eff_dis"]
            )

    model.soc = pyo.Constraint(model.T, rule=soc_rule)

    # Objective: maximize profit (revenue from discharge - cost of charge)
    model.obj = pyo.Objective(
        expr=sum(
            price_series.iat[t] * model.P_dis[t] - price_series.iat[t] * model.P_ch[t]
            for t in model.T
        ),
        sense=pyo.maximize,
    )

    # Solve
    solver = pyo.SolverFactory("appsi_highs")
    solver.solve(model)

    return model

def extract_storage_profits(model, price_series, storage_params=None):
    """
    Processes the solved model and outputs a DataFrame with dispatch and profit per time step.
    """
    # Sensible defaults
    if storage_params is None:
        storage_params = {
            "eff_ch": 0.95,
            "eff_dis": 0.95,
        }
    n_steps = len(price_series)
    results_df = pd.DataFrame(
        {
            "P_ch": [pyo.value(model.P_ch[t]) for t in range(n_steps)],
            "P_dis": [pyo.value(model.P_dis[t]) for t in range(n_steps)],
            "E": [pyo.value(model.E[t]) for t in range(n_steps)],
            "price": [price_series.iat[t] for t in range(n_steps)],
        },
        index=price_series.index,
    )
    results_df["profit"] = results_df["price"] * results_df["P_dis"] - results_df["price"] * results_df["P_ch"]
    
    return results_df

def optimization_func(price_df, storage_params=None):
    # Example usage
    # Load price data from CSV. The included CSV along this code is just a sample 
    # and should be replaced with your actual price data.
    #price_csv_path = "price_data.csv"  # <-- Change to your CSV file path
    #price_df = pd.read_csv(price_csv_path, index_col=0)
    # Ensure price column is named 'price'
    if "price" not in price_df.columns:
        raise ValueError("CSV must contain a column named 'price'.")

    # Define storage parameters <- Adjust for your specific project
    storage_params = {
        "capacity": 100,      # MWh
        "p_max": 50,          # MW
        "eff_ch": 0.95,       # charging efficiency
        "eff_dis": 0.95,      # discharging efficiency
        "soc_init": 0,        # initial state of charge (MWh)
    }

    # Run optimization
    model = optimize_storage_dispatch(price_df["price"], storage_params)

    # Extract profits and dispatch info
    results_df = extract_storage_profits(model, price_df["price"], storage_params)
    # Calculate total profit
    total_profit = results_df['profit'].sum()/1000 # Convert to

    # Print results
    print("Dispatch results (head):")
    print(results_df.head())
    print(f"\nTotal profit: {total_profit:.2f} k€")  # Assuming prices are in €/MWh

    return results_df
