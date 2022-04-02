# Parse input
def get_jobs(path):
    jobs = []
    with open(path, "r") as f:
        i = 0
        for line in f:
            vals = line.split()
            # (job_number, start_time, end_time, weight)
            jobs.append((i, int(vals[0]), int(vals[1]), int(vals[2])))
            i += 1
    return jobs

# Helper anonymous functions
job_no = lambda x: x[0]
start = lambda x: x[1]
finish = lambda x: x[2]
weight = lambda x: x[3]

total_weight = lambda jobs, x: sum(list(map(weight, [jobs[i] for i in x])))

# Return non-overlapping jobs
def compatible(jobs, i):
    s = start(jobs[i])
    f = finish(jobs[i])
    comp = [jobs[j] for j in range(len(jobs)) if j != i and (finish(jobs[j]) <= s or start(jobs[j]) >= f)]
    return comp

# Dynamic programming algorithm
called_times = 0
cache = {}

def max_weight_subset(jobs):
    chosen = max_weight_subset_recurse(jobs, len(jobs)-1)
    return total_weight(jobs, chosen), chosen

def max_weight_subset_recurse(jobs, i):
    global called_times
    if len(jobs) == 0:
        called_times += 1
        return []
    elif job_no(jobs[i]) in cache.keys():
        return cache[job_no(jobs[i])]
    
    next_job = compatible(jobs, i)
    chosen_i = max_weight_subset_recurse(next_job, len(next_job)-1)
    chosen_not_i = max_weight_subset_recurse(jobs[:-1], i-1) 

    called_times += 1
    if weight(jobs[i]) + total_weight(jobs, chosen_i) >= total_weight(jobs, chosen_not_i):
        chosen_i.append(job_no(jobs[i]))
        cache[job_no(jobs[i])] = chosen_i.copy()
        return chosen_i
    else:
        cache[job_no(jobs[i])] = chosen_not_i.copy()
        return chosen_not_i


if __name__ == "__main__":
    jobs = get_jobs("jobs.txt")
    original_order = jobs
    weight, chosen = max_weight_subset(jobs)
    print(f"Optimal Job Selection: {chosen}")
    print(f"Max Weight: {weight}")
    print(f"Called Times: {called_times}")
