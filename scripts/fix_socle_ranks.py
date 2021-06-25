import logging
import sys
import csv
from models import (
    DefaultSocleCompetency,
    DefaultSocleContainer,
    SocleCompetency,
    SocleContainer,
    Group,
    database,
)


def full_rank_list(o):
    l = [o.rank]
    container = o.container
    while container != None:
        l.insert(0, container.rank)
        container = container.container
    return l


def fix_rank(o, expected_rank):
    if o.rank != expected_rank:
        print("Rank error", o, o.rank, expected_rank)
        o.rank = expected_rank
        o.save()


def fix_full_rank(o):
    l = full_rank_list(o)
    full_rank = ".".join([f"{e}" for e in l]) + "."
    alpha_full_rank = ".".join([f"{e:04d}" for e in l]) + "."
    if o.full_rank != full_rank or o.alpha_full_rank != alpha_full_rank:
        print(
            "Full rank error",
            o,
            o.full_rank,
            full_rank,
            o.alpha_full_rank,
            alpha_full_rank,
        )
        o.full_rank = full_rank
        o.alpha_full_rank = alpha_full_rank
        o.save()


def fix_objects_rank(group_id):
    fix_objects_rank_by_cycle(group_id, "c1")
    fix_objects_rank_by_cycle(group_id, "c2")
    fix_objects_rank_by_cycle(group_id, "c3")
    fix_objects_rank_by_cycle(group_id, "c4")


def fix_objects_rank_by_cycle(group_id, cycle):
    print("  cycle", cycle)
    l1s = (
        SocleContainer.select()
        .where(
            SocleContainer.container == None,
            SocleContainer.active == True,
            SocleContainer.group_id == group_id,
            SocleContainer.cycle == cycle,
        )
        .order_by(SocleContainer.alpha_full_rank)
    )
    rank = 1
    for l1 in l1s:
        fix_rank(l1, rank)
        fix_full_rank(l1)
        rank += 1

    for l1 in l1s:
        l2s = (
            SocleContainer.select()
            .where(
                SocleContainer.container == l1,
                SocleContainer.active == True,
                SocleContainer.group_id == group_id,
            )
            .order_by(SocleContainer.alpha_full_rank)
        )
        competencies = (
            SocleCompetency.select()
            .where(
                SocleCompetency.container == l1,
                SocleCompetency.active == True,
                SocleCompetency.group_id == group_id,
                SocleCompetency.cycle == cycle,
            )
            .order_by(SocleCompetency.alpha_full_rank)
        )

        print(cycle, "l1", l1.full_rank, len(l2s), len(competencies))

        rank = 1
        for c in competencies:
            fix_rank(c, rank)
            fix_full_rank(c)
            rank += 1

        rank = 1
        for l2 in l2s:
            fix_rank(l2, rank)
            fix_full_rank(l2)
            # Fix cycle due to a typo/bug in socle loading by companion
            if l2.cycle != cycle:
                l2.cycle = cycle
                l2.save()
            rank += 1

        for l2 in l2s:
            competencies = (
                SocleCompetency.select()
                .where(
                    SocleCompetency.container == l2,
                    SocleCompetency.active == True,
                    SocleCompetency.group_id == group_id,
                    SocleCompetency.cycle == cycle,
                )
                .order_by(SocleCompetency.alpha_full_rank)
            )

            print(cycle, "l2", l2.full_rank, len(competencies))

            rank = 1
            for c in competencies:
                fix_rank(c, rank)
                fix_full_rank(c)
                rank += 1


def main():
    groups = Group.select()
    for group in groups:
        print("Checking group", group)
        fix_objects_rank(group)


if __name__ == "__main__":
    main()