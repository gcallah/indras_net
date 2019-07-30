"""
El Farol Bar Problem
A problem to check if it's possible for the bar to be
occupied by 60% of the population every time
"""

import random

POPULATION = 10
OPTIMAL_OCCUPANCY = 0.6 * POPULATION
MOTIVATION = [0.6] * POPULATION


def get_decision(actor):
    random_integer = random.randint(1, 100) / 100
    if random_integer <= MOTIVATION[actor]:
        return 1

    return 0


def discourage(unwanted, attenders):
    while unwanted:
        demotivate_person = attenders[random.randint(0, len(attenders) - 1)]
        MOTIVATION[demotivate_person] -= 0.05
        unwanted -= 1

    return 0


def random_drunks(weekends=10):
    # print("Motivation: ", MOTIVATION)

    attendance_record = []
    while weekends > 0:
        person = 0
        attendance = 0
        attenders = []
        while person < POPULATION:
            decision = get_decision(person)
            if decision:
                attendance += 1
                attenders.append(person)

            person += 1

        if attendance > OPTIMAL_OCCUPANCY:
            extras = attendance - OPTIMAL_OCCUPANCY
            discourage(extras, attenders)

        attendance_record.append(attendance)
        weekends -= 1

    return attendance_record


def get_average_attendance(record):
    i = len(record)
    sum_attendance = 0
    while i:
        sum_attendance += record[i - 1]
        i -= 1

    return sum_attendance / len(record)


def main():
    # global red_group
    # global blue_group
    # global env
    #
    # (env, blue_group, red_group) = set_up()
    #
    # if DEBUG2:
    #     print(env.__repr__())
    #
    # env()

    x = 45
    record = random_drunks(x)
    print(record)
    print(get_average_attendance(record))
    return 0


if __name__ == "__main__":
    main()
