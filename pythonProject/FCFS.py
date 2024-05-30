import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def read_processes(filename):
    processes = []
    context_switch = 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        context_switch = int(lines[0].strip())
        for line in lines[1:]:
            pid, arrival, burst = line.split()
            processes.append(Process(int(pid), int(arrival), int(burst)))
    return processes, context_switch

def fcfs(processes):
    timeline = 0
    for process in sorted(processes, key=lambda x: x.arrival_time):
        if timeline < process.arrival_time:
            timeline = process.arrival_time
        process.start_time = timeline
        process.finish_time = timeline + process.burst_time
        process.waiting_time = timeline - process.arrival_time
        process.turnaround_time = process.finish_time - process.arrival_time
        timeline += process.burst_time

def plot_gantt_chart(processes):
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    total_burst_time = sum(p.burst_time for p in processes)
    cpu_utilization = (total_burst_time / max(p.finish_time for p in processes)) * 100

    print("Process\tArrival\tBurst\tFinish\tWaiting\tTurnaround")
    for p in processes:
        print(f"{p.pid}\t{p.arrival_time}\t{p.burst_time}\t{p.finish_time}\t{p.waiting_time}\t{p.turnaround_time}")
    print("\nAverage Waiting Time:", total_waiting_time / len(processes))
    print("Average Turnaround Time:", total_turnaround_time / len(processes))
    print("CPU Utilization: {:.2f}%".format(cpu_utilization))


    fig, ax = plt.subplots()
    y = 10
    for process in processes:
        ax.broken_barh([(process.start_time, process.burst_time)], (y, 9), facecolors=('tab:blue'))
        ax.text(process.start_time + process.burst_time / 2, y + 5, f'P{process.pid}', ha='center', va='center', color='white')
        y += 10

    ax.set_ylim(5, y + 5)
    ax.set_xlim(0, max(p.finish_time for p in processes))
    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title('FCFS Scheduling Gantt Chart')
    plt.show()


def main():
    filename = "FCFS.txt"
    processes, context_switch = read_processes(filename)
    print(f"Context Switch Time: {context_switch}")

    fcfs_processes = processes.copy()
    fcfs(fcfs_processes)
    print("\\FCFS Scheduling Results:")
    plot_gantt_chart(fcfs_processes)


if __name__ == "__main__":
    main()