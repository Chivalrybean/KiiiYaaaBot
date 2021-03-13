import random as rng

def die_roll(max, explode=0, min=1):
    roll = rng.randint(min, max)
    pool = [roll]
    total = roll
    overload_protection = 0
    if explode > 0:
        if roll >= explode:
            while roll >= explode:
                roll = rng.randint(min, max)
                pool.append(roll)
                total += roll
                overload_protection += 1
                if overload_protection == 31:
                    return {"total": total, "pool": pool}
    return {"total": total, "pool": pool}