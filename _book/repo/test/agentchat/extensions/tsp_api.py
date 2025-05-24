# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0
#
# Portions derived from  https://github.com/microsoft/autogen are under the MIT License.
# SPDX-License-Identifier: MIT
from typing import Any

from .tsp import tsp_data


def change_dist(dist: Any, i: int, j: int, new_cost: float) -> float:
    """Change the distance between two points.

    Args:
        dist (dict): distance matrix, where the key is a pair and value is
            the cost (aka, distance).
        i (int): the source node
        j (int): the destination node
        new_cost (float): the new cost for the distance

    Returns:
        float: the previous cost
    """
    prev_cost = dist[i, j]
    dist[i, j] = new_cost
    return prev_cost


def compare_costs(prev_cost: float, new_cost: float) -> float:
    """Compare the previous cost and the new cost.

    Args:
        prev_cost (float): the previous cost
        new_cost (float): the updated cost

    Returns:
        float: the ratio between these two costs
    """
    return (new_cost - prev_cost) / prev_cost


dists = tsp_data(5, seed=1)
